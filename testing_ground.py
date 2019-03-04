from equipment_slots import EquipmentSlots

def main():
    print(''+'a')

def unicode_test():
    for i in range(0, 65536):
        if (i % 100):
            print(str(i)+": "+chr(i))
        else:
            print(chr(i))
        #32-126

if __name__ == '__main__':
    main()
