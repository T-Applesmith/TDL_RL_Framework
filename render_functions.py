import math, time
import tdl

from dev.dev_console import dev_console
from enum import Enum
from game_states import GameStates
from menus import character_screen, inventory_menu, level_up_menu, equipment_menu, escape_menu, keybindings_screen,\
     help_screen, options_menu, fps_counter, look_box

from loader_functions.config_loaders import write_config


class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4
    TARGETER = 5


def get_names_under_mouse(mouse_coordinates, entities, game_map):
    x, y = mouse_coordinates

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and game_map.fov[entity.x, entity.y] and entity.name != 'Target Reticle']
    names = ', '.join(names)

    names = '[{0},{1}] {2}'.format(x, y, names)

    return names.capitalize()


def get_description_under_mouse(mouse_coordinates, entities, game_map):
    x, y = mouse_coordinates
    render_order_index = 4
    description = None

    while description == None and render_order_index > 0:
        render_order_enum = RenderOrder(render_order_index)
        #print('{0}'.format(render_order_enum))
        for entity in entities:
            if entity.x == x and entity.y == y and game_map.fov[entity.x, entity.y] and entity.render_order == render_order_enum:
                description = entity.description
                #print('Render Order: {0}'.format(entity.render_order))
        render_order_index -= 1
        
    print('Description: {0}'.format(description))
    return description
        


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color, string_color):
    # Render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # Render the background first
    panel.draw_rect(x, y, total_width, 1, None, bg=back_color)

    # Now render the bar on top
    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)

    # Finally, some centered text with the values
    text = name + ': ' + str(value) + '/' + str(maximum)
    x_centered = x + int((total_width-len(text)) / 2)

    panel.draw_str(x_centered, y, text, fg=string_color, bg=None)


def render_all(con, panel, entities, player, game_map, fov_recompute, root_console, message_log, mouse_coordinates,
               game_state, constants, config, dev_console_input, targeting_structure):
    screen_width = constants['screen_width']
    screen_height = constants['screen_height']
    bar_width = constants['bar_width']
    panel_height = constants['panel_height']
    panel_y = constants['panel_y']
    colors = constants['colors']
    
    # Draw all the tiles in the game map
    if fov_recompute:
        for x, y in game_map:
            wall = not game_map.transparent[x, y]

            if game_map.fov[x, y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('light_wall'))
                else:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('light_ground'))

                game_map.explored[x][y] = True
            elif game_map.explored[x][y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('dark_wall'))
                else:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('dark_ground'))
    
        if game_state == GameStates.TARGETING:
            #print('tiles:{0}'.format(targeting_structure.tiles))
            for x, y in game_map:
                '''
                if game_state == GameStates.TARGETING:# and targeting_structure:
                    #print('({0},{1}), tiles:{2}'.format(x, y, targeting_structure.tiles))
                    #if (x, y) in targeting_structure.tiles:

                    if targeting_structure.h == x and targeting_structure.k == y:
                        #print('(x,y) in targeting_structure.tiles')
                        con.draw_char(x, y, None, fg=None, bg=colors.get('dark_red'))
                        '''
                if (x, y) in targeting_structure.tiles:
                    color = con.get_char(x, y)[2]
                    color = (color[0]+80, color[1], color[2])
                    con.draw_char(x, y, None, fg=None, bg=color)

    # Draw all entities in the list
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    current_time = time.clock()
    
    for entity in entities_in_render_order:
        if not entity.visible_time:
            draw_entity(con, entity, game_map)
        elif entity.visible_time == 'blink_slow' and math.floor(current_time) % 2 == 0:
            draw_entity(con, entity, game_map)
        elif entity.visible_time == 'blink_moderate' and current_time - math.floor(current_time) >= .5:
            draw_entity(con, entity, game_map)
        elif entity.visible_time == 'blink_fast' and (2*current_time - math.floor(2*current_time)) >= .5:
            draw_entity(con, entity, game_map)

    con.draw_str(1, screen_height - 2, 'HP: {0:02}/{1:02}'.format(player.fighter.hp, player.fighter.max_hp))

    root_console.blit(con, 0, 0, screen_width, screen_height, 0, 0)

    panel.clear(fg=colors.get('white'), bg=colors.get('black'))

    # Print the game messages, one line at a time
    y = 1
    dy = 0
    for message in message_log.messages:
        #print('{0}:{1}'.format(y, message_log.index))
        if dy < 6 and (y >= message_log.index and message_log.index + 6 > y):
            panel.draw_str(message_log.x, dy, '{0}'.format(message.text), bg=None, fg=message.color)
            dy += 1
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               colors.get('light_red'), colors.get('darker_red'), colors.get('white'))

    panel.draw_str(1, 0, get_names_under_mouse(mouse_coordinates, entities, game_map))
    panel.draw_str(1, 3, 'Dungeon Level: {0}'.format(game_map.dungeon_level), fg=colors.get('white'), bg=None)

    root_console.blit(panel, 0, panel_y, screen_width, panel_height, 0, 0)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'

        inventory_menu(con, root_console, inventory_title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, root_console, 'Level up! Choose a stat to raise:', player, 40, screen_width,
                      screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(root_console, player, 30, 10, screen_width, screen_height)

    elif game_state == GameStates.EQUIPMENT_MENU:
        equipment_menu(con, root_console, 'Equipment', player, 30, screen_width, screen_height)

    elif game_state == GameStates.ESCAPE_MENU:
        escape_menu(root_console, 'ESCAPE MENU', 30, 10, screen_width, screen_height)

    elif game_state == GameStates.KEYBINDINGS_MENU:
        keybindings_screen(root_console, 'KEYBINDINGS (PROOF OF CONCEPT)', 50, 40, screen_width, screen_height, config)

    elif game_state == GameStates.OPTIONS_MENU:
        options_menu(root_console, 'OPTIONS (PROOF OF CONCEPT)', 30, 10, screen_width, screen_height, config)

    elif game_state == GameStates.HELP_SCREEN:
        help_screen(root_console, 'HELP (PROOF OF CONCEPT)', 60, 40, screen_width, screen_height)

    elif game_state == GameStates.DEV_CONSOLE:
        dev_console(con, root_console, '~:', dev_console_input, 60, 1, screen_width, screen_height, config)

    elif game_state == GameStates.LOOK:
        description = get_description_under_mouse(mouse_coordinates, entities, game_map)
        look_box(root_console, description, screen_width, screen_width, screen_height)
        
    if config['fps_display'] in ['True', 'TRUE', 'true']:
        fps_counter(root_console, constants['screen_width'])     


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, game_map):
    if game_map.fov[entity.x, entity.y] or (entity.stairs and game_map.explored[entity.x][entity.y]):
        con.draw_char(entity.x, entity.y, entity.char, entity.color, bg=None)


def clear_entity(con, entity):
    # erase the character that represents this object
    con.draw_char(entity.x, entity.y, ' ', entity.color, bg=None)
