import math
import random

import tcod

from components.ai import BasicMonster, ConfusedMonster
from components.equipment import Equipment
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.inventory import Inventory
from components.level import Level
from components.stairs import Stairs

from render_functions import RenderOrder


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None,
                 item=None, inventory=None, stairs=None, level=None, equipment=None, equippable=None, description=None,\
                 visible_time=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        self.equipment = equipment
        self.equippable = equippable
        self.description = description
        self.visible_time = visible_time

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.level:
            self.level.owner = self

        if self.equipment:
            self.equipment.owner = self

        if self.equippable:
            self.equippable.owner = self

            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

    #@classmethod
    def entity_init_from_dict(dictionary):
        print('dictionary: '+str(dictionary))
        x = dictionary.get('x')
        y = dictionary.get('y')
        char = dictionary.get('char')
        color = dictionary.get('color')
        name = dictionary.get('name')
        #entity = Entity(dictonary.get('x'), dictonary.get('y'), '@', (255,255,255), 'If you can see this, entity_init_from_dict broke')
        entity = Entity(x, y, char, color, name)

        for key, value in dictionary.items():
            entity.key = value

        print('ENTITY_INIT_FROM_DICT: '+str(entity.__dict__))
        return entity

    def to_json(self):
        print('saving entity: '+str(self.name))
        if self.fighter:
            fighter_data = self.fighter.to_json()
        else:
            fighter_data = None

        if self.ai:
            ai_data = self.ai.to_json()
        else:
            ai_data = None

        if self.item:
            item_data = self.item.to_json()
        else:
            item_data = None

        if self.inventory:
            inventory_data = self.inventory.to_json()
        else:
            inventory_data = None

        if self.stairs:
            stairs_data = self.stairs.to_json()
        else:
            stairs_data = None

        if self.level:
            level_data = self.level.to_json()          
        else:
            level_data = None

        if self.equipment:
            print('equipment: '+str(self.equipment.__dict__))
            equipment_data = self.equipment.to_json()
        else:
            equipment_data = None

        if self.equippable:
            print('entity>equippable: '+str(self.name)+': '+str(self.equippable))
            equippable_data = self.equippable.to_json()
        else:
            equippable_data = None

        json_data = {
            'x': self.x,
            'y': self.y,
            'char': self.char,
            'color': self.color,
            'name': self.name,
            'blocks': self.blocks,
            'render_order': self.render_order.value,
            'fighter': fighter_data,
            'ai': ai_data,
            'item': item_data,
            'inventory': inventory_data,
            'stairs': stairs_data,
            'level': level_data,
            'equipment': equipment_data,
            'equippable': equippable_data,
            'description': self.description,
            'visible_time': self.visible_time
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        x = json_data.get('x')
        y = json_data.get('y')
        char = json_data.get('char')
        color = json_data.get('color')
        name = json_data.get('name')
        blocks = json_data.get('blocks')
        render_order = RenderOrder(json_data.get('render_order'))
        fighter_json = json_data.get('fighter')
        ai_json = json_data.get('ai')
        item_json = json_data.get('item')
        inventory_json = json_data.get('inventory')
        stairs_json = json_data.get('stairs')
        level_json = json_data.get('level')
        equipment_json = json_data.get('equipment')
        equippable_json = json_data.get('equippable')
        description = json_data.get('description')
        visible_time = json_data.get('visible_time')

        entity = Entity(x, y, char, color, name, blocks, render_order, description=description, visible_time=visible_time)

        if fighter_json:
            entity.fighter = Fighter.from_json(fighter_json)
            entity.fighter.owner = entity

        if ai_json:
            name = ai_json.get('name')

            if name == BasicMonster.__name__:
                ai = BasicMonster.from_json()
            elif name == ConfusedMonster.__name__:
                ai = ConfusedMonster.from_json(ai_json, entity)
            else:
                ai = None

            if ai:
                entity.ai = ai
                entity.ai.owner = entity

        if item_json:
            entity.item = Item.from_json(item_json)
            entity.item.owner = entity

        if inventory_json:
            entity.inventory = Inventory.from_json(inventory_json)
            entity.inventory.owner = entity

        if level_json:
            entity.level = Level.from_json(level_json)
            print('level.from_json: '+str(Level.to_json(entity.level)))
            entity.level.owner = entity

        if stairs_json:
            entity.stairs = Stairs.from_json(stairs_json)
            entity.stairs.owner = entity

        if equipment_json:
            entity.equipment = Equipment.from_json(equipment_json)
            entity.equipment.owner = entity

        if equippable_json:
            entity.equippable = Equippable.from_json(equippable_json)
            print('equippable.from_json: ' + str(entity))
            entity.equippable.owner = entity

        return entity


    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy
        

    def move_towards(self, game_map, entities, **kwargs):
        self.move_astar(game_map, entities, **kwargs)
        

    def move_backup(self, game_map, entities, **kwargs):
        '''
        Backup plan if a* fails due to distance constrants or otherwise
        Is not perfect, but handles situations where a* fails well enough to not currently be an issue
        '''
        target_x = kwargs.get('target_x')
        target_y = kwargs.get('target_y')
        walkable_map = game_map

        path = walkable_map.compute_path(self.x, self.y, target_x, target_y)

        if path:
            dx = path[0][0] - self.x
            dy = path[0][1] - self.y

            if walkable_map.walkable[path[0][0], path[0][1]]:
                #prep for strafing
                strafe_direction = random.choice([1, -1])
                
                #move into path if nothing is blocking
                if not get_blocking_entities_at_location(entities, self.x + dx, self.y + dy):
                    self.move(dx, dy)

                #horizontal - strafe into path if nothing is blocking
                elif dx == 0 or dy == 0:
                    if dx == 0:
                        if not get_blocking_entities_at_location(entities, self.x + strafe_direction, self.y + dy) and walkable_map.walkable[self.x + strafe_direction, self.y + dy]:
                            self.move(strafe_direction, dy)
                        elif not get_blocking_entities_at_location(entities, self.x - strafe_direction, self.y + dy) and walkable_map.walkable[self.x - strafe_direction, self.y + dy]:
                            self.move(-strafe_direction, dy)
                    if dy == 0:
                        if not get_blocking_entities_at_location(entities, self.x + dx, self.y + strafe_direction) and walkable_map.walkable[self.x + dx, self.y + strafe_direction]:
                            self.move(dx, strafe_direction)
                        elif not get_blocking_entities_at_location(entities, self.x + dx, self.y - strafe_direction) and walkable_map.walkable[self.x + dx, self.y - strafe_direction]:
                            self.move(dx, -strafe_direction)

                #corner - strafe into path if nothing is blocking
                elif abs(dx) == 1 and abs(dy) == 1:
                    #strafe x first
                    if strafe_direction > 0:
                        if not get_blocking_entities_at_location(entities, self.x, self.y + dy) and walkable_map.walkable[self.x, self.y + dy]:
                            self.move(0, dy)
                        elif not get_blocking_entities_at_location(entities, self.x + dx, self.y) and walkable_map.walkable[self.x + dx, self.y]:
                            self.move(dx, 0)
                    #strafe y first
                    elif strafe_direction < 0:
                        if not get_blocking_entities_at_location(entities, self.x + dx, self.y) and walkable_map.walkable[self.x + dx, self.y]:
                            self.move(dx, 0)
                        elif not get_blocking_entities_at_location(entities, self.x, self.y + dy) and walkable_map.walkable[self.x, self.y + dy]:
                            self.move(0, dy)


    def move_astar(self, game_map, entities, **kwargs):#self, target_x, target_y, game_map, entities):
        MAP_WIDTH = game_map.width
        MAP_HEIGHT = game_map.height
        fov = tcod.map_new(MAP_WIDTH, MAP_HEIGHT)

        target = kwargs.get('target')
        if target:
            target_x = target.x
            target_y = target.y
        else:
            target_x = kwargs.get('target_x')
            target_y = kwargs.get('target_y')

        #pre A* movement to slightly improve cpu time
        if self.x == target_x:
            if move_cardinal_y(self, target_y, game_map):
                self.move_backup(game_map, entities, target_x=target_x, target_y=target_y)
                #print('Walking North/South')
     
        elif self.y == target_y:
            if move_cardinal_x(self, target_x, game_map):
                self.move_backup(game_map, entities, target_x=target_x, target_y=target_y)
                #print('Walking East/West')

        else:
            #pre A* calculations
            for y1 in range(MAP_HEIGHT):
                for x1 in range(MAP_WIDTH):
                    tcod.map_set_properties(fov, x1, y1, game_map.transparent[x1][y1], game_map.walkable[x1][y1])

            for entity in entities:
                if entity.blocks and entity != self and entity != target:
                    tcod.map_set_properties(fov, entity.x, entity.y, True, False)

            my_path = tcod.path_new_using_map(fov, 1.41)

            tcod.path_compute(my_path, self.x, self.y, target_x, target_y)
            
            if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
                # A* for general use
                x, y = tcod.path_walk(my_path, True)
                if x or y:
                    self.x = x
                    self.y = y

            else:
                # if no paths, use old method
                # typically used due to path size >= 25
                # noticed that path is sometimes zero - but there is an alternate path? -no issues yet but keep in mind
                # possibly due to fov? - just a hunch
                #print('Cannot A*, using backup pathing algo, path distance: {0}'.format(tcod.path_size(my_path)))
                self.move_backup(game_map, entities, target_x=target_x, target_y=target_y)

            # free up memory
            tcod.path_delete(my_path)


    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)


    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
    



def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None

def move_cardinal_x(self, target_x, game_map):
    walkable = True
    walk = self.x
    x = target_x - self.x
    direction = int(x>0) - int(x<0)

    while walk != target_x:
        walk += direction
        if not (game_map.transparent[walk][self.y] and game_map.walkable[walk][self.y]):
            walkable = False

    return walkable

def move_cardinal_y(self, target_y, game_map):
    walkable = True
    walk = self.y
    y = target_y - self.y
    direction = int(y>0) - int(y<0)

    while walk != target_y:
        walk += direction
        if not (game_map.transparent[self.x][walk] and game_map.walkable[self.x][walk]):
            walkable = False

    return walkable
