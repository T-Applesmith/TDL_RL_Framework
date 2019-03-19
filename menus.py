import tdl

import textwrap


def menu(con, root, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after textwrap)
    header_wrapped = textwrap.wrap(header, width)
    header_height = len(header_wrapped)

    # calculate total height of the options (after textwrap)
    option_height = 0
    #for option in options:
    #    option_wrapped = textwrap.wrap(option, width)
    #    option_height += len(option_wrapped)
    option_height = len(options)

    # calculate total height of the menu
    height = option_height + header_height

    # create an off-screen console that represents the menu's window
    window = tdl.Console(width, height)

    # print the header, with wrapped text
    window.draw_rect(0, 0, width, height, None, fg=(255, 255, 255), bg=None)
    for i, line in enumerate(header_wrapped):
        window.draw_str(0, 0 + i, header_wrapped[i])

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text

        # if option is too long, wrap it
        #option_wrapped = textwrap.wrap(option_text, width)
        #for i, line in enumerate(option_wrapped):
        #    window.draw_str(0, y, option_wrapped[i])
        #    y += 1

        #if option is too long, truncate it
        loop_str_print_exception = True
        while(loop_str_print_exception):
            loop_str_print_exception = False
            try:
                window.draw_str(0, y, text, bg=None)
            except tdl.TDLError as err:
                print("tdl.TDLError: {0}: {1}".format(err, text))
                loop_str_print_exception = True
                text_len = len(text)
                text = text[:text_len-1]
                pass
            
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = screen_width // 2 - width // 2
    y = screen_height // 2 - height // 2
    root.blit(window, x, y, width, height, 0, 0)


def inventory_menu(con, root, header, player, inventory_width, screen_width, screen_height):
    # show a menu with each item of the inventory as an option
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            #Mostly vestigal, going to keep to the next clean-up
            if player.equipment:
                if player.equipment.main_hand:
                    if player.equipment.main_hand == item:
                        options.append('{0} (on main hand)'.format(item.name))
                    else:
                        #options.append('{0} (BUG: on main hand)'.format(item.name))
                        #options.append('{0} (BUG: attempted to be on main hand)'.format(item.name))
                        options.append('{0}'.format(item.name))
                elif player.equipment.off_hand:
                    if player.equipment.off_hand == item:
                        options.append('{0} (on off hand)'.format(item.name))
                    else:
                        #options.append('{0} (BUG: offhand)'.format(item.name))
                        #options.append('{0} (BUG: attempted to be on off hand)'.format(item.name))
                        options.append('{0}'.format(item.name))
                else:
                    options.append(item.name)
            else:
                #print(']nREPORT\nplayer.equipment: {0}'.format(player.equipment))
                print('FATAL BUG: inventory_menu, no player.equipment found')
                pass
                                
    menu(con, root, header, options, inventory_width, screen_width, screen_height)


def equipment_menu(con, root, header, player, equipment_width, screen_width, screen_height):
    # show a menu with currently equipped items
    options = []

    if player.equipment:
        if player.equipment.main_hand:
            options.append('main hand: {0}'.format(player.equipment.main_hand.name))
        else:
            options.append('main hand: (empty)')

        if player.equipment.off_hand:
                options.append('off hand: {0}'.format(player.equipment.off_hand.name))
        else:
            options.append('off hand: (empty)')
    else:
        #print('\nREPORT\nplayer.equipment: {0}'.format(player.equipment))
        #print('FATAL BUG: equipment_menu, no player.equipment found')
        pass
        
    menu(con, root, header, options, equipment_width, screen_width, screen_height)
            


