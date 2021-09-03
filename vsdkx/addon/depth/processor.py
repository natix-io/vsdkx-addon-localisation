from typing import Dict, List

import numpy as np
import torch

from vsdkx.core.interfaces import Addon, AddonObject


class DepthEstimator(Addon):
    """
    Depth Estimator class

    Attributes:
        'device' (string): Where to run the model, must be either
                'cuda' or 'cpu';
        'stages' (int): For how many levels to divide objects' distances from a
                 camera. For example, if stages is 3, then object will be
                 classified by 3 levels of distance from a camera: close,
                 middle and far;
        'grid_size' (int): used to calculate the depth;
        'model_type' (string): The name of depth estimator model;
    """

    def __init__(self, addon_config: dict, model_settings: dict,
                 model_config: dict, drawing_config: dict):
        super().__init__(addon_config, model_settings, model_config,
                         drawing_config)
        # self.debug_mode = drawing_config.get("depth", {})
        self.device = model_settings['device']
        self.stages = addon_config['stages']
        self.grid_size = addon_config['grid_size']
        self.model_type = addon_config['model_type']
        self.model = torch.hub.load("intel-isl/MiDaS", self.model_type).to(
            self.device)
        self.transform = None
        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
        if self.model_type == "DPT_Large" or self.model_type == "DPT_Hybrid":
            self.transform = midas_transforms.dpt_transform
        else:
            self.transform = midas_transforms.small_transform

    @torch.no_grad()
    def post_process(self, addon_object: AddonObject) -> AddonObject:
        """
        Estimates Depth of detected object on image. The function uses objects'
        coordinates to estimate their relative depth predicted by depth
        estimation model. Then function sorts objects boxes, scores and classes
        by their relative distance from a camera: the first, the 2nd, ...

        Args:
            frame (np.ndarray): 3D image array
            detections (dict): Dictionary with the following keys:
                               boxes (list): Array with bounding boxes
                               scores (list): Array with confidence scores
                               classes (list): Array with class names

        Returns:
            (Dict): Dict containing the same information about detected object
                    as before but all elements will be sorted in the order of
                    object's distance from the camera: first will be closest,ect
        """
        coords = addon_object.inference.boxes
        # if no objects are detected then return same input
        if len(coords) == 0:
            return addon_object

        # get confidence and class values to reorder them by objects' distances
        # from a camera
        scores = addon_object.inference.scores
        classes = addon_object.inference.classes

        # estimate depth of every pixel of an inout image
        depth_img = self._estimate_depth(addon_object.frame)
        # get center coordinates of detected objects
        center_points = self._get_center_points(coords)
        # get estimated depth values of around centers of objects
        image_squares = self._get_center_area(depth_img, center_points,
                                              square_size=self.grid_size)

        # get average of estimated depth values around objects
        object_distances = [int(grid.mean()) for grid in image_squares]
        # get indices of sorted estimated depth values from closest to furthest
        depth_sizes = np.argsort(object_distances).tolist()
        depth_sizes = depth_sizes[::-1]
        # now sort coords, classes and scores by objects distances from a camera
        sorted_coords = np.array(coords)[depth_sizes].astype(np.int32).tolist()
        sorted_scores = np.array(scores)[depth_sizes].astype(np.int32).tolist()
        sorted_classes = np.array(classes)[depth_sizes].astype(
            np.int32).tolist()

        # overwrite old values
        addon_object.inference.boxes = sorted_coords
        addon_object.inference.scores = sorted_scores
        addon_object.inference.classes = sorted_classes

        # categorise objects by distance stages from a camera
        sorted_obj_distances = np.array(object_distances)[depth_sizes]
        min_dist, max_dist = depth_img.min(), depth_img.max()
        step_size = (max_dist - min_dist) / self.stages
        stage_distance_ids = []
        for i in range(len(sorted_obj_distances)):
            object_dist = sorted_obj_distances[i]
            for j in range(0, self.stages):
                if object_dist >= (
                        step_size * j + min_dist) and object_dist <= (
                        step_size * (j + 1) + min_dist):
                    stage_distance_ids.append((self.stages - 1) - j)
                    break
        try:
            addon_object.inference.extra['distance_ids'] = stage_distance_ids
        except KeyError:
            addon_object.inference.extra['extra'] = {
                'distance_ids': stage_distance_ids
            }

        return addon_object

    @staticmethod
    def _get_center_points(coords: List[List[int]]) -> List[List[int]]:
        """
        Finds center points of detected object from coordinates.

        Args:
            coords (list): List of Lists of x1,y1,x2,y2 coordinates.

        Returns:
            (List[List[int]]): objects center coordinates.
        """
        center_points = [[int((y1 + y2) / 2), int((x1 + x2) / 2)] for
                         x1, y1, x2, y2 in coords]
        return center_points

    @staticmethod
    def _get_center_area(image: np.ndarray,
                         center_points: list,
                         square_size: int = 10) -> List[np.ndarray]:
        """
        Splits image into centers.

        Args:
            image (np.ndarray): 3D image
            center_points (list): x,y coords of centers
            square_size (int): half are of grid size

        Returns:
            (list): Center areas of detected objects.
        """
        image_squares = [image[(y - square_size):(y + square_size),
                         (x - square_size):(x + square_size)] for y, x in
                         center_points]
        return image_squares

    def _estimate_depth(self, image: np.ndarray) -> np.ndarray:
        """
        Returns depth estimated image.

        Args:
            image (np.ndarray): BGR image

        Returns:
            (np.ndarray): Depth estimated image
        """
        input_batch = self.transform(image).to(self.device)
        with torch.no_grad():
            prediction = self.model(input_batch)

            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=image.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()

            output = prediction.cpu().numpy()
        return output
