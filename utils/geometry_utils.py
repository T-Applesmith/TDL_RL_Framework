import math

#from entity import get_blocking_entities_at_location


class Rect:
    def __init__(self, x, y, w, h):
        self.struct_name = 'Rect'
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def to_json(self):
        json_data = {
            'struct_name': self.struct_name,
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2
        }

        return json_data

    def from_json(json_data):
        struct_name = json_data.get('struct_name')
        x1 = json_data.get('x1')
        y1 = json_data.get('y1')
        x2 = json_data.get('x2')
        y2 = json_data.get('y2')

        rect = Rect(x1, y1, x2-x1, y2-y1)

        return rect
    

class Line:
    def __init__(self, x1, y1, x2=None, y2=None, m=None, l=None):
        self.struct_name = 'Line'
        if m == None and l == None:
            self.x1 = x1
            self.x2 = x2
            self.y1 = y1
            self.y2 = y2

            self.m = None
            self.l = None
        elif x2 == None and y2 == None:
            # Not sure if this will ever be used
            self.x1 = x1
            self.y1 = y1
            self.m = m
            self.l = l

            self.x2 = None
            self.y2 = None
        else:
            raise Exception('Line.__init__(): Invalid Line input params')
        self.tiles = self.pass_through_tiles(1)

        return

    def to_json(self):
        json_data = {
            'struct_name': self.struct_name,
            'x1': self.x1,
            'x2': self.x2,
            'y1': self.y1,
            'y2': self.y2,
            'm': self.m,
            'l': self.l
        }

        return json_data

    def from_json(json_data):
        struct_name = json_data.get('struct_name')
        x1 = json_data.get('x1')
        x2 = json_data.get('x2')
        y1 = json_data.get('y1')
        y2 = json_data.get('y2')
        m = json_data.get('m')
        l = json_data.get('l')

        line = Line(x1, y1, x2, y2, m, l)

        return line

    def update(self, x1=None, y1=None, x2=None, y2=None, m=None, l=None):
        if (m == None or self.m == None) and (l == None or self.l == None):
            if x1 is not None:
                self.x1 = x1
            if x2 is not None:
                self.x2 = x2
            if y1 is not None:
                self.y1 = y1
            if y2 is not None:
                self.y2 = y2

            self.m = None
            self.l = None
        elif (x2 == None and self.x2 == None) and (y2 == None and self.y2 == None):
            # Not sure if this will ever be used
            if x1 is not None:
                self.x1 = x1
            if y1 is not None:
                self.y1 = y1
            if m is not None:
                self.m = m
            if l is not None:
                self.l = l

            self.x2 = None
            self.y2 = None
        else:
            raise Exception('Line.update(): Invalid Line update params')
        self.tiles = self.pass_through_tiles()
        
        return self

    def slope(self):
        if self.x1 != self.x2:
            self.m = (self.y2 - self.y1)/(self.x2 - self.x1)
        else:
            self.m = None
        return self.m


    def pass_through_tiles(self, r):
        '''
        Line
        r : distance from center to be considered within tile
        r = .4 seems decent
        '''
        tiles = []

        if not self.m:
            self.slope()

        if self.m == None:
            direction = 'POS'
            #x_walk, y_walk = self.x2 +.5, self.y2 +.5
        elif  self.m >= 0:
            direction = 'POS'
            #x_walk, y_walk = self.x2 +.5, self.y2 +.5
        else:
            direction = 'NEG'
            #x_walk, y_walk = self.x1 +.5, self.y1 +.5

        #decide where to start
        if direction == 'POS':
            if self.x2 > self.x1:
                x_walk, y_walk = self.x1 +.5, self.y1 +.5
            elif self.x2 == self.x1:
                if self.y2 > self.y1:
                    x_walk, y_walk = self.x1 +.5, self.y1 +.5
                else:
                    x_walk, y_walk = self.x2 +.5, self.y2 +.5
            else:
                x_walk, y_walk = self.x2 +.5, self.y2 +.5
        elif direction == 'NEG':
            if self.x2 > self.x1:
                x_walk, y_walk = self.x2 +.5, self.y2 +.5
            elif self.x2 == self.x1:
                if self.y2 > self.y1:
                    x_walk, y_walk = self.x2 +.5, self.y2 +.5
                else:
                    x_walk, y_walk = self.x1 +.5, self.y1 +.5
            else:
                x_walk, y_walk = self.x1 +.5, self.y1 +.5

        #and where to end
        if x_walk == self.x1+.5 and y_walk == self.y1+.5:
            destination = 2
        else:
            destination = 1

        print('direction:{0} walk:({1},{2}) 1:({3},{4}) 2:({5},{6}) DST:{7}'.format(direction,x_walk,y_walk,self.x1,self.y1,self.x2,self.y2,destination))

        if not ((destination == 1 and (.25 <= abs(x_walk - (self.x1 +.5)) or .25 <= abs(y_walk - (self.y1 +.5)))) or\
              (destination == 2 and (.25 <= abs(x_walk - (self.x2 +.5)) or .25 <= abs(y_walk - (self.y2 +.5))))):
            if destination == 1:
                print('X:{0} Y:{1}'.format(.25 <= abs(x_walk - (self.x1 +.5)), .25 <= abs(y_walk - (self.y1 +.5))))
            if destination == 2:
                print('X:{0} Y:{1}'.format(.25 <= abs(x_walk - (self.x2 +.5)), .25 <= abs(y_walk - (self.y2 +.5))))
        #while x_walk < (self.x2 +.5) and y_walk < (self.y2 +.5):
        #while x_walk < (self.x2 +.5) and y_walk < (self.y2 +.5):
        #while (direction == 'POS' and (x_walk < (self.x1 +.5) or y_walk < (self.y1 +.5))) or \
        #      (direction == 'NEG' and (x_walk > (self.x2 +.5) or y_walk > (self.y2 +.5))):
        #while (direction == 'POS' and (.25 <= abs(x_walk - (self.x1 +.5)) and .25 <= abs(y_walk - (self.y1 +.5)))) or \
        #      (direction == 'NEG' and (.25 <= abs(x_walk - (self.x2 +.5)) and .25 <= abs(y_walk - (self.y2 +.5)))):
        while (destination == 1 and (.25 <= abs(x_walk - (self.x1 +.5)) or .25 <= abs(y_walk - (self.y1 +.5)))) or\
              (destination == 2 and (.25 <= abs(x_walk - (self.x2 +.5)) or .25 <= abs(y_walk - (self.y2 +.5)))):
            x_floor, y_floor = math.floor(x_walk), math.floor(y_walk)
                
            #print('pass_through: ({0},{1}) distance:{2}'.format(x_floor,y_floor,distance_to(x_floor+.5, y_floor+.5, x_walk, y_walk)))
            if (not (x_floor, y_floor) in tiles) and distance_to(x_floor+.5, y_floor+.5, x_walk, y_walk) < r:
                tiles.append((x_floor, y_floor))

            if direction == 'POS':
                if self.m == None:
                    y_walk += 1
                elif self.m == 0:
                    x_walk += 1
                else:
                    delta_x = math.sqrt(.01/(self.m**2 + 1))
                    delta_y = self.m * delta_x
                    x_walk += delta_x
                    y_walk += delta_y
            elif direction == 'NEG':
                if self.m == None:
                    y_walk -= 1
                elif self.m == 0:
                    x_walk -= 1
                else:
                    delta_x = math.sqrt(.01/(self.m**2 + 1))
                    delta_y = self.m * delta_x
                    x_walk -= delta_x
                    y_walk -= delta_y
                    
            #print('x_walk:{0};y_walk:{1}'.format(x_walk, y_walk))

        print('Line Pass_Through_Tiles: {0}'.format(tiles))
        return tiles
        

