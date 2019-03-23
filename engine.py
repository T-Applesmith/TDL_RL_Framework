#http://www.roguebasin.com/index.php?title=Roguelike_Tutorial,_using_python3%2Btdl
#http://rogueliketutorials.com/

import tdl
#https://python-tcod.readthedocs.io/en/latest/tdl.html

from tcod import image_load, console
#https://python-tcod.readthedocs.io/en/latest/tcod.html

from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.json_loaders import load_game, save_game
from loader_functions.config_loaders import write_config, read_config

from utils.map_utils import next_floor

from death_functions import kill_monster, kill_player
from dev.dev_console import dev_powers
from dev.dev_print import print_dev
from entity import Entity, get_blocking_entities_at_location
from game_messages import Message
from game_states import GameStates
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from menus import main_menu, message_box
from render_functions import clear_all, render_all, RenderOrder


def play_game(player, entities, game_map, message_log, game_state, root_console, con, panel, constants, config):
    print_dev('======================\nBeginning to play game\n======================', config)
    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    fov_recompute = True

    mouse_coordinates = (0, 0)
    previous_mouse_coordinates = mouse_coordinates
    mouse_coordinates_changed = False

    previous_game_state = game_state

    targeting_item = None
    dev_console_input = ''

    while not tdl.event.is_window_closed():
        if fov_recompute:
            game_map.compute_fov(player.x, player.y, fov=constants['fov_algorithm'], radius=constants['fov_radius'],
                                 light_walls=constants['fov_light_walls'])

        render_all(con, panel, entities, player, game_map, fov_recompute, root_console, message_log,
                   mouse_coordinates, game_state, constants, config, dev_console_input)
        tdl.flush()

        clear_all(con, entities)

        fov_recompute = False

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
            elif event.type == 'MOUSEMOTION':
                previous_mouse_coordinates = mouse_coordinates
                mouse_coordinates = event.cell
                if mouse_coordinates != previous_mouse_coordinates:
                    mouse_coordinates_changed = True
                elif mouse_coordinates == previous_mouse_coordinates:
                    mouse_coordinates_changed = False
                #print('{0}'.format(mouse_coordinates))
            elif event.type == 'MOUSEDOWN':
                user_mouse_input = event
                break
            
        else:
            user_input = None
            user_mouse_input = None

        if not (user_input or user_mouse_input or mouse_coordinates_changed):
            #skips everything else if no input
            continue

        player_turn_results = []

        action = handle_keys(user_input, game_state, config)
        mouse_action = handle_mouse(user_mouse_input)

        move = action.get('move')
        wait = action.get('wait')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        escape_index = action.get('escape_index')
        down_stairs = action.get('down_stairs')
        level_up = action.get('level_up')
        look = action.get('look')
        
        show_character_screen = action.get('show_character_screen')
        show_equipment_menu = action.get('show_equipment_menu')
        show_keybindings_menu = action.get('show_keybindings_menu')
        show_options_menu = action.get('show_options_menu')
        show_help_screen = action.get('show_help_screen')
        show_dev_console = action.get('show_dev_console')
        equipment_index = action.get('equipment_index')
        return_to_game = action.get('return_to_game')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        # dev console input
        dev_console_keypress = action.get('dev_console_keypress')
        dev_console_backspace = action.get('dev_console_backspace')
        dev_console_submit = action.get('dev_console_submit')

        # handle dev console
        print_dev('dev_console_keypress:{0}, console_input:{1}'.format(dev_console_keypress,dev_console_input), config)
        if dev_console_input == None or show_dev_console:
            dev_console_input = ''
        elif dev_console_keypress and len(dev_console_input) < 55:
            dev_console_input = dev_console_input + str(dev_console_keypress)
        elif dev_console_backspace:
            dev_console_input = dev_console_input[:len(dev_console_input)-1]
        elif dev_console_submit:
            player_turn_results.extend(dev_powers(dev_console_input, entities, message_log, constants, config))
            dev_console_input = ''

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')
        message_log_up = mouse_action.get('message_log_up')
        message_log_down = mouse_action.get('message_log_down')

        if (move or (left_click and ((abs(left_click[0] - player.x) <= 1) and (abs(left_click[1] - player.y) <= 1)))) and game_state == GameStates.PLAYERS_TURN:
            if move:
                dx, dy = move
                destination_x = player.x + dx
                destination_y = player.y + dy
            elif left_click:
                dx = left_click[0] - player.x
                dy = left_click[1] - player.y
                destination_x, destination_y = left_click

            if game_map.walkable[destination_x, destination_y]:
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if move and GameStates.TARGETING:
            for entity in entities:
                if entity.name == 'Target Reticle':
                    dx, dy = move
                    destination_x = entity.x + dx
                    destination_y = entity.y + dy
                    if game_map.fov[destination_x, destination_y]:
                        entity.x = destination_x
                        entity.y = destination_y

        elif wait:
            game_state = GameStates.ENEMY_TURN

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity, constants['colors'])
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', constants['colors'].get('yellow')))

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, constants['colors'], entities=entities,
                                                                game_map=game_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item, constants['colors']))

        if escape_index is not None:
            pass

        if down_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    game_map, entities = next_floor(player, message_log, entity.stairs.floor, constants)
                    fov_recompute = True
                    con.clear()

                    break
            else:
                message_log.add_message(Message('There are no stairs here.', constants['colors'].get('yellow')))

        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            elif level_up == 'str':
                player.fighter.base_power += 1
            elif level_up == 'def':
                player.fighter.base_defense += 1

            game_state = previous_game_state

        if look:
            previous_game_state = game_state
            game_state = GameStates.LOOK

        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        if show_equipment_menu:
            previous_game_state = game_state
            game_state = GameStates.EQUIPMENT_MENU

        if show_keybindings_menu:
            game_state = GameStates.KEYBINDINGS_MENU

        if show_help_screen:
            game_state = GameStates.HELP_SCREEN

        if show_options_menu:
            game_state = GameStates.OPTIONS_MENU

        if show_dev_console and GameStates.PLAYERS_TURN:
            #previous_game_state = game_state
            game_state = GameStates.DEV_CONSOLE

        if equipment_index is not None and previous_game_state != GameStates.PLAYER_DEAD:
            if equipment_index == 0:
                equipment_selected = player.equipment.main_hand
            elif equipment_index == 1:
                equipment_selected = player.equipment.off_hand
            else:
                equipment_selected = None

            if game_state == GameStates.EQUIPMENT_MENU and equipment_selected is not None:
                player.inventory.add_item(equipment_selected, constants['colors'])
                player_turn_results.extend(player.equipment.toggle_equip(equipment_selected))

        if game_state == GameStates.TARGETING:
            if mouse_coordinates_changed and mouse_coordinates[0] < game_map.width and mouse_coordinates[1] < game_map.height:
                for entity in entities:
                    if entity.name == 'Target Reticle' and game_map.fov[mouse_coordinates]:
                        (entity.x, entity.y) = mouse_coordinates

        if left_click:
            if game_state == GameStates.TARGETING:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(targeting_item, constants['colors'], entities=entities,
                                                        game_map=game_map, target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
                
            elif game_state == GameStates.ESCAPE_MENU:
                target_x, target_y = left_click
                #22 top, 25 bottom
                if constants['screen_height'] == 50:
                    if target_y == 22:
                        game_state = GameStates.OPTIONS_MENU
                    elif target_y == 23:
                        game_state = GameStates.KEYBINDINGS_MENU
                    elif target_y == 24:
                        game_state = GameStates.HELP_SCREEN
                    elif target_y == 25:
                        exit = True
                else:
                    print('''MOUSE DISABLED: constants['screen_height'] changed''')

            elif game_state == GameStates.EQUIPMENT_MENU:
                target_x, target_y = left_click
                print_dev('{0}, {1}'.format(target_x, target_y), config)

            elif game_state == GameStates.SHOW_INVENTORY:
                #inventory adjusts, figure this out
                target_x, target_y = left_click
                print_dev('{0}, {1}'.format(target_x, target_y), config)

            elif game_state == GameStates.DROP_INVENTORY:
                #inventory adjusts, figure this out
                target_x, target_y = left_click
                print_dev('{0}, {1}'.format(target_x, target_y), config)

            elif game_state == GameStates.PLAYERS_TURN:
                target_x, target_y = left_click
                print_dev('{0}, {1}'.format(target_x, target_y), config)

            elif game_state == GameStates.OPTIONS_MENU:
                #update configs
                write_config(config)
                tdl.set_fps(int(config['fps_cap']))
                
                target_x, target_y = left_click
                print_dev('{0}, {1}'.format(target_x, target_y), config)
                if target_x < 51 and target_x > 25:
                    if target_y == 26:
                        if config['fps_display'] == 'False':
                            config['fps_display'] = 'True'
                        elif config['fps_display'] == 'True':
                            config['fps_display'] = 'False'
                    elif target_y == 27:
                        fps_cap = int(config['fps_cap']) + 5
                        if fps_cap > 200:
                            fps_cap = fps_cap - 200
                        config['fps_cap'] = str(fps_cap)
                    
        if right_click:
            if game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})

            elif game_state == GameStates.ESCAPE_MENU:
                return_to_game = True

            elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN, GameStates.EQUIPMENT_MENU,\
                          GameStates.OPTIONS_MENU, GameStates.KEYBINDINGS_MENU, GameStates.HELP_SCREEN):
                exit = True

        if return_to_game:
            if game_state == GameStates.ESCAPE_MENU:
                game_state = previous_game_state
            elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN, GameStates.EQUIPMENT_MENU):
                # menus
                game_state = previous_game_state
            elif game_state == GameStates.LOOK:
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            elif game_state == GameStates.DEV_CONSOLE:
                game_state = GameStates.PLAYERS_TURN
            elif game_state in (GameStates.KEYBINDINGS_MENU, GameStates.OPTIONS_MENU, GameStates.HELP_SCREEN):
                #for those that go to and from the Escape_Menu
                game_state = GameStates.ESCAPE_MENU
            else:
                previous_game_state = game_state
                game_state = GameStates.ESCAPE_MENU

        if message_log_up:
            message_log.index_message(1)
        if message_log_down:
            message_log.index_message(-1)

        if exit:
            if game_state == GameStates.ESCAPE_MENU:
                game_state = previous_game_state
                print_dev('\nBeginning save...', config)
                print_dev('player: '+str(player), config)
                print_dev('entities: '+str(entities), config)
                print_dev('game map: '+str(game_map), config)
                print_dev('message log: '+str(message_log), config)
                print_dev('game_state: '+str(game_state), config)
                save_game(player, entities, game_map, message_log, game_state, config)
                print_dev('==============\nSave complete!\n==============\n', config)
                return True
            else:
                previous_game_state = game_state
                game_state = GameStates.ESCAPE_MENU

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            equip = player_turn_result.get('equip')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            xp = player_turn_result.get('xp')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity, constants['colors'])
                    print('The game doesn\'t hate you, I hate you. My name is Tiberius Applesmith, and this is MY game.')
                else:
                    message = kill_monster(dead_entity, constants['colors'])

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                if game_state == GameStates.TARGETING:
                    for entity in entities:
                        if entity.name == 'Target Reticle':
                            entities.remove(entity)
                    
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)

                game_state = GameStates.ENEMY_TURN

            if equip:
                equip_results = player.equipment.toggle_equip(equip)

                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equipped:
                        player.inventory.remove_item(equipped)
                        message_log.add_message(Message('You equipped the {0}'.format(equipped.name)))

                    if dequipped:
                        player.inventory.add_item(dequipped, constants['colors'])
                        message_log.add_message(Message('You dequipped the {0}'.format(dequipped.name)))

                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                target_reticle = Entity(player.x, player.y, 'X', constants['colors'].get('yellow'), 'Target Reticle', render_order=RenderOrder.TARGETER,\
                              visible_time='blink_moderate')
                entities.append(target_reticle)

                message_log.add_message(targeting_item.item.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state

                for entity in entities:
                    if entity.name == 'Target Reticle':
                        entities.remove(entity)

                message_log.add_message(Message('Targeting cancelled'))

            if xp:
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(Message('You gain {0} experience points.'.format(xp)))

                if leveled_up:
                    message_log.add_message(Message(
                        'Your battle skills grow stronger! You reached level {0}'.format(
                            player.level.current_level) + '!',
                        constants['colors'].get('yellow')))
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity, constants['colors'])
                                print('The game doesn\'t hate you, I hate you. My name is Tiberius Applesmith, and this is MY game.')
                            else:
                                message = kill_monster(dead_entity, constants['colors'])

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN


