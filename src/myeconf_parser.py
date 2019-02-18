import configparser
import os

from myelindl.log import logger

def config_section_map(configer):
    """
        Converts a ConfigParser object into a dictionary.

        The resulting dictionary has sections as keys which point to a dict of the
        sections options as key => value pairs.
        :param config_files: a list of config files returned by configparser.read()
        :return: a dictionary of [section][key]:[value]
    """
    conf_dict = {}
    for section in configer.sections():
        conf_dict[section] = {}
        for key, val in configer.items(section):
            conf_dict[section][key] = val
    return conf_dict


def get_config(config_files, toMap=True):
    """
    setup the config files of myelintek
    :param config_files: a list of config files
    :return: a dictionary of [section][key]:[value]
    """
    # get config
    confparser = configparser.ConfigParser()
    confparser._interpolation = configparser.ExtendedInterpolation()
    config_files = confparser.read(config_files)

    config = None

    # global config
    if config_files:
        if toMap:
            config = config_section_map(confparser)
        else:
            config = config_files

    return config

from functools import wraps
# arg conf_sess_name is used to identify which session you want to read value from.
def get_value_decorator(config, conf_sess_name):

    logger.debug("config = {}, \nconf_sess_name = {}".format(config, conf_sess_name))

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # check the config session existence
                if config and config[conf_sess_name]:
                    return f(*args, **kwargs)
            except KeyError as e:
                logger.warning('No such config session in myeconfig')

        return wrapper

    return decorator

# an example
SENAME = "your session in config"
myconfig = {}
@get_value_decorator(myconfig, SENAME)
def myconfig_value(keyword, def_value):
    try:
        return myconfig[SENAME][keyword]
    except KeyError as e:
        logger.warning('Key Error: %s, use def_value', keyword)
        return def_value

