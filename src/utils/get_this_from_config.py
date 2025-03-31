from configobj import ConfigObj

async def get_this_from_runtime_config(key):
    config = ConfigObj("config.ini")
    if key not in config:
        raise ValueError(f"Key {key} not found in config")
    return config[key]

config_file = ConfigObj("config.ini")
async def get_this_from_cached_config(key):
    if key not in config_file:
        raise ValueError(f"Key {key} not found in config")
    return config_file[key]