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

    # Keybinding - Movement
    if config_dict.get('key_wait') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_wait'] = config_dict['key_wait']
    else:
        config['KEYBINDINGS']['key_wait'] = 'z'

    if config_dict.get('key_north') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_north'] = config_dict['key_north']
    else:
        config['KEYBINDINGS']['key_north'] = 'k'

    if config_dict.get('key_south') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_south'] = config_dict['key_south']
    else:
        config['KEYBINDINGS']['key_south'] = 'j'

    if config_dict.get('key_west') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_west'] = config_dict['key_west']
    else:
        config['KEYBINDINGS']['key_west'] = 'h'

    if config_dict.get('key_east') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_east'] = config_dict['key_east']
    else:
        config['KEYBINDINGS']['key_east'] = 'l'

    if config_dict.get('key_northwest') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_northwest'] = config_dict['key_northwest']
    else:
        config['KEYBINDINGS']['key_northwest'] = 'y'

    if config_dict.get('key_northeast') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_northeast'] = config_dict['key_northeast']
    else:
        config['KEYBINDINGS']['key_northeast'] = 'u'

    if config_dict.get('key_southwest') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_southwest'] = config_dict['key_southwest']
    else:
        config['KEYBINDINGS']['key_southwest'] = 'b'

    if config_dict.get('key_southeast') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_southeast'] = config_dict['key_southeast']
    else:
        config['KEYBINDINGS']['key_southeast'] = 'n'

    if config_dict.get('key_down_stairs') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_down_stairs'] = config_dict['key_down_stairs']
    else:
        config['KEYBINDINGS']['key_down_stairs'] = '>'

    if config_dict.get('key_up_stairs') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_up_stairs'] = config_dict['key_up_stairs']
    else:
        config['KEYBINDINGS']['key_up_stairs'] = '<'

    # Keybinding - Actions
    if config_dict.get('key_pickup') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_pickup'] = config_dict['key_pickup']
    else:
        config['KEYBINDINGS']['key_pickup'] = 'g'

    if config_dict.get('key_drop') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_drop'] = config_dict['key_drop']
    else:
        config['KEYBINDINGS']['key_drop'] = 'd'

    # Keybinding - Menus
    if config_dict.get('key_inventory') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_inventory'] = config_dict['key_inventory']
    else:
        config['KEYBINDINGS']['key_inventory'] = 'i'

    if config_dict.get('key_character_menu') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_character_menu'] = config_dict['key_character_menu']
    else:
        config['KEYBINDINGS']['key_character_menu'] = 'c'

    if config_dict.get('key_equipment') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_equipment'] = config_dict['key_equipment']
    else:
        config['KEYBINDINGS']['key_equipment'] = 'e'

    if config_dict.get('key_help') and (config_dict['allow_keybinding'] in ['True', 'TRUE']):
        config['KEYBINDINGS']['key_help'] = config_dict['key_help']
    else:
        config['KEYBINDINGS']['key_help'] = '?'

      
    # Development Tools
    config['DEV'] = {}

    if config_dict.get('allow_keybinding'):
        config['DEV']['allow_keybinding'] = config_dict['allow_keybinding']
    else:
        config['DEV']['allow_keybinding'] = 'False'

    if config_dict.get('verbose'):
        config['DEV']['verbose'] = config_dict['verbose']
    else:
        config['DEV']['verbose'] = 'False'
        
    # write to file
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

    return config_dict
