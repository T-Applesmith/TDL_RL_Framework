import tdl, tcod


from dev.dev_print import print_dev
from game_messages import Message
from item_functions import heal
from menus import menu


def dev_console(con, root_console, header, content, menu_width, menu_height, screen_width, screen_height, config):
    options = []
    
    window = tdl.Console(menu_width, menu_height)

    window.draw_rect(0, 0, menu_width, menu_height, None, fg=(255, 0, 255), bg=(80, 95, 115))
    window.draw_str(0, 0, '{0}{1}'.format(header, content))

    root_console.blit(window, 0, 0, menu_width, menu_height, 0, 0)


def dev_powers(string, entities, message_log, constants, config):
    '''
    This translates a 'string' provided by the dev_console into an action

    Heal - positive number heals target, negative damages
    Teleport - moves entity at A to B
    '''
    colors = constants['colors']
    results = []
    
    args = string.split()
    print('DEV_CONSOLE: {0}'.format(args))

    function = args[0]

    #Dev Powers
    print('{0}'.format(function.capitalize()))
    
    if function.lower() in ['heal']:
        #Heal/Damage Target
        target_x, target_y = find_target_location(args[1])
        heal_amount = int(args[2])

        for entity in entities:
            print('{0},{1} {2},{3}'.format(entity.x, entity.y, entity.x == target_x, entity.y == target_y))
            if entity.x == target_x and entity.y == target_y:
                print('DEV: Found TARGET')
                if heal_amount > 0:
                    results = heal(entity, colors, amount=heal_amount, dev=True)
                elif heal_amount < 0:
                    results = entity.fighter.take_damage(abs(heal_amount))

    elif function.lower() in ['teleport']:
        #Move Entities from Location A to B
        target_x1, target_y1 = find_target_location(args[1])
        target_x2, target_y2 = find_target_location(args[2])

        for entity in entities:
            if entity.x == target_x1 and entity.y == target_y1:
                entity.x = target_x2
                entity.y = target_y2

                print_dev('DEV: {0} has teleported to [{1},{2}].'.format(entity.name, target_x2, target_y2), config)
                message_log.add_message(Message('DEV: {0} has teleported to [{1},{2}].'.format(entity.name, target_x2, target_y2), constants['colors'].get('white')))
                results = []

    return results                    

    
def find_target_location(string):
    x = string.replace('[', '')
    x = x.split(',', 1)[0]

    y = string.replace(']', '')
    y = y.split(',', 1)[1]

    return int(x), int(y)
