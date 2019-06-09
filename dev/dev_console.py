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


def dev_powers(string, entities, message_log, constants, config, game_vars):
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

    elif function.lower() in ['omniscient', 'omniscience'] and len(args) > 1:
        #View things out of sight
        if args[1].lower() in ['local']:
            game_vars['omniscience_local'] = not game_vars['omniscience_local']
        elif args[1].lower() in ['global']:
            game_vars['omniscience_global'] = not game_vars['omniscience_global']

        print_dev('DEV: toggled omniscience; local:{0} global:{1}'.format(game_vars['omniscience_local'], game_vars['omniscience_global']))
        message_log.add_message(Message('DEV: Your awareness of the world suddenly shifts.'))
        results = []

    elif function.lower() in ['spawn'] and len(args) > 3:
        from components.ai import BasicMonster
        from components.fighter import Fighter
        from components.item import Item
        from entity import Entity
        from render_functions import RenderOrder
        from item_functions import cast_fireball
        from utils.geometry_utils import Circle, Cone, Coordinate

        for entity in entities:
            if entity.name == 'Player':
                player = entity
        
        #create an object at a given location
        if args[1] == 'orc':
            fighter_component = Fighter(hp=20, defense=0, power=4, xp=35, fov_range=10, targets=[])
            ai_component = BasicMonster()

            monster = Entity(int(args[2]), int(args[3]), 'o', colors.get('desaturated_green'), 'Orc', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,\
                                 description="A fearsome orc")
            entities.append(monster)

        elif args[1] == 'scroll_fireball':
            item_component = Item(use_function=cast_fireball, targeting=True, targeting_structure=Circle(player.x, player.y, radius=2),\
                                  targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', colors.get('light_cyan')),\
                                  damage=25, radius=3)
            item = Entity(int(args[2]), int(args[3]), '#', colors.get('red'), 'Fireball Scroll', render_order=RenderOrder.ITEM,
                              item=item_component, description="A single-use item to damage entities nearby the blast")
            print('fireball: {0}'.format(item.item.targeting_structure.tiles))
            entities.append(item)
        

    return results                    

    
def find_target_location(string):
    x = string.replace('[', '')
    x = x.split(',', 1)[0]

    y = string.replace(']', '')
    y = y.split(',', 1)[1]

    return int(x), int(y)
