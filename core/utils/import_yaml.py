import yaml


def import_config_file(path):
    """
    Imports the contents of an entire yaml file into a dictionary
    for future use

    Args:
        path (string): path to a yaml file

    Returns:
        (dict): dictionary of yaml key-value pairs
    """
    with open(path) as config_file:
        config_data = yaml.load(config_file, Loader=yaml.FullLoader)
    return config_data


def get_system_config_data_by_key(
        key,
        base_path='./',
        path='config/system.yaml'):
    """
    Wrapper function to import a value from system.yaml

    Args:
        key (string): key to extract data by
        base_path (string): Base path string
        path (string): path to a yaml file

    Returns:
        (any) data associated with the given key
        (none) if key is not found
    """
    config = import_config_file(base_path + path)
    return config.get(key)


def get_model_config_data_by_key(
        key,
        base_path='./',
        path='config/models.yaml'
):
    """
    Wrapper function to import a value from models.yaml

    Args:
        key (string): key to extract data by
        base_path (string): Base path string
        path (string): path to a yaml file

    Returns:
        (any) data associated with the given key
        (none) if key is not found
    """
    config = import_config_file(base_path + path)
    return config.get(key)


def get_class_cfg(base_path='./', path='config/classes.yaml'):
    """
    Wrapper function to get class config from classes.yaml

    Args:
        base_path (string): Base path string
        path (string): path to a yaml file

    Returns:
        (dict) with class properties
    """
    config = import_config_file(base_path + path)
    return config


def get_model_config(base_path='./', path='config/models.yaml'):
    """
    Wrapper function to get the models's properties from models.yaml

    Args:
        base_path (string): Base path string
        path (string): path to a yaml file

    Returns:
        (dict) with models properties
    """
    config = import_config_file(base_path + path)
    return config


def get_system_config(base_path='./', path='config/system.yaml'):
    """
    Wrapper function to get the models's properties from system.yaml

    Args:
        base_path (string): Base path string
        path (string): path to a yaml file

    Returns:
        (dict) with models properties
    """
    config = import_config_file(base_path + path)
    return config


def get_model_import(base_path='./', path='config/models.yaml'):
    """
    Wrapper function to get the model type properties from models.yaml

    Args:
        base_path (string): Base path string
        path (string): path to models config

    Returns:
        (dict) with models properties
    """
    config = import_config_file(base_path + path)
    return config['models_import_path']
