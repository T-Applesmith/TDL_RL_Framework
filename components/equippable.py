from equipment_slots import EquipmentSlots

class Equippable:
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus

    def to_json(self):
        print('Beginning save of equippable')
        slot_data = self.slot.value
        print('slot_data: {0}'.format(slot_data))
        
        json_data = {
            'slot': slot_data, 
            'power_bonus': self.power_bonus,
            'defense_bonus': self.defense_bonus,
            'max_hp_bonus': self.max_hp_bonus
        }
        print('equippable: {0}'.format(json_data))
        print('Save of equippable complete')

        return json_data

    def from_json(json_data):
        slot_data = json_data.get('slot')
        print('Loading slot_data: '+str(slot_data))
        slot = EquipmentSlots(slot_data)
        print('Loading slot: '+str(slot))
        power_bonus = json_data.get('power_bonus')
        defense_bonus = json_data.get('defense_bonus')
        max_hp_bonus = json_data.get('max_hp_bonus')

        equippable = Equippable(slot, power_bonus, defense_bonus, max_hp_bonus)
        print('equippable: {0}\n\t{1}'.format(equippable,equippable.__dict__))

        return equippable
