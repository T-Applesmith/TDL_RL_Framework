from tdl.map import Map

from random import randint

from components.ai import BasicMonster
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs

import utils.geometry_utils
from utils.geometry_utils import Rect, Coordinate, Cone
from utils.random_utils import from_dungeon_level, random_choice_from_dict

from entity import Entity
from game_messages import Message
from item_functions import cast_confuse, cast_fireball, cast_lightning, heal
from render_functions import RenderOrder


class GameMap(Map):
    def __init__(self, width, height, dungeon_level=1):
        super().__init__(width, height)
        self.explored = [[False for y in range(height)] for x in range(width)]

        self.dungeon_level = dungeon_level

    def to_json(self):
        print('saving game map')
        walkable = []
        transparent = []

        for y in range(self.height):
            walkable_row = []
            transparent_row = []

            for x in range(self.width):
                if self.walkable[x, y]:
                    walkable_value = True
                else:
                    walkable_value = False

                if self.transparent[x, y]:
                    transparent_value = True
                else:
                    transparent_value = False

                walkable_row.append(walkable_value)
                transparent_row.append(transparent_value)

            walkable.append(walkable_row)
            transparent.append(transparent_row)

        json_data = {
            'width': self.width,
            'height': self.height,
            'explored': self.explored,
            'walkable': walkable,
            'transparent': transparent
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        width = json_data.get('width')
        height = json_data.get('height')
        explored = json_data.get('explored')
        walkable = json_data.get('walkable')
        transparent = json_data.get('transparent')

        game_map = GameMap(width, height)
        game_map.explored = explored

        for y in range(height):
            for x in range(width):
                game_map.walkable[x, y] = walkable[y][x]
                game_map.transparent[x, y] = transparent[y][x]

        return game_map


class Previous_Game_Map:
    def __init__(self, game_map, entities):
        self.game_map = game_map
        self.entities = entities
        self.dungeon_level = game_map.dungeon_level

    def to_json(self):
        json_data = {
            'game_map': self.game_map.to_json(),
            'entities': [entity.to_json() for entity in self.entities],
            'dungeon_level': self.dungeon_level
        }

        return json_data

    def from_json(json_data):
        game_map_json = json_data.get('game_map')
        entities_json = json_data.get('entities')

        game_map = GameMap.from_json(game_map_json)
        entities = [Entity.from_json(entity_json) for entity_json in entities_json]

        previous_game_map = Previous_Game_Map(game_map, entities)
        return previous_game_map


def create_room(game_map, room):
    # go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            game_map.walkable[x, y] = True
            game_map.transparent[x, y] = True


def create_h_tunnel(game_map, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True


def create_v_tunnel(game_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True


def place_entities(room, entities, dungeon_level, colors):
    max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], dungeon_level)
    max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], dungeon_level)

    # Get a random number of monsters
    number_of_monsters = randint(0, max_monsters_per_room)
    number_of_items = randint(0, max_items_per_room)

    monster_chances = {
        'orc': 80,
        'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], dungeon_level)
    }

    item_chances = {
        'healing_potion': 35,
        'sword': from_dungeon_level([[5, 4]], dungeon_level),
        'shield': from_dungeon_level([[15, 8]], dungeon_level),
        'lightning_scroll': from_dungeon_level([[25, 4]], dungeon_level),
        'fireball_scroll': from_dungeon_level([[25, 6]], dungeon_level),
        'confusion_scroll': from_dungeon_level([[10, 2]], dungeon_level)
    }

    for i in range(number_of_monsters):
        # Choose a random location in the room
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            monster_choice = random_choice_from_dict(monster_chances)

            if monster_choice == 'orc':
                fighter_component = Fighter(hp=20, defense=0, power=4, xp=35, fov_range=15, targets=[])
                ai_component = BasicMonster()

                monster = Entity(x, y, 'o', colors.get('desaturated_green'), 'Orc', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,\
                                 description="A fearsome orc")
            else:
                fighter_component = Fighter(hp=30, defense=2, power=8, xp=100, fov_range=7, targets=[])
                ai_component = BasicMonster()

                monster = Entity(x, y, 'T', colors.get('darker_green'), 'Troll', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,\
                                 description="A terrifying troll")

            entities.append(monster)

    for i in range(number_of_items):
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            item_choice = random_choice_from_dict(item_chances)

            if item_choice == 'healing_potion':
                item_component = Item(use_function=heal, amount=40)
                item = Entity(x, y, '!', colors.get('violet'), 'Healing Potion', render_order=RenderOrder.ITEM,
                              item=item_component, description="A single-use item to remove some of your wounds")
            elif item_choice == 'sword':
                equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
                item = Entity(x, y, '/', colors.get('sky'), 'Sword', equippable=equippable_component,\
                              description="An equippable item that moderately increases your attack")
            elif item_choice == 'shield':
                equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
                item = Entity(x, y, '[', colors.get('darker_orange'), 'Shield', equippable=equippable_component,\
                              description="An equippable item that increases your agility")
            elif item_choice == 'fireball_scroll':
                item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                    'Left-click a target tile for the fireball, or right-click to cancel.', colors.get('light_cyan')),
                                      damage=25, radius=3)
                item = Entity(x, y, '#', colors.get('red'), 'Fireball Scroll', render_order=RenderOrder.ITEM,
                              item=item_component, description="A single-use item to damage entities nearby the blast")
            elif item_choice == 'confusion_scroll':
                item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(\
                    'Left-click an enemy to confuse it, or right-click to cancel.', colors.get('light_cyan')),\
                                      targeting_structure=Coordinate(0,0))
                item = Entity(x, y, '#', colors.get('light_pink'), 'Confusion Scroll', render_order=RenderOrder.ITEM,\
                              item=item_component, description="A single-use item that causes an entity to be confused")
            else:
                item_component = Item(use_function=cast_lightning, damage=20, maximum_range=5)
                item = Entity(x, y, '#', colors.get('yellow'), 'Lightning Scroll', render_order=RenderOrder.ITEM,
                              item=item_component, description="A single-use item that damages the nearest enemy")

            entities.append(item)


