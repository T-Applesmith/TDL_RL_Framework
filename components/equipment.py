from equipment_slots import EquipmentSlots


class Equipment:
    def __init__(self, main_hand=None, off_hand=None):
        self.main_hand = main_hand
        self.off_hand = off_hand

    def to_json(self):
        print('Saving equipment')
        print('main_hand: '+str(self.main_hand)+'\noff_hand: '+str(self.off_hand))
        json_data = {}
        # these are entities
        if self.main_hand:
            json_data['main_hand'] = self.main_hand.to_json()
        if self.off_hand:
            json_data['off_hand'] = self.off_hand.to_json()
        
        print('Equipment: '+str(json_data))
        print('Equipment save successful')

        return json_data

    @staticmethod
    def from_json(json_data):
        from entity import Entity
        main_hand_entity = None
        off_hand_entity = None
        
        #print('main_hand: '+str(json_data.get('main_hand')))
        main_hand = json_data.get('main_hand')
        if main_hand:
            #main_hand = main_hand.items()
            print('main_hand: '+str(main_hand))
            main_hand_entity = Entity.from_json(main_hand)
            print('main_hand_entity: '+str(main_hand_entity))
            
        off_hand = json_data.get('off_hand')
        if off_hand:
            off_hand = off_hand.items()
            off_hand_entity = Entity.from_json(off_hand)
        
        print('main_hand: '+str(main_hand))

        equipment = Equipment(main_hand_entity, off_hand_entity)

        return equipment


    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.power_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        return bonus

    def toggle_equip(self, equippable_entity):
        results = []

        print('toggle_equip>equippable_entity: {0}\n\t{1}'.format(equippable_entity, equippable_entity.to_json()))
        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})

                print('self.main_hand: {0}'.format(self.main_hand))
                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})
                
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        return results
