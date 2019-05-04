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

        print('Pass_Through_Tiles: {0}:'.format(tiles))
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

        angle_1 = math.atan(self.slope) + self.angle
        angle_2 = math.atan(self.slope) - self.angle

        # Its messed up HERE
        alpha_1 = ((self.x - self.h)/abs(self.x - self.h + .00000001)) * self.radius * math.cos(angle_1) +x_orig
        #beta_1 = ((self.y - self.k)/abs(self.y - self.k + .00000001)) * self.radius * math.sin(angle_1) +y_orig
        alpha_2 = ((self.x - self.h)/abs(self.x - self.h + .00000001)) * self.radius * math.cos(angle_2) +x_orig
        #beta_2 = ((self.y - self.k)/abs(self.y - self.k + .00000001)) * self.radius * math.sin(angle_2) +y_orig
        #'''
        #alpha_1 = ((self.x - self.h)/(self.x - self.h + .00000001)) * self.radius * math.cos(angle_1) +x_orig
        beta_1 = ((self.y - self.k)/(self.y - self.k + .00000001)) * self.radius * math.sin(angle_1) +y_orig
        #alpha_2 = ((self.x - self.h)/(self.x - self.h + .00000001)) * self.radius * math.cos(angle_2) +x_orig
        beta_2 = ((self.y - self.k)/(self.y - self.k + .00000001)) * self.radius * math.sin(angle_2) +y_orig
        #'''
        print('orig:({0},{1}) dest:({2},{3}) ab_1:({4},{5}) ab_2:({6},{7})'.format(x_orig,y_orig,x_dest,y_dest,alpha_1,beta_1,alpha_2,beta_2))
        #print('angle_1:{0} angle_2:{1}'.format(angle_1, angle_2))

        y_scan = y_orig - self.radius
        while y_scan <= y_orig + self.radius:
            x_scan = y_orig - self.radius
            while x_scan <= x_orig + self.radius:
                #print('scan:({0},{1})'.format(x_scan, y_scan))
                #print('  test 1 : {0}'.format(((beta_1 - y_orig)/(alpha_1 - x_orig))))

                if alpha_1 == x_orig:
                    alpha_1 += .0001
                               
                #if y_scan <= truncate((beta_1 - y_orig)/(alpha_1 - x_orig),5) * (x_scan - x_orig) + y_orig:
                if  -.01 <= truncate((beta_1 - y_orig)/(alpha_1 - x_orig),5) * (x_scan - x_orig) + y_orig - y_scan:
                    #print('  test 2 : {0}'.format(((beta_2 - y_orig)/(alpha_2 - x_orig))))

                    if alpha_2 == x_orig:
                        alpha_2 += .0001
                    
                    #if y_scan >= truncate((beta_2 - y_orig)/(alpha_2 - x_orig),5) * (x_scan - x_orig) + y_orig:
                    if .01 >= truncate((beta_2 - y_orig)/(alpha_2 - x_orig),5) * (x_scan - x_orig) + y_orig - y_scan:
                        #print('  test 3 : {0}'.format((x_scan - x_orig)**2 + (y_scan - y_orig)**2))
                        
                        if self.radius ** 2 >= (x_scan - x_orig)**2 + (y_scan - y_orig)**2:

                            if (.5 - r <= x_scan % 1 <= .5 + r) and (.5 - r <= y_scan % 1 <= .5 + r):

                                width_style = 'middle'
                                if width_style == 'thin':
                                    if x_scan > 0:
                                        x_floor = math.floor(x_scan)
                                    else:
                                        x_floor = math.ceil(x_scan)
                                    if y_scan > 0:
                                        y_floor = math.floor(y_scan)
                                    else:
                                        y_floor = math.ceil(y_scan)
                                    
                                elif width_style == 'middle':
                                    #print('{0}'.format(x_scan % 1))
                                    if False:#(x_scan % 1 >.5 ):#and x_scan > 0) or (x_scan % 1 < .5 and x_scan < 0):
                                        x_floor = math.ceil(x_scan)
                                    else:
                                        x_floor = math.floor(x_scan)
                                    #print('{0}'.format(y_scan % 1))
                                    if False:#(y_scan % 1 >.5 ):#and y_scan > 0) or (y_scan % 1 < .5 and y_scan < 0):
                                        y_floor = math.ceil(y_scan)
                                    else:
                                        y_floor = math.floor(y_scan)
                                    
                                else: #thick
                                    x_floor, y_floor = math.floor(x_scan), math.floor(y_scan)

                                #print('  passed')
                                if (not (x_floor, y_floor) in tiles):
                                    tiles.append((x_floor, y_floor))
                                    #print('  ({0},{1})'.format(x_floor, y_floor))
                                #print(' passed 3, tiles:{0}'.format(tiles))

                x_scan += .25
            #print('exit x_scan')
            y_scan += .25
                
        return tiles
        
        # sacrifice this code to the Old Ones