def make_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, colors, direction='down'):
    rooms = []
    num_rooms = 0

    center_of_last_room_x = None
    center_of_last_room_y = None

    for r in range(max_rooms):
        # random width and height
        w = randint(room_min_size, room_max_size)
        h = randint(room_min_size, room_max_size)
        # random position without going out of the boundaries of the map
        x = randint(0, map_width - w - 1)
        y = randint(0, map_height - h - 1)

        # "Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)

        # run through the other rooms and see if they intersect with this one
        for other_room in rooms:
            if new_room.intersect(other_room):
                break
        else:
            # this means there are no intersections, so this room is valid

            # "paint" it to the map's tiles
            create_room(game_map, new_room)

            # center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center()

            center_of_last_room_x = new_x
            center_of_last_room_y = new_y

            if num_rooms == 0:
                # this is the first room, where the player starts at
                player.x = new_x
                player.y = new_y
            else:
                # all rooms after the first:
                # connect it to the previous room with a tunnel

                # center coordinates of previous room
                (prev_x, prev_y) = rooms[num_rooms - 1].center()

                # flip a coin (random number that is either 0 or 1)
                if randint(0, 1) == 1:
                    # first move horizontally, then vertically
                    create_h_tunnel(game_map, prev_x, new_x, prev_y)
                    create_v_tunnel(game_map, prev_y, new_y, new_x)
                else:
                    # first move vertically, then horizontally
                    create_v_tunnel(game_map, prev_y, new_y, prev_x)
                    create_h_tunnel(game_map, prev_x, new_x, new_y)

            place_entities(new_room, entities, game_map.dungeon_level, colors)

            # finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1

    if direction == 'down':
        down_stairs_x = center_of_last_room_x
        down_stairs_y = center_of_last_room_y
        up_stairs_x = player.x
        up_stairs_y = player.y
    elif direction == 'up':
        down_stairs_x = player.x
        down_stairs_y = player.y
        up_stairs_x = center_of_last_room_x
        up_stairs_y = center_of_last_room_y

    stairs_component_down = Stairs(game_map.dungeon_level + 1)
    down_stairs = Entity(down_stairs_x, down_stairs_y, '>', (255, 255, 255), 'Stairs Down',
                         render_order=RenderOrder.STAIRS, stairs=stairs_component_down)
    entities.append(down_stairs)

    if game_map.dungeon_level - 1 > 0:
        stairs_component_up = Stairs(game_map.dungeon_level - 1)
        up_stairs = Entity(up_stairs_x, up_stairs_y, '<', (255, 255, 255), 'Stairs Up', render_order=RenderOrder.STAIRS,\
                           stairs=stairs_component_up)
        entities.append(up_stairs)
    

def next_floor(previous_game_maps, game_map, entities, player, message_log, dungeon_level, constants):
    #Save previous map
    previous_map = Previous_Game_Map(game_map, entities)
    if previous_game_maps:
        previous_game_maps.append(previous_map)
    else:
        previous_game_maps = [previous_map]

    #Check if map is made, checkout it if true
    map_already_made = None
    for previous_map in previous_game_maps:
        if dungeon_level == previous_map.dungeon_level:
            map_already_made = previous_map
            previous_game_maps.remove(map_already_made)
            break

    if map_already_made:
        game_map = map_already_made.game_map
        entities = map_already_made.entities

        for entity in entities:
                if entity.stairs and entity.name == 'Stairs Up':
                    player.x = entity.x
                    player.y = entity.y
                    
    else:
        #Create new map
        game_map = GameMap(constants['map_width'], constants['map_height'], dungeon_level)
        entities = [player]

        make_map(game_map, constants['max_rooms'], constants['room_min_size'],
                 constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities,
                 constants['colors'], direction='down')

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.',\
                                        constants['colors'].get('light_violet')))

    return game_map, entities, previous_game_maps, player

def previous_floor(previous_game_maps, game_map, entities, player, message_log, dungeon_level, constants):
    '''
    possibly consolidate into next_floor, as current only difference is direction of movement
    '''
    
    #Save previous map
    previous_map = Previous_Game_Map(game_map, entities)
    if previous_game_maps:
        previous_game_maps.append(previous_map)
    else:
        previous_game_maps = [previous_map]

    #Check if map is made, checkout it if true
    map_already_made = None
    for previous_map in previous_game_maps:
        if dungeon_level == previous_map.dungeon_level:
            map_already_made = previous_map
            previous_game_maps.remove(map_already_made)
            break

    if map_already_made:
        game_map = map_already_made.game_map
        entities = map_already_made.entities

        for entity in entities:
                if entity.stairs and entity.name == 'Stairs Down':
                    player.x = entity.x
                    player.y = entity.y
                    
    else:
        #Create new map
        game_map = GameMap(constants['map_width'], constants['map_height'], dungeon_level)
        entities = [player]

        make_map(game_map, constants['max_rooms'], constants['room_min_size'],
                 constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities,
                 constants['colors'], direction='up')

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.',\
                                        constants['colors'].get('light_violet')))

    return game_map, entities, previous_game_maps, player