def main_menu(con, root_console, background_image, screen_width, screen_height, colors):
    background_image.blit_2x(root_console, 0, 0)

    title = 'TOMBS OF THE ANCIENT TUTORIAL'
    center = (screen_width - len(title)) // 2
    root_console.draw_str(center, screen_height // 2 - 4, title, bg=None, fg=colors.get('light_yellow'))

    title = 'By TApplesmith'
    center = (screen_width - len(title)) // 2
    root_console.draw_str(center, screen_height - 2, title, bg=None, fg=colors.get('light_yellow'))

    menu(con, root_console, '', ['Play a new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height)


def level_up_menu(con, root, header, player, menu_width, screen_width, screen_height):
    options = ['Constitution (+20 HP, from {0})'.format(player.fighter.max_hp),
               'Strength (+1 attack, from {0})'.format(player.fighter.power),
               'Agility (+1 defense, from {0})'.format(player.fighter.defense)]

    menu(con, root, header, options, menu_width, screen_width, screen_height)


def character_screen(root_console, player, character_screen_width, character_screen_height, screen_width,
                     screen_height):
    window = tdl.Console(character_screen_width, character_screen_height)

    window.draw_rect(0, 0, character_screen_width, character_screen_height, None, fg=(255, 255, 255), bg=None)

    character_screen_array = ['Character Information', 'Level: {0}'.format(player.level.current_level),\
    'Experience: {0}'.format(player.level.current_xp),'Experience to Level: {0}'.format(player.level.experience_to_next_level),\
    'Maximum HP: {0}'.format(player.fighter.max_hp), 'Attack: {0}'.format(player.fighter.power),\
    'Defense: {0}'.format(player.fighter.defense)]
    menu_text(window, 0, 1, character_screen_height, character_screen_array)

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    root_console.blit(window, x, y, character_screen_width, character_screen_height, 0, 0)


def keybindings_screen(root_console, header, menu_width, menu_height, screen_width, screen_height, config):
    import tdl

    window = tdl.Console(menu_width, menu_height)
    
    window.draw_rect(0, 0, menu_width, menu_height, None, fg=(255, 255, 255), bg=None)
    window.draw_str(0, 0, '{0}'.format(header))

    if config['allow_keybinding'] in ['True', 'TRUE']:
        keybindings_rebind_list(window, menu_height, config)
    elif config['allow_keybinding'] in ['False', 'FALSE']:
        keybindings_full_uninteractive_list(window, menu_height)

    x = screen_width // 2 - menu_width // 2
    y = screen_height // 2 - menu_height // 2
    root_console.blit(window, x, y, menu_width, menu_height, 0, 0)

def keybindings_rebind_list(window, menu_height, config):
    keybinding_screen_array = ['Movement',\
                               '   wait:        {0}'.format(config['key_wait']),\
                               '   north:       {0}'.format(config['key_north']),\
                               '   northeast:   {0}'.format(config['key_northeast']),\
                               '   east:        {0}'.format(config['key_east']),\
                               '   southeast:   {0}'.format(config['key_southeast']),\
                               '   south:       {0}'.format(config['key_south']),\
                               '   southwest:   {0}'.format(config['key_southwest']),\
                               '   west:        {0}'.format(config['key_west']),\
                               '   northwest:   {0}'.format(config['key_northwest']),\
                               'Actions',\
                               '   pickup item: {0}'.format(config['key_pickup']),\
                               '   drop item:   {0}'.format(config['key_drop']),\
                               'Menus',\
                               '   inventory:   {0}'.format(config['key_inventory']),\
                               '   character:   {0}'.format(config['key_character_menu']),\
                               '   equipment:   {0}'.format(config['key_equipment']),\
                               '   help:        {0}'.format(config['key_help']),\
                               'Interface (Unbindable)',\
                               '   return/escape: ESC',\
                               '   scroll log:    mousewheel up/down',\
                               '   fullscrren:    alt+Enter']
    menu_text(window, 0, 1, menu_height, keybinding_screen_array)
    
def keybindings_full_uninteractive_list(window, menu_height):
    """Lists typical key inputs and their default bindings"""
    from input_handlers import handle_player_turn_keys
    
    action_number = 2
    #space? starts at 32
    for i in range(32, 126):
        event = tdl.event.KeyDown(key=chr(i),char=chr(i))
        action = handle_player_turn_keys(event)
        if action:
            window.draw_str(0, action_number, chr(i) +' '+ str(action))
            action_number += 1

        if action_number >= menu_height:
            break


def escape_menu(root_console, header, menu_width, menu_height, screen_width, screen_height):
    window = tdl.Console(menu_width, menu_height)

    window.draw_rect(0, 0, menu_width, menu_height, None, fg=(255, 255, 255), bg=None)

    escape_array = ['{0}'.format(header), '(O)ptions', '(K)eybindings', '(H)elp', '(S)ave & Quit']
    menu_text(window, 0, 1, menu_height, escape_array)

    x = screen_width // 2 - menu_width // 2
    y = screen_height // 2 - menu_height // 2
    root_console.blit(window, x, y, menu_width, menu_height, 0, 0)


def options_menu(root_console, header, menu_width, menu_height, screen_width, screen_height, config):
    window = tdl.Console(menu_width, menu_height)

    window.draw_rect(0, 0, menu_width, menu_height, None, fg=(255, 255, 255), bg=None)

    options_array = ['{0}'.format(header), 'This is where', 'my options would be', 'if I HAD ANY!',\
                     'Master Volume: \N{INFINITY}', 'Display FPS: {0}'.format(config['fps_display']),\
                     'FPS Cap: {0}'.format(config['fps_cap'])]
    menu_text(window, 0, 1, menu_height, options_array)

    x = screen_width // 2 - menu_width // 2
    y = screen_height // 2 - menu_height // 2
    root_console.blit(window, x, y, menu_width, menu_height, 0, 0)


def help_screen(root_console, header, menu_width, menu_height, screen_width, screen_height):
    window = tdl.Console(menu_width, menu_height)

    window.draw_rect(0, 0, menu_width, menu_height, None, fg=(255, 255, 255), bg=None)

    help_screen_array = ['{0}'.format(header),\
                         'Press keys in [] or in () to select that option within menus.',\
                         'Press [Esc] to pause the game and access other menus,',\
                         '   or to quickly exit menus.',\
                         'The Keybindings Menu shows available actions during gameplay.',\
                         '   (It will be cleaned up in the future)',\
                         '   move {1, 0} means move right one and up zero.',\
                         'Walk into enimies to attack with your weapon.'] 
                         
    menu_text(window, 0, 1, menu_height, help_screen_array)

    x = screen_width // 2 - menu_width // 2
    y = screen_height // 2 - menu_height // 2
    root_console.blit(window, x, y, menu_width, menu_height, 0, 0)


def fps_counter(root_console, screen_width):
    width = 8
    height = 1
    window = tdl.Console(width, height)
    window.draw_str(0, 0, 'fps:{0}'.format(tdl.get_fps()))
    root_console.blit(window, screen_width-7, 0, width, height, 0, 0)
    


def message_box(con, root_console, header, width, screen_width, screen_height):
    menu(con, root_console, header, [], width, screen_width, screen_height)


def menu_text(window, x, y, menu_height, text_array, truncation=True, tab_when_wrapped=False,
                             justification='Left'):
    for text in text_array:
        if y < menu_height:
            
            if truncation:
                # if text is too long, truncate it
                loop_str_print_exception = True
                while(loop_str_print_exception):
                    loop_str_print_exception = False
                    
                    try:
                        
                        if justification == 'Left':
                            window.draw_str(x, y, text, bg=None)
                        if justification == 'Center':
                            pass
                        if justification == 'Right':
                            pass
                        
                    except tdl.TDLError as err:
                        # this is the bit that truncates
                        print("tdl.TDLError: {0}: {1}".format(err, text))
                        loop_str_print_exception = True
                        text_len = len(text)
                        text = text[:text_len-1]
                        pass
            else:
                # if text is too long, wrap it
                pass
            
            #window.draw_str(x, y, text)
            y+=1
