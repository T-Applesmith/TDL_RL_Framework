import configparser
#https://docs.python.org/3/library/configparser.html


def write_config(fps=60, fps_display=False):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'fps_cap': '60', 'fps_display': 'False'}
    config['Dev'] = {}

    #config['DEFAULT']['fps'] = fps

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    return


def read_config():
    config = configparser.ConfigParser()

    config.read('config.ini')
    config_default = config['DEFAULT']

    config_dict = {}

    for key in config_default:
        config_dict[key] = config_default[key]

    return config_dict
