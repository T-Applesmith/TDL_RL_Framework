import configparser
#https://docs.python.org/3/library/configparser.html


def write_config(config_dict):
    config = configparser.ConfigParser()

    # Default
    config['DEFAULT'] = {}

    # Options
    config['OPTIONS'] = {}
    
    if config_dict.get('fps_cap'):
        config['OPTIONS']['fps_cap'] = config_dict['fps_cap']
    else:
        config['OPTIONS']['fps_cap'] = '60'
        
    if config_dict.get('fps_display'):
        config['OPTIONS']['fps_display'] = config_dict['fps_display']
    else:
        config['OPTIONS']['fps_display'] = 'False'

    # Keybindings
    config['KEYBINDINGS'] = {}
    
    if config_dict.get('key_wait'):
        config['KEYBINDINGS']['key_wait'] = config_dict['key_wait']
    else:
        config['KEYBINDINGS']['key_wait'] = 'z'
    
    # Development Tools
    config['DEV'] = {}

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    return


def read_config():
    config = configparser.ConfigParser()
    update_configs = False
    config_dict = {}

    try:
        config.read('config.ini')
        config_default = config['DEFAULT']
        config_options = config['OPTIONS']
        config_keybindings = config['KEYBINDINGS']
        config_dev = config['DEV']

        config_dict = {}

        # Extract values to dictionary
        for key in config_default:
            config_dict[key] = config_default[key]
        for key in config_options:
            config_dict[key] = config_options[key]
        for key in config_keybindings:
            config_dict[key] = config_keybindings[key]
        for key in config_dev:
            config_dict[key] = config_dev[key]
    except:
        update_configs = True

    return update_configs, config_dict
