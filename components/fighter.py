from game_messages import Message

from components.target_entity import Target_Entity

class Fighter:
    def __init__(self, hp, defense, power, xp=0, fov_range=0, targets=[], seen_objects=[]):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp
        self.fov_range = fov_range
        self.targets = targets
        self.seen_objects = seen_objects

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)))})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name))})

        return results

    def to_json(self):
        json_data = {
            'max_hp': self.base_max_hp,
            'hp': self.hp,
            'defense': self.base_defense,
            'power': self.base_power,
            'xp': self.xp,
            'fov_range': self.fov_range,
            'targets': [target.to_json() for target in self.targets],
            'seen_objects': [target.to_json() for target in self.seen_objects]
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        max_hp = json_data.get('max_hp')
        hp = json_data.get('hp')
        defense = json_data.get('defense')
        power = json_data.get('power')
        xp = json_data.get('xp')
        fov_range = json_data.get('fov_range')
        targets_data = json_data.get('targets')
        seen_objects_data = json_data.get('seen_objects')

        targets = [Target_Entity.from_json(target) for target in targets_data]
        seen_objects = [Target_Entity.from_json(target) for target in seen_objects_data]

        fighter = Fighter(max_hp, defense, power, xp, fov_range, targets, seen_objects)
        fighter.hp = hp

        return fighter
