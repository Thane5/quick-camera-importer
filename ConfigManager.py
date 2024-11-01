import configparser
import os
from pathlib import Path

def set_default_path(defaultpath):
    # Try to read the existing configuration
    config = configparser.ConfigParser()
    config_path = Path("quickcameraimporter.ini")

    if config_path.exists():
        config.read(config_path)

    # Ensure the 'GENERAL' section exists
    if 'GENERAL' not in config:
        config['GENERAL'] = {}

    # Update the default path in the configuration
    config['GENERAL']['defaultpath'] = defaultpath

    # Save the updated configuration to the file
    with config_path.open('w') as configfile:
        config.write(configfile)

    # Print the updated configuration
    print(f"Default path set to: {defaultpath}")

def get_default_path():
    # Try to read the configuration from the INI file
    config = configparser.ConfigParser()
    config_path = Path("quickcameraimporter.ini")

    if config_path.exists():
        config.read(config_path)

    # Get the default path from the configuration
    defaultpath = config.get('GENERAL', 'defaultpath', fallback=None)

    # If defaultpath is not found, return a default value
    if defaultpath is None:
        defaultpath = os.path.join(os.path.expanduser("~"), "Pictures")

    return defaultpath