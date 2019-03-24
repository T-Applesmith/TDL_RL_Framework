from random import randint

from game_messages import Message
from components.target_entity import Target_Entity


class BasicMonster:
    def take_turn(self, target, game_map, entities):
        results = []

        monster = self.owner

        if game_map.fov[monster.x, monster.y]:
            print('Player within FOV')
            # add target to list of targets if not already
            target_in_targets = False
            for monster_target in monster.fighter.targets:
                if entities.index(target) == monster_target.entity_index:
                    monster_target.update_location(target.x, target.y)
                    target_in_targets = True
                    break

            # otherwise update location
            if not target_in_targets:
                monster.fighter.targets.append(Target_Entity(entities.index(target), target.x, target.y))

            # move to location
            if monster.distance_to(target) >= 2:
                monster.move_towards(game_map, entities, target=target)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        # if cannot see but known last location
        else:
            for monster_target in monster.fighter.targets:
                if entities.index(target) == monster_target.entity_index:
                    # move to last known location
                    if monster.distance_to(monster_target):
                        monster.move_towards(game_map, entities, target=monster_target)
                    
                    monster_target.increment_time()
                    

        return results

    def to_json(self):
        json_data = {
            'name': self.__class__.__name__
        }

        return json_data

    @staticmethod
    def from_json():
        basic_monster = BasicMonster()

        return basic_monster


class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, game_map, entities):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(game_map, entities, target_x=random_x, target_y=random_y)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer confused!'.format(self.owner.name))})

        return results

    def to_json(self):
        json_data = {
            'name': self.__class__.__name__,
            'previous_ai': self.previous_ai.__class__.__name__,
            'number_of_turns': self.number_of_turns
        }

        return json_data

    @staticmethod
    def from_json(json_data, owner):
        previous_ai_name = json_data.get('previous_ai')
        number_of_turns = json_data.get('number_of_turns')

        if previous_ai_name == 'BasicMonster':
            previous_ai = BasicMonster()
            previous_ai.owner = owner
        else:
            previous_ai = None

        confused_monster = ConfusedMonster(previous_ai, number_of_turns)

        return confused_monster