def main():
    constants = get_constants()

    # magic config load sequence to load and repair bad configs
    config_dict = read_config()
    write_config(config_dict)
    config_dict = read_config() 

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    root_console = tdl.init(constants['screen_width'], constants['screen_height'], constants['window_title'])
    con = tdl.Console(constants['screen_width'], constants['screen_height'])
    panel = tdl.Console(constants['screen_width'], constants['panel_height'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False

    main_menu_background_image = image_load('menu_background.png')

    tdl.set_fps(int(config_dict['fps_cap'])) #Let's not be chrome

    while not tdl.event.is_window_closed():
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None

        if show_main_menu:
            main_menu(con, root_console, main_menu_background_image, constants['screen_width'],
                      constants['screen_height'], constants['colors'])

            if show_load_error_message:
                message_box(con, root_console, 'No save game to load', 50, constants['screen_width'],
                            constants['screen_height'])

            tdl.flush()

            action = handle_main_menu(user_input)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN

                show_main_menu = False
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state = load_game(config_dict)
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                write_config(config_dict)
                root_console.__del__() # this closes the console + garbage collects
                break

        else:
            root_console.clear()
            con.clear()
            panel.clear()
            play_game(player, entities, game_map, message_log, game_state, root_console, con, panel, constants, config_dict)

            show_main_menu = True


if __name__ == '__main__':
    main()
