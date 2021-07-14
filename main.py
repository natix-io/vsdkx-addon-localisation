import importlib

import numpy as np

from core.utils.IntegrityChecker import IntegrityChecker
from core.utils.import_yaml import (get_system_config, get_model_import,
                                    get_model_config)


class EventDetector:
    """
    Wrapper class that handles the following:
        1. It imports the system and model configs from custom locations
        2. It Initializes the camera tampering detection object
        3. It wraps the inference method of the camera tampering detection class

        Attributes:
            base_path (string): Base path
            system_config (dict): Dictionary with system preferences
            model_settings (dict): Dictionary with model settings
            model_type (string): Type of model - defaults resnet50
            system_models (dict): Contains system model import path, defined
                in config/models.yaml {models_import_path}
            debug_config (dict): Debug config
            debug_mode (bool): Debug mode
            model_config (dict): System model preferences
    """

    def __init__(
            self,
            system_config=None,
            base_path='./'):
        """
        Args:
            system_config (dict): Dictionary with system preferences
            base_path (string): Base path string
        """
        self.base_path = base_path
        if system_config is None:
            self.system_config = get_system_config(
                base_path=self.base_path)
        else:
            self.system_config = system_config

        checker = IntegrityChecker(system_preferences=self.system_config,
                                   base_path=base_path)

        self.system_config = checker.run_integrity_check()
        self.event_detector_details = \
            self.system_config['event_detector_details']
        self.model_type = self.event_detector_details['model_type']
        self.image_type = self.system_config['model_settings']['image_type']
        self.model_settings = self.system_config['model_settings']
        self.system_models = get_model_import(base_path=base_path)
        self.class_name = self.system_models['class_name']
        self.debug_config = self.system_config['debug']
        self.debug_mode = self.debug_config['debug_mode']
        self.model_config = get_model_config(base_path=base_path)
        self.model = self.model_init()

    def model_init(self):
        """
        Creates an instance of a camera tampering detection object.

        Returns:
            (object) Model object
        """
        module = importlib.import_module(self.system_models[self.model_type])
        model = getattr(module, self.class_name)(
            model_settings=self.model_settings,
            image_type=self.image_type,
            model_type=self.model_type,
            debug_mode=self.debug_mode
        )
        return model

    def predict(self, image: np.ndarray) -> dict:
        """
        Wrapper method that runs the inference on the initialized
        object detection model.
        Accepts an image as input and returns the boolean type label
        whether tampering is happening or not, in the dict under "extra" key.

        Args:
            image (np.array): 3D Image array of the shape [H, W, C]

        Returns:
            dict with following structure: {..., 'extra': {'is_tampering': prediction}}
            - "prediction" boolean type and it is False if no tampering is happening and True if it is.
        """
        prediction = self.model.inference(frame=image)
        result_dict = {'boxes': [],
                       'scores': [],
                       'classes': [],
                       'extra':
                           {
                               'is_tampering': prediction
                           }
                       }

        return result_dict
