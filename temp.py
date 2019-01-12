import json
from components.level import Level

test = Level()

#    data = {
#        'player_index': entities.index(player),
#        'entities': [entity.to_json() for entity in entities],
#        'game_map': game_map.to_json(),
#        'message_log': message_log.to_json(),
#        'game_state': game_state.value
#    }
#
#    with open('save_game.json', 'w') as save_file:
 #       json.dump(data, save_file, indent=4)

data0 = {
    'level': test.to_json()
    }
with open('testing_save.json', 'w') as save_file0:
    json.dump(data0, save_file0, indent = 4)

print('Save Successful')

with open('testing_save.json') as save_file1:
        json_data1 = json.load(save_file1)

print(str(json_data1))

level_load = json_data1.get('level')
print('\nlevel: ' + str(level_load))
current_level = json_data1.get('current_level')
print('current_level: ' + str(current_level))
current_xp = json_data1.get('current_xp')
print('current_xp: ' + str(current_xp))
level_up_base = json_data1.get('level_up_base')
print('level_up_base: ' + str(level_up_base))
level_up_factor = json_data1.get('level_up_factor')
print('level_up_factor: ' + str(level_up_factor) +'\n')

print('current_level: ' + str(level_load.get('current_level')))
print('current_xp: ' + str(level_load.get('current_xp')))
print('level_up_base: ' + str(level_load.get('level_up_base')))
print('Load Sucessful')
