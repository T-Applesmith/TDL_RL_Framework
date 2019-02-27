import json

from utils.map_utils import GameMap

from dev.dev_print import print_dev
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates

from components.level import Level

def save_game(player, entities, game_map, message_log, game_state, config):
    data = {
        'player_index': entities.index(player),
        'entities': [entity.to_json() for entity in entities],
        'game_map': game_map.to_json(),
        'message_log': message_log.to_json(),
        'game_state': game_state.value
    }

    print_dev('Saving to JSON', config)
    print_dev('data: '+str(data), config)
    with open('save_game.json', 'w') as save_file:
        json.dump(data, save_file, indent=4)
    print_dev('Saved to JSON', config)


def load_game(config):
    print_dev('Loading from JSON', config)
    with open('save_game.json') as save_file:
        data = json.load(save_file)

    player_index = data['player_index']
    entities_json = data['entities']
    game_map_json = data['game_map']
    message_log_json = data['message_log']
    game_state_json = data['game_state']

    entities = [Entity.from_json(entity_json) for entity_json in entities_json]
    player = entities[player_index]
    game_map = GameMap.from_json(game_map_json)
    message_log = MessageLog.from_json(message_log_json)
    game_state = GameStates(game_state_json)

    print_dev('Loading from JSON complete', config)
    return player, entities, game_map, message_log, game_state
