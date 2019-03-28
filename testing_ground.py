from equipment_slots import EquipmentSlots

def main():
    walk_straight()

def unicode_test():
    for i in range(0, 65536):
        if (i % 100):
            print(str(i)+": "+chr(i))
        else:
            print(chr(i))
        #32-126

def sign(x):
    return int(x>0) - int(x<0)

def walk_straight():
    self = 10
    target = -33
    
    walk = self
    y = target - self
    direction = int(y>0) - int(y<0)

    while walk != target:
        walk += direction
        print('{0}'.format(walk))

if __name__ == '__main__':
    main()


