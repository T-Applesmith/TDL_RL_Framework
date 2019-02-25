from game_states import GameStates


def handle_keys(user_input, game_state, config_dict):
    if user_input:
        if game_state == GameStates.PLAYERS_TURN:
            return handle_player_turn_keys(user_input, config_dict)
        elif game_state == GameStates.PLAYER_DEAD:
            return handle_player_dead_keys(user_input)
        elif game_state == GameStates.TARGETING:
            return handle_targeting_keys(user_input)
        elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
            return handle_inventory_keys(user_input)
        elif game_state == GameStates.LEVEL_UP:
            return handle_level_up_menu(user_input)
        elif game_state == GameStates.CHARACTER_SCREEN:
            return handle_character_screen(user_input)
        elif game_state == GameStates.EQUIPMENT_MENU:
            return handle_equipment_menu(user_input)
        elif game_state == GameStates.KEYBINDINGS_MENU:
            return handle_keybindings_menu(user_input, config_dict)
        elif game_state == GameStates.ESCAPE_MENU:
            return handle_escape_menu(user_input)
        elif game_state == GameStates.HELP_SCREEN:
            return handle_help_screen(user_input)
        elif game_state == GameStates.OPTIONS_MENU:
            return handle_options_menu(user_input)

    return {}


def handle_player_turn_keys(user_input, config_dict):
    try:
        key_char = user_input.text
    except AttributeError:
        print('ERROR CAUGHT: AttributeError: input_handlers.handle_player_turn_keys')
        key_char = chr(user_input)
        user_input = chr(user_input)

    # Movement keys
    if user_input.key == 'UP' or key_char == config_dict.get('key_north'):
        #if user_input.key == 'UP' or key_char == 'k':
        return {'move': (0, -1)}
    elif user_input.key == 'DOWN' or key_char == config_dict.get('key_south'):
        #elif user_input.key == 'DOWN' or key_char == 'j':
        return {'move': (0, 1)}
    elif user_input.key == 'LEFT' or key_char == config_dict.get('key_west'):
        #elif user_input.key == 'LEFT' or key_char == 'h':
        return {'move': (-1, 0)}
    elif user_input.key == 'RIGHT' or key_char == config_dict.get('key_east'):
        #elif user_input.key == 'RIGHT' or key_char == 'l':
        return {'move': (1, 0)}
    elif key_char == config_dict.get('key_northwest'):
        #elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == config_dict.get('key_northeast'):
        #elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == config_dict.get('key_southwest'):
        #elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == config_dict.get('key_southeast'):
        #elif key_char == 'n':
        return {'move': (1, 1)}
    elif key_char == config_dict.get('key_wait'):
        #elif key_char == 'z':
        return {'wait': True}

    if key_char == config_dict.get('key_pickup'):
        #if key_char == 'g':
        return {'pickup': True}

    elif key_char == config_dict.get('key_inventory'):
        #elif key_char == 'i':
        return {'show_inventory': True}

    elif key_char == config_dict.get('key_drop'):
        #elif key_char == 'd':
        return {'drop_inventory': True}

    elif key_char == config_dict.get('key_down_stairs'):
        #elif key_char == '>':
        return {'down_stairs': True}

    elif key_char == config_dict.get('key_character_menu'):
        #elif key_char == 'c':
        return {'show_character_screen': True}

    elif key_char == config_dict.get('key_equipment'):
        #elif key_char == 'e':
        return {'show_equipment_menu': True}

    elif key_char == config_dict.get('key_help'):
        #elif key_char == '?':
        #Open the help_screen
        return {'show_help_screen': True}

    # CANNOT BE RE-BOUND
    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':
        # Escape Menu
        return {'return_to_game': True}

    # No key was pressed
    return {}


def handle_targeting_keys(user_input):
    if user_input.key == 'ESCAPE':
        return {'return_to_game': True}

    return {}


def handle_keybindings_menu(user_input, config_dict):
    if user_input.key == 'ESCAPE':
        return {'return_to_game': True}

    if config_dict['allow_keybinding'] in ['True', 'TRUE']:
        pass

    return {}


def handle_options_menu(user_input):
    if user_input.key == 'ESCAPE':
        return {'return_to_game': True}

    return {}


def handle_help_screen(user_input):
    if user_input.key == 'ESCAPE':
        return {'return_to_game': True}

    return {}


def handle_escape_menu(user_input):
    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':
        #Return to the previous game state
        return {'return_to_game': True}
    elif user_input.char == 'o':# or user_input.key == 'O':
        #Open the options_menu
        return {'show_options_menu': True}
    elif user_input.char == 'k':
        #Open the keybindings_menu
        return {'show_keybindings_menu': True}
    elif user_input.char == 'h':# or user_input.key == 'H':
        #Open the help_screen
        return {'show_help_screen': True}
    elif user_input.char == 's':# or user_input.key == 'S':
        #Save and quit the game
        return {'exit': True}

    return {}


def handle_player_dead_keys(user_input):
    key_char = user_input.char

    if key_char == 'i':
        return {'show_inventory': True}
    if key_char == 'e':
        return {'show_equipment': True}

    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}


def handle_inventory_keys(user_input):
    if not user_input.char:
        return {}

    index = ord(user_input.char) - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':
        # Return to the game
        return {'return_to_game': True}

    return {}


def handle_main_menu(user_input):
    if user_input:
        key_char = user_input.char

        if key_char == 'a':
            return {'new_game': True}
        elif key_char == 'b':
            return {'load_game': True}
        elif key_char == 'c' or user_input.key == 'ESCAPE':
            return {'exit': True}

    return {}


def handle_level_up_menu(user_input):
    if user_input:
        key_char = user_input.char

        if key_char == 'a':
            return {'level_up': 'hp'}
        elif key_char == 'b':
            return {'level_up': 'str'}
        elif key_char == 'c':
            return {'level_up': 'def'}

    return {}


def handle_character_screen(user_input):
    if user_input.key == 'ESCAPE':
        return {'return_to_game': True}

    return {}


def handle_equipment_menu(user_input):
    if not user_input.char:
        return {}

    index = ord(user_input.char) - ord('a')

    if index >= 0:
        return {'equipment_index': index}

    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif user_input.key == 'ESCAPE':
        # Return to the game
        return {'return_to_game': True}

    return {}


def handle_mouse(mouse_event):
    if mouse_event:
        (x, y) = mouse_event.cell

        if mouse_event.button == 'LEFT':
            return {'left_click': (x, y)}
        elif mouse_event.button == 'RIGHT':
            return {'right_click': (x, y)}

    return {}
