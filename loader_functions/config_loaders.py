import configparser
#https://docs.python.org/3/library/configparser.html


def write_config(config_default_dict):
    config = configparser.ConfigParser()

    if config_default_dict['fps_cap']:
        config['DEFAULT']['fps_cap'] = config_default_dict['fps_cap']
    else:
        config['DEFAULT']['fps_cap'] = 60
        
    if config_default_dict['fps_display']:
        config['DEFAULT']['fps_display'] = config_default_dict['fps_display']
    else:
        config['DEFAULT']['fps_display'] = 'False'

    config['Dev'] = {}

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    return


def read_config():
    config = configparser.ConfigParser()

    config.read('config.ini')
    config_default = config['DEFAULT']

    config_default_dict = {}

    for key in config_default:
        config_default_dict[key] = config_default[key]

    return config_default_dict
