import math


class Rect:
    def __init__(self, x, y, w, h):
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
    

class Line:
    def __init__(self, x1, y1, x2=None, y2=None, m=None, l=None):
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
            raise Exception('Line.__init__: Invalid Line input params')
        #self.pass_through_tiles = self.pass_through_tiles()

    def slope(self):
        if self.x1 != self.x2:
            self.m = (self.y2 - self.y1)/(self.x2 - self.x1)
        else:
            self.m = None
        return self.m


    def pass_through_tiles(self, r):
        '''
        r : distance from center to be considered within tile
        r = .4 seems decent
        '''
        tiles = []
        x_walk, y_walk = self.x1 +.5, self.y1 +.5

        if not self.m:
            self.slope()

        while x_walk < (self.x2 +.5) and y_walk < (self.y2 +.5):
            x_floor, y_floor = math.floor(x_walk), math.floor(y_walk)
                
            if (not (x_floor, y_floor) in tiles) and distance_to(x_floor+.5, y_floor+.5, x_walk, y_walk) < r:
                tiles.append((x_floor, y_floor))
            
            if self.m == None:
                y_walk += 1
            elif self.m == 0:
                x_walk += 1
            else:
                delta_x = math.sqrt(.01/(self.m**2 + 1))
                delta_y = self.m * delta_x
                x_walk += delta_x
                y_walk += delta_y
            #print('x_walk:{0};y_walk:{1}'.format(x_walk, y_walk))

        print('Line Pass_Through_Tiles: {0}:'.format(tiles))
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
        if arc_length == None and angle == None:
            print('ERROR: Cone requires either arc_length or angle')
        elif angle == None:
            angle = self.calc_angle(arc_length, distance_to(h, k, x, y))
            self.angle = angle
        elif arc_length == None:
            arc_length = angle * distance_to(h, k, x, y)
            self.arc_length = arc_length
        
        self.update(h, k, x, y, arc_length, angle)

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
        r - distance from center to be considered within tile
        '''
        tiles = []
        x_orig, y_orig = self.h +.5, self.k +.5
        x_dest, y_dest = self.x +.5, self.y +.5

        base_slope = math.atan2(self.y-self.k, self.x-self.h)
        #print('base_slope:{0}'.format(base_slope))

        angle_1 = base_slope + self.angle
        angle_2 = base_slope - self.angle
        #print('angle1: {0} angle2: {1} difference: {2}'.format(angle_1, angle_2, angle_1-angle_2))

        print('Cos(A1):{0} Sin(A1):{1} Cos(A2):{2} Sin(A2):{3}'.format(self.radius * math.cos(angle_1),self.radius * math.sin(angle_1),self.radius * math.cos(angle_2),self.radius * math.sin(angle_2)))
        alpha_1 = (self.radius * math.cos(angle_1)) +x_orig
        beta_1 = (self.radius * math.sin(angle_1)) +y_orig
        
        alpha_2 = (self.radius * math.cos(angle_2)) +x_orig
        beta_2 = (self.radius * math.sin(angle_2)) +y_orig
        print('orig:({0},{1}) dest:({2},{3}) ab_1:({4},{5}) ab_2:({6},{7})'.format(x_orig,y_orig,x_dest,y_dest,alpha_1,beta_1,alpha_2,beta_2))

        self.alpha_1, self.beta_1 = alpha_1, beta_1
        self.alpha_2, self.beta_2 = alpha_2, beta_2        

        y_scan = y_orig - self.radius
        while y_scan <= y_orig + self.radius:
            #begin scanning across y-Axis
            x_scan = x_orig - self.radius
            while x_scan <= x_orig + self.radius:
                #begin scanning across x-Axis
                Test_1, Test_2, Test_3, Test_4, Test_5 = False, False, False, False, False

                x_floor = math.floor(x_scan)
                y_floor = math.floor(y_scan)
                
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

                if Test_3 and Test_4 and Test_3 and Test_4 and Test_5:
                    if (not (x_floor, y_floor) in tiles):
                        tiles.append((x_floor, y_floor))

                x_scan += .25
            #print('exit x_scan')
            y_scan += .25
                
        return tiles  


class Coordinate:
    def __init__(self, h, k):
        self.h = h
        self.k = k
        self.tiles = (h, k)

    def to_json(self):
        json_data = {
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


def distance_to(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx ** 2 + dy ** 2)

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper
