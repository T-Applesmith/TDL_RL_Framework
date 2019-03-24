import configparser
#https://docs.python.org/3/library/configparser.html


def write_config(config_dict):
    config = configparser.ConfigParser()

    # Default
    config['DEFAULT'] = {}

    # Options
    config['OPTIONS'] = {}

    setup_options_config(config, config_dict, 'OPTIONS', 'fps_cap', '60')
    setup_options_config(config, config_dict, 'OPTIONS', 'fps_display', 'False')

    # Keybindings
    config['KEYBINDINGS'] = {}

    # Keybinding - Movement
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_wait', 'z')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_north', 'k')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_south', 'j')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_west', 'h')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_east', 'l')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_northwest', 'y')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_northeast', 'u')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_southwest', 'b')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_southeast', 'n')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_down_stairs', '>')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_up_stairs', '<')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_west', 'h')

    # Keybinding - Actions
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_pickup', 'g')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_drop', 'd')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_look', 'L')

    # Keybinding - Menus
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_inventory', 'i')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_character_menu', 'c')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_equipment', 'e')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_help', '?')
    setup_keybindings_config(config, config_dict, 'KEYBINDINGS', 'key_dev_console', '~')
      
    # Development Tools
    config['DEV'] = {}

    setup_options_config(config, config_dict, 'DEV', 'allow_keybinding', 'False')
    setup_options_config(config, config_dict, 'DEV', 'verbose', 'False')
        
    # write to file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    return


def setup_options_config(config, config_dict, location, name, default):
    if config_dict.get(name):
        config[location][name] = config_dict[name]
    else:
        config[location][name] = default
    return


def setup_keybindings_config(config, config_dict, location, name, default):
    if config_dict.get(name) and config_dict['allow_keybinding'].lower == 'true':
        config[location][name] = config_dict[name]
    else:
        config[location][name] = default


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

    return config_dict