class Cone:
    def __init__(self, h, k, x, y, arc_length=None, angle=None):
        '''
        NOT PROPERLY DEBUGGED
        
        (h,k) - origin points
        (x,y) - destination points
        radius - distance from origin to destination
        slope - angle from origin to destination
        arc_length - distance from side to side along curve
        angle - angle from destination to edge of arc
        '''
        self.struct_name = 'Cone'
        if arc_length == None and angle == None:
            print('ERROR: Cone requires either arc_length or angle')
        elif angle == None:
            angle = self.calc_angle(arc_length, distance_to(h, k, x, y))
            self.angle = angle
        elif arc_length == None:
            arc_length = angle * distance_to(h, k, x, y)
            self.arc_length = arc_length
        
        self.update(h, k, x, y, arc_length, angle)

    def to_json(self):
        json_data = {
            'struct_name': self.struct_name,
            'h': self.h,
            'k': self.k,
            'x': self.x,
            'y': self.y,
            'arc_length': self.arc_length,
            'angle': self.angle
            }

        return json_data

    def from_json(json_data):
        struct_name = json_data.get('struct_name')
        h = json_data.get('h')
        k = json_data.get('k')
        x = json_data.get('x')
        y = json_data.get('y')
        arc_length = json_data.get('arc_length')
        angle = json_data.get('angle')

        cone = Cone(h, k, x, y, arc_length, angle)

        return cone
        

    #@classmethod
    def update(self, h=None, k=None, x=None, y=None, arc_length=None, angle=None):
        if h is None:
            h = self.h
        if k is None:
            print('k updated')
            k = self.k
        if x is None:
            print('x updated')
            x = self.x
        if y is None:
            y = self.y
        if arc_length is None:
            if self.arc_length is None:
                arc_length = 0
            else:
                arc_length = self.arc_length
            
        if angle is None:
            if self.angle is None:
                angle = 0
            else:
                angle = self.angle

        self.h = h
        self.k = k
        self.x = x
        self.y = y

        print('Cone: {0}'.format(self.__dict__))
        #print('{0}'.format(self.__dir__()))

        self.radius = distance_to(h, k, x, y)
        self.slope = self.calc_slope(h, k, x, y)
        self.arc_length = arc_length
        self.angle = self.calc_angle(arc_length, self.radius)
        self.tiles = self.pass_through_tiles(1)

        print('Cone: {0}'.format(self.__dict__))
            
        return self

    def calc_slope(self, h, k, x, y):
        if h != x:
            #print('y-k: {0}'.format(y-k))
            m = (y - k)/(x - h)
        else:
            m = 99999999
        
        #nudge so edge case of -0 does not exist
        if y == k:
            if h > x:
                m -= .00000001
            elif h < x:
                m += .00000001
        
        return m

    def calc_angle(self, arc_length, radius):
        if radius != 0:
            angle = arc_length/radius
        else:
            angle = 0
        return angle

    def pass_through_tiles(self, r):
        '''
        r - number of hits to bet considered within a tile
        '''
        tiles = []
        x_orig, y_orig = self.h +.5, self.k +.5
        x_dest, y_dest = self.x +.5, self.y +.5
        #print('Pass_Through_Tiles: ({0},{1}) ({2},{3})'.format(x_orig,y_orig,x_dest,y_dest))

        base_slope = math.atan2(self.y-self.k, self.x-self.h)
        #print('base_slope:{0}'.format(base_slope))

        angle_1 = base_slope + self.angle
        angle_2 = base_slope - self.angle
        #print('angle1: {0} angle2: {1} difference: {2}'.format(angle_1, angle_2, angle_1-angle_2))

        #print('Cos(A1):{0} Sin(A1):{1} Cos(A2):{2} Sin(A2):{3}'.format(self.radius * math.cos(angle_1),self.radius * math.sin(angle_1),self.radius * math.cos(angle_2),self.radius * math.sin(angle_2)))      
        alpha_1 = (self.radius * math.cos(angle_1)) +x_orig
        beta_1 = (self.radius * math.sin(angle_1)) +y_orig
        
        alpha_2 = (self.radius * math.cos(angle_2)) +x_orig
        beta_2 = (self.radius * math.sin(angle_2)) +y_orig
        #print('orig:({0},{1}) dest:({2},{3}) ab_1:({4},{5}) ab_2:({6},{7})'.format(x_orig,y_orig,x_dest,y_dest,alpha_1,beta_1,alpha_2,beta_2))

        self.alpha_1, self.beta_1 = alpha_1, beta_1
        self.alpha_2, self.beta_2 = alpha_2, beta_2        

        tile_container = [[0 for x in range(2 * math.ceil(self.radius))] for y in range(2 * math.ceil(self.radius))]
        if self.angle < 1.5708:
            y_scan = min(y_orig, y_dest, beta_1, beta_2)
        else:
            y_scan = self.k - self.radius
            
        while y_scan <= y_orig + self.radius:
            #begin scanning across y-Axis
            if self.angle < 1.5708:
                x_scan = min(x_orig, x_dest, alpha_1, alpha_2)
            else:
                x_scan = self.h - self.radius
                
            while x_scan <= x_orig + self.radius:
                #begin scanning across x-Axis
                Test_1, Test_2, Test_3, Test_4, Test_5 = False, False, False, False, False

                x_floor = math.floor(x_scan)
                y_floor = math.floor(y_scan)

                #print('{0} {1} {2} {3}'.format(self.h, x_scan, x_floor, self.radius))
                x_container = self.h - x_floor
                y_container = self.k - y_floor
                
                #print('scan:({0},{1})'.format(x_scan, y_scan))

                if alpha_1 == x_orig:
                    alpha_1 += .0001
                if alpha_2 == x_orig:
                    alpha_2 += .0001

                #print('  test 1 : {0}'.format(((beta_1 - y_orig)/(alpha_1 - x_orig))))

                if min(x_orig, x_dest, alpha_1, alpha_2) <= x_scan and max(x_orig, x_dest, alpha_1, alpha_2) >= x_scan: 
                    Test_1 = True
                if min(y_orig, y_dest, beta_1, beta_2) <= y_scan and max(y_orig, y_dest, beta_1, beta_2) >= y_scan:
                    Test_2 = True
                if self.radius ** 2 >= (x_scan - x_orig)**2 + (y_scan - y_orig)**2:
                    Test_3 = True
                if alpha_2 >= x_orig:
                    if y_scan >= truncate((beta_2 - y_orig)/(alpha_2 - x_orig),5) * (x_scan - x_orig) + y_orig:
                        Test_4 = True
                elif alpha_2 < x_orig:
                    if y_scan < truncate((beta_2 - y_orig)/(alpha_2 - x_orig),5) * (x_scan - x_orig) + y_orig:
                        Test_4 = True
                if alpha_1 >= x_orig:
                    if y_scan < truncate((beta_1 - y_orig)/(alpha_1 - x_orig),5) * (x_scan - x_orig) + y_orig:
                        Test_5 = True
                elif alpha_1 < x_orig:
                    if y_scan >= truncate((beta_1 - y_orig)/(alpha_1 - x_orig),5) * (x_scan - x_orig) + y_orig:
                        Test_5 = True

                if Test_3 and ((self.angle < 1.5708 and Test_4 and Test_5) or (self.angle >= 1.5708 and (Test_4 or Test_5)))\
                   and (x_floor != self.h or y_floor != self.k):
                    #print('container_size:{0} x_contain:{1} y_contain:{2}'.format(2 * math.ceil(self.radius), x_container, y_container))
                    tile_container[x_container][y_container] += 1

                    if (not (x_floor, y_floor) in tiles) and tile_container[x_container][y_container] >= r:
                        #print('container_size:{0} x_contain:{1} y_contain:{2}'.format(2 * math.ceil(self.radius), x_container, y_container))
                        tiles.append((x_floor, y_floor))

                x_scan += .25
            #print('exit x_scan')
            y_scan += .25
                
        return tiles  


