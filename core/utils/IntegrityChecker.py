from core.utils.import_yaml import get_system_config


class IntegrityChecker:
    """
    Performs an integrity check on the custom system settings:
    1. Raises warnings when a setting is missing or misspelled
    2. Sets missing settings to those from the default system.yaml

    Attributes:
        system_preferences (dict): Dictionary with custom system preferences
        base_path (string): Base path string
        model_settings_str (string): Model settings string
        debug_str (string): Debug string
        debug_mode_str (string): Debug mode string
        device_str (string): Device string
        event_detector_details_str (string): Event detector details string
        model_type_str (string): Model type string
        threshold (string): Model threshold string
        mean (string): Model mean string
        std (string): Model std string
        model_path (string): Model model_path string
        input_shape (string): Model input_shape string
        model_type (string): Model model_type string
    """

    def __init__(self, system_preferences, base_path='./'):
        """
        Args:
            system_preferences (dict): Dictionary with custom system preferences
            base_path (string): Base path string
        """
        self.system_preferences = system_preferences
        self.default_preferences = get_system_config(
            base_path=base_path)
        self.model_settings_str = 'model_settings'
        self.debug_str = 'debug'
        self.negative_prediction_text_color = 'negative_prediction_text_color'
        self.positive_prediction_text_color = 'positive_prediction_text_color'
        self.image_type = 'image_type'
        self.debug_mode_str = 'debug_mode'
        self.output_video_path = 'output_video_path'
        self.mean = 'mean'
        self.std = 'std'
        self.video_fps_rate = 'video_fps_rate'
        self.input_shape = 'input_shape'
        self.device_str = 'device'
        self.event_detector_details_str = 'event_detector_details'
        self.model_type_str = 'model_type'
        self.min_tampering_length = 'min_tampering_length'
        self.send_frames_in_second = 'send_frames_in_second'

    def run_integrity_check(self):
        """
        Runs the integrity check on the system_preferences

        Returns:
            system_preferences (dict): Updated system preferences
        """
        # Run integrity check from the main system preference categories
        self.__check_main_categories()

        return self.system_preferences

    def __check_main_categories(self):
        """
        Runs a top down check, by initially checking the main categories and
        moving to the deeper (children) settings (e.g. debug -> debug_model etc)
        """
        # Set default keys for main categories
        default_main_keys = [self.debug_str,
                             self.event_detector_details_str,
                             self.model_settings_str]
        # Check if there are any unrecognizable system preference keys
        # and issue the relevant warnings. This is mainly to capture any string
        # typos in the custom system config and encourage devs to correct them
        self.__check_default_keys(default_main_keys, self.system_preferences)

        # Check if debug category exists
        debug_exists = self.__key_exists(self.debug_str)

        # If debug_exists, check integrity of custom preferences
        # when debug_exists is False it means that we copy the default settings
        # and this check is no longer relevant
        if debug_exists:
            default_debug_keys = [self.debug_mode_str,
                                  self.negative_prediction_text_color,
                                  self.positive_prediction_text_color,
                                  self.output_video_path,
                                  ]
            # Check if custom keys have typos and issue a warning
            self.__check_default_keys(default_debug_keys,
                                      self.system_preferences[self.debug_str])
            # Check if there are any missing keys
            missing_key, preferences = \
                self.__check_missing_keys(self.system_preferences[
                                              self.debug_str],
                                          default_debug_keys,
                                          self.default_preferences[
                                              self.debug_str])
            # If missing_keys, overwrite system_preferences to the default
            if missing_key:
                self.system_preferences[self.debug_str] = preferences

        # Repeat the same steps for the model_settings category
        # Check if mode_settings category exists
        model_settings_exist = self.__key_exists(self.model_settings_str)

        # If model_settings_exist, check integrity of custom preferences
        # when model_settings_exist is False it means that we copy the default
        # settings and this check is no longer relevant
        if model_settings_exist:
            # Check if custom keys have typos and issue a warning
            default_model_settings_keys = [self.image_type,
                                           self.video_fps_rate,
                                           self.min_tampering_length,
                                           self.send_frames_in_second,
                                           self.device_str]
            self.__check_default_keys(default_model_settings_keys,
                                      self.system_preferences[
                                          self.model_settings_str])
            # Check if there are any missing keys
            missing_key, preferences = \
                self.__check_missing_keys(self.system_preferences[
                                              self.model_settings_str],
                                          default_model_settings_keys,
                                          self.default_preferences[
                                              self.model_settings_str])
            # If missing_keys, overwrite system_preferences to the default
            if missing_key:
                self.system_preferences[self.model_settings_str] = preferences

        # Repeat the same steps for the event_detector_details category
        # Check if event_detector_details category exists
        event_detector_details_exist = \
            self.__key_exists(self.event_detector_details_str)

        # If event_detector_details_exist, check integrity of custom preferences
        # when event_detector_details_exist is False it means that we copy the
        # default settings and this check is no longer relevant
        if event_detector_details_exist:
            default_detector_details_exist = [self.model_type_str]
            # Check if custom keys have typos and issue a warning
            self.__check_default_keys(default_detector_details_exist,
                                      self.system_preferences[
                                          self.event_detector_details_str])
            # Check if there are any missing keys
            missing_key, preferences = \
                self.__check_missing_keys(self.system_preferences[
                                              self.event_detector_details_str],
                                          default_detector_details_exist,
                                          self.default_preferences[
                                              self.event_detector_details_str])
            # If missing_keys, overwrite system_preferences to the default
            if missing_key:
                self.system_preferences[self.event_detector_details_str] = \
                    preferences

    def __key_exists(self, key):
        """
        Checks if the key exists in the system_preferences. If key is not
        available, it falls back to the default settings.

        Args:
            key (string): Main category key

        Returns:
            exists (bool): Flag on whether the key exists
        """
        exists = False

        # Check if key exists in the system_preferences
        if key in self.system_preferences:
            # Set exists to True
            exists = True
        else:
            # Print warning for missing category
            print(f"We couldn't find any settings for {key} "
                  f"falling back to the default system preferences..")
            # Adding missing category from the default config
            self.system_preferences[key] = \
                self.default_preferences[key]
            # Set exists to False
            exists = False

        return exists

    def __check_default_keys(self, keys, system_preferences):
        """
        Checks if the custom system settings introduce any un-known keys and
        issues a warning. This method aims to capture typos & incorrect settings

        Args:
            keys (list): List of strings
            system_preferences (dict): Dictionary with preferences
        """
        for key in system_preferences:
            if key not in keys:
                print(f"Unrecognizable system preference key: {key}")

    def __check_missing_keys(
            self,
            input_keys,
            default_keys,
            default_preferences):
        """
        Check if any keys are missing from the custom settings and copy them
        over from the default config settings

        Args:
            input_keys (dict): Dictionary with settings
            default_keys (list): List of strings
            default_preferences (dict): Dictionary with default settings

        Returns:
            missing_key (bool): Flag to denote if a missing key was detected
            input_keys (dict): Dictionary with updated settings
        """
        missing_key = False

        # Iterate through all default keys
        for key in default_keys:
            # Check if default key is missing from the input_keys
            if key not in input_keys:
                # Print a warning
                print(f"We couldn't find any settings for {key} "
                      f"falling back to the default system preferences..")
                # Add default key
                input_keys[key] = default_preferences[key]
                # Set missing key to True
                missing_key = True
            else:
                # If key exists, do nothing for now
                continue

        return missing_key, input_keys
