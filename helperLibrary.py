# Helper library
import os
import configparser
import logging
from pathlib import Path


def init_logger(log_folder_path, log_level, log_mode):

    if not os.path.exists(log_folder_path):
        # Log folder path does not exists. Defaulting to /opt/extract/Log/log.txt
        log_file_path = Path("/opt/extract/Log/log.txt")
    else:
        log_file_path = Path(log_folder_path, "log.txt")

    log_level_dict = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING,
                      "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL}
    if log_level.strip() not in log_level_dict:
        level = logging.DEBUG
    else:
        level = log_level_dict[log_level]

    log_mode_dict = {"APPEND": "a", "OVERWRITE": "w"}
    if log_mode.strip() not in log_mode_dict:
        filemode = "w"
    else:
        filemode = log_mode_dict[log_mode]

    try:
        logging.basicConfig(force=True, filename=str(log_file_path), level=level, filemode=filemode,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    except Exception as e:
        print("CRITICAL", "Exception occurred while configuring Logger", flush=True)
        return False

    return True


def print_msg(arg1, arg2="", exc_info=False):
    print(arg2)
    if arg1 == "DEBUG":
        logging.debug(arg2)
    elif arg1 == "INFO":
        logging.info(arg2)
    elif arg1 == "WARNING":
        logging.warning(arg2)
    elif arg1 == "ERROR":
        logging.error(arg2, exc_info=exc_info)
    elif arg1 == "CRITICAL":
        logging.critical(arg2, exc_info=True)
    else:
        logging.debug(arg1)


def get_config_value(config_file_path, config_section, config_item):
    config = configparser.ConfigParser()
    config.read(config_file_path)
    if len(config.sections()) == 0:
        print_msg("ERROR", f"No valid configuration file found '{config_file_path}'")
        return False, ""
    if config_section in config:
        if config_item in config[config_section]:
            return True, config[config_section][config_item]
        else:
            print_msg("ERROR", f"Configuration Item '{config_item}' not found in config section '{config_section}'")
            return False, ""
    else:
        print_msg("ERROR", f"Configuration Section '{config_section}' not found in config file")
        return False, ""


def get_config_section(config_file_path, config_section):
    config = configparser.ConfigParser()
    config.read(config_file_path)
    if len(config.sections()) == 0:
        print("ERROR ", f"No valid configuration file found '{config_file_path}'", flush=True)
        return False
    if config_section in config:
        section_values = {"Status": "success"}
        for key in config[config_section]:
            section_values[key] = config[config_section][key]
        return section_values
    else:
        print("ERROR ", f"Configuration Section '{config_section}' not found in config file", flush=True)
        return False