class Coordinate:
    def __init__(self, h, k):
        self.struct_name = 'Coordinate'
        self.h = h
        self.k = k
        self.tiles = [(h, k)]

    def to_json(self):
        json_data = {
            'struct_name': self.struct_name,
            'x': self.h,
            'y': self.k,
            'tiles': self.tiles
            }
        return json_data

    def from_json(json_data):
        h = json_data.get('h')
        k = json_data.get('k')

        coords = Coordinate(h, k)

        return coords

    def update(self, h=None, k=None, x=None, y=None):
        if h is not None:
            self.h = h
        if k is not None:
            self.k = k
        if x is not None:
            self.h = x
        if y is not None:
            self.k = y
        self.tiles = [(self.h, self.k)]

        return self


class Circle:
    def __init__(self, h, k, x=None, y=None, radius=None):
        '''        
        (h,k) - origin points
        (x,y) - destination points
        radius - distance from origin to destination
        '''
        self.struct_name = 'Circle'
        self.h, self.k, self.x, self.y, self.radius = None, None, None, None, None
        self.update(h, k, x, y, radius)

    def to_json(self):
        json_data = {
            'struct_name': self.struct_name,
            'h': self.h,
            'k': self.k,
            'x': self.x,
            'y': self.y,
            'radius': self.radius
            }

        return json_data

    def from_json(json_data):
        struct_name = json_data.get('struct_name')
        h = json_data.get('h')
        k = json_data.get('k')
        x = json_data.get('x')
        y = json_data.get('y')
        radius = json_data.get('radius')

        circle = Circle(h, k, x, y, radius)

        return circle

    #@classmethod
    def update(self, h=None, k=None, x=None, y=None, radius=None):
        if h is None:
            h = self.h
        if k is None:
            k = self.k
        if x is None:
            x = self.x
        if y is None:
            y = self.y            

        self.h = h
        self.k = k
        self.x = x
        self.y = y

        if radius is None and self.radius is None:
            self.radius = distance_to(h, k, x, y)
        elif radius is not None:
            self.radius = radius
        self.tiles = self.pass_through_tiles(1)

        print('Circle: {0}'.format(self.__dict__))
        return self

    def pass_through_tiles(self, r):
        '''
        r : distance from center to be considered within tile
        '''
        tiles = []
        
        y_scan = self.k +.5-self.radius

        while y_scan <= self.k +.5+self.radius:
            x_scan = self.h +.5-self.radius
            while x_scan <= self.h +.5+self.radius:
                x_floor, y_floor = math.floor(x_scan), math.floor(y_scan)
                
                if (not (x_floor, y_floor) in tiles) and distance_to(x_floor+.5, y_floor+.5, x_scan, y_scan) < r:
                    tiles.append((x_floor, y_floor))

                x_scan += .2
            y_scan += .2
        
        print('Circle Pass_Through_Tiles: {0}:'.format(tiles))
        return tiles

def distance_to(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx ** 2 + dy ** 2)

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

def blocking_between(entities, game_map, x1, y1, x2, y2):
    is_blocking = False
    line = Line(x1, y1, x2=x2, y2=y2)
    for coordinate in line.tiles:
        #print('Coordinate ({0},{1}): transparent:{2} walkable:{3}'.format(coordinate[0], coordinate[1], game_map.transparent[coordinate[0]][coordinate[1]], game_map.walkable[coordinate[0]][coordinate[1]]))
        #if get_blocking_entities_at_location(entities, coordinate[0], coordinate[1]) != None and not (game_map.transparent[coordinate[0]][coordinate[1]] and game_map.walkable[coordinate[0]][coordinate[1]]):
        if get_blocking_entities_at_location(entities, coordinate[0], coordinate[1]) != None or not game_map.transparent[coordinate[0]][coordinate[1]]:
            if not ((coordinate[0] == x1 and coordinate[1] == y1) or (coordinate[0] == x2 and coordinate[1] == y2)): 
                is_blocking = True
    if not line.tiles:
        is_blocking = True
    return is_blocking
    
def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
