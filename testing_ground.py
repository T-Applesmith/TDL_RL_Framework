from equipment_slots import EquipmentSlots
from utils.geometry_utils import Cone, Line

def main():
    '''
    #walk_straight()

    
    #line = Line(0,0, 5, 1)
    #print('Line:({0},{1}),({2},{3}),m={4}'.format(line.x1,line.y1,line.x2,line.y2,line.m))
    #tiles = line.pass_through_tiles(.4)
    '''

    cone = Cone(1, 1, 1, 1, .7854*4)
    tiles = cone.pass_through_tiles(.4)
    print('tiles: {0}'.format(tiles))

    cone = cone.update(h=3,x=3)
    tiles = cone.pass_through_tiles(.4)
    print('tiles: {0}'.format(tiles))

    

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


