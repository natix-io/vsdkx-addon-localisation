from typing import Dict

import numpy as np
import torch


class DepthEstimator:
    """
    Class for object detection

    Attributes:
        model_settings (dict): Model settings config with the following keys:
                'image_type' (string): Channel ordering of an input image either 'BGR' or 'RGB'
                'device' (string): Where to run the model, must be either 'cuda'
                or 'cpu'

    """

    def __init__(self,
                 model_settings,
                 model_type: str,
                 image_type: str,
                 debug_mode: bool = False
                 ):
        self.image_type = image_type
        self.model_type = model_type
        self.debug_mode = debug_mode
        self.device = model_settings['device']
        self.model = torch.hub.load("intel-isl/MiDaS", self.model_type).to(
            self.device)
        self.transform = None
        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
        if self.model_type == "DPT_Large" or self.model_type == "DPT_Hybrid":
            self.transform = midas_transforms.dpt_transform
        else:
            self.transform = midas_transforms.small_transform

    @torch.no_grad()
    def inference(self, frame: np.ndarray, detections: Dict) -> Dict:
        """
        Estimates Depth of detected object on image.

        Args:
            frame (np.ndarray): 3D image array
            detections (dict):

        Returns:
            (Dict): Dict containing the same information about detected object
                    as before but all elements will be sorted in the order of
                    object distance from the camera: first will be closest, ect.
        """
