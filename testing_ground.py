from equipment_slots import EquipmentSlots

for i in range(0, 65536):
    if (i % 100):
        print(str(i)+": "+chr(i))
    else:
        print(chr(i))
    #32-126