'''
        # setup lines to walk along
        radius = distance_to(self.h, self.k, self.x, self.y)
        m = self.slope(self.h, self.k, self.x, self.y)
        print('X_Dest:{0}; Y_Dest:{1}; M:{2}; R:{3}'.format(x_dest, y_dest, m, radius))

        while (i >= 0):            
            # walk along lines
            x_walk, y_walk = self.h +.5, self.k +.5

            #while abs(x_walk) < abs(x_dest) or abs(y_walk) < abs(y_dest):
            while abs(x_walk - x_dest) > .1*r and abs(y_walk - y_dest) > .1*r:
                x_floor, y_floor = math.floor(x_walk), math.floor(y_walk)
                
                if (not (x_floor, y_floor) in tiles) and distance_to(x_floor+.5, y_floor+.5, x_walk, y_walk) < r:
                    tiles.append((x_floor, y_floor))
            
                if m == None:
                    y_walk += 1
                    print('Slope: Infinite')
                elif m == 0:
                    x_walk += 1
                    print('Slope: Zero')
                else:
                    # just checking
                    m = self.slope(self.h+.5, self.k+.5, x_dest, y_dest)
                    #
                    delta_x = math.sqrt(.01/(m**2 + 1))
                    delta_y = m * delta_x
                    x_walk += delta_x
                    y_walk += delta_y
                print('dx:{2};dy:{3};x_walk:{0};y_walk:{1}'.format(x_walk, y_walk, delta_x, delta_y))


            # find next point to walk towards
            print('X_Dest:{0}; Y_Dest:{1}; M:{2}; R:{3}'.format(x_dest, y_dest, m, distance_to(self.h, self.k, x_dest, y_dest)))
            if m != None and m != 0:
                # Calculate the points of a triangle given right angle, two points, and two lengths
                alpha = x_dest + math.sqrt(l**2 / (1 + m**-2))
                beta = y_dest - (alpha - x_dest)/m
            elif m == 0:
                pass
            elif m == None:
                pass
            x_dest = alpha
            y_dest = beta
            m = self.slope(self.h, self.k, x_dest, y_dest)
            print('Alpha:{0}; Beta:{1}; M:{2}'.format(x_dest, y_dest, m))

            #Choose point to be w/in range!
            x_dest = self.h + math.sqrt(radius**2 / (1 + m**2))
            y_dest = self.k - m*(self.h - x_dest)
            m = self.slope(self.h, self.k, x_dest, y_dest)
            print('X_Dest:{0}; Y_Dest:{1}; M:{2}; R:{3}'.format(x_dest, y_dest, m, distance_to(self.h, self.k, x_dest, y_dest)))
            
            i -= 1
            print('I:{0};                               Pass_Through_Tiles: {1}'.format(i, tiles))

        print('Pass_Through_Tiles: {0}:'.format(tiles))
        return tiles
'''        


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
