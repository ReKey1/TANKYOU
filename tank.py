import pyxel, math, random

def collision(x1, y1, w1, h1, x2, y2, w2, h2):
    # Calculate the right and bottom edges of both rectangles
    r1, b1 = x1 + w1, y1 + h1
    r2, b2 = x2 + w2, y2 + h2
    
    # Check if the rectangles overlap
    if x1 < r2 and r1 > x2 and y1 < b2 and b1 > y2:
        return True
    else:
        return False 
    
def circle_rectangle_collision(circle_x, circle_y, circle_radius, rect_x, rect_y, rect_w, rect_h):
    # Find the closest point to the circle within the rectangle
    closest_x = max(rect_x, min(circle_x, rect_x + rect_w))
    closest_y = max(rect_y, min(circle_y, rect_y + rect_h))
    
    # Calculate the distance between the circle's center and this closest point
    distance_x = circle_x - closest_x
    distance_y = circle_y - closest_y

    # Calculate the distance squared
    distance_squared = distance_x**2 + distance_y**2
    
    # If the distance squared is less than the radius squared, there is a collision
    return distance_squared < circle_radius**2   

def point_position(direction_radians, x_base, y_base, x_point, y_point, tolerance_radians):
    # Direction vector components
    dx = math.cos(direction_radians)
    dy = math.sin(direction_radians)
    
    # Vector from base to point
    px = x_point - x_base
    py = y_point - y_base
    
    # Calculate the magnitude of vectors
    vector_magnitude = math.sqrt(dx**2 + dy**2)
    point_vector_magnitude = math.sqrt(px**2 + py**2)
    
    # Dot product
    dot_product = dx * px + dy * py
    
    # Calculate the cosine of the angle between the vectors
    if vector_magnitude == 0 or point_vector_magnitude == 0:
        cos_angle = 1  # Angle is 0 if one of the vectors is zero
    else:
        cos_angle = dot_product / (vector_magnitude * point_vector_magnitude)
        
    # Clamp the cosine value to the range [-1, 1] to avoid domain errors in acos
    cos_angle = max(-1, min(1, cos_angle))
    
    # Calculate the angle between the vectors in radians
    angle_between = math.acos(cos_angle)
    
    # Cross product to determine the side
    cross_product = dx * py - dy * px
    angle_between = abs(angle_between - math.radians(180)) #idk chat gpt is weird this is wacky code don't ask it works now
    if angle_between <= tolerance_radians:
        return "on the line"
    elif cross_product > 0:
        return "left"
    else:
        return "right"

def is_point_in_rectangle(x, y, rect):
    """Check if a point (x, y) is inside a rectangle."""
    x1, y1, w, h = rect
    x2, y2 = x1 + w, y1 + h
    return x1 <= x <= x2 and y1 <= y <= y2

def do_lines_intersect(p1, p2, q1, q2):
    """Check if line segment p1p2 intersects with line segment q1q2."""
    def ccw(a, b, c):
        """Check if the points a, b, and c are listed in a counter-clockwise order."""
        ax, ay = a
        bx, by = b
        cx, cy = c
        return (cy - ay) * (bx - ax) > (by - ay) * (cx - ax)
    
    return ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2)

def does_line_intersect_rectangle(rect, line):
    """Check if a line intersects a rectangle."""
    x1, y1, w, h = rect
    x3, y3, x4, y4 = line
    
    # Check if either end of the line is inside the rectangle
    if is_point_in_rectangle(x3, y3, rect) or is_point_in_rectangle(x4, y4, rect):
        return True
    
    # Rectangle corners
    rect_points = [
        (x1, y1),
        (x1 + w, y1),
        (x1 + w, y1 + h),
        (x1, y1 + h)
    ]
    
    # Rectangle edges
    rect_edges = [
        (rect_points[0], rect_points[1]),
        (rect_points[1], rect_points[2]),
        (rect_points[2], rect_points[3]),
        (rect_points[3], rect_points[0])
    ]
    
    # Check if the line intersects any of the rectangle's edges
    for edge in rect_edges:
        if do_lines_intersect((x3, y3), (x4, y4), edge[0], edge[1]):
            return True
    
    return False

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))

class Gun:
        def __init__(self):
            self.tipX = 0
            self.tipY = 0
            self.angle = 0
            self.color = 1
            self.length = 7
            self.width = 1
        def draw(self, startX, startY, endX, endY):
            if (endX - startX) == 0:
                angle = self.angle
            else:
                angle = math.atan((endY - startY) / (endX - startX))
            if endX < startX:#note: math.tan gives only up to pi, does not go over 180 degrees.
                angle += math.radians(180)
            #pyxel.line(startX, startY, startX + self.length*math.cos(angle), startY + self.length*math.sin(angle), self.color)

            tempX = startX
            tempY = startY
            incX = math.cos(angle) #incriment x by
            incY = math.sin(angle) #incriment y by
            for i in range(int(self.length)):
                pyxel.circ(tempX, tempY, self.width, self.color)
                tempX += incX
                tempY += incY
            self.tipX = tempX
            self.tipY = tempY
            self.angle = angle

class Projectile:
    color = 7
    outlineColor = 0
    radius = 2
    hasBounced = False
    gone = False
    bounceNum = 2
    def __init__(self, x, y, direction, parentTank):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 2.1
        self.damage = parentTank.damage

        self.parentTank = parentTank
        if parentTank.tankType == 1: #red enemy
            self.color = 7
            self.outlineColor = 8
        if parentTank.tankType == 2: #brown enemy
            self.color = 7
            self.outlineColor = 8
            self.radius = 1
            self.bounceNum = 0
            self.speed = random.randint(20, 25)/10
        if parentTank.tankType == 3:#green enemy
            self.color = 0
            self.outlineColor = 8
            self.speed = 3.5
            self.bounceNum = 1


        self.xMoveBy = math.cos(self.direction) * self.speed
        self.yMoveBy = math.sin(self.direction) * self.speed
    def update(self):
        self.x += self.xMoveBy
        self.y += self.yMoveBy
        if pyxel.width + self.radius*2 <= self.x or self.x <= -self.radius*2: #if out of bounds
            self.gone = True
            return True
        if pyxel.height + self.radius*2 <= self.y or self.y <= -self.radius*2:
            self.gone = True
            return True
        if self.bounceNum <= -1: #if projectile bounce number expires
            return True
        return False #return true if out of bounds
    def collide(self, coords, size):
        collided = False
        if circle_rectangle_collision(self.x + self.xMoveBy, self.y, self.radius, coords[0]*8, coords[1]*8, size, size):
            self.xMoveBy *= -1
            self.hasBounced = True
            collided = True
        if circle_rectangle_collision(self.x, self.y + self.yMoveBy, self.radius, coords[0]*8, coords[1]*8, size, size):
            self.yMoveBy *= -1  
            self.hasBounced = True 
            collided = True 
        if collided:
            self.bounceNum -= 1
            pyxel.play(0, 1)
        return collided
    def collideTank(self, tank, tankSize):
        size = tankSize
        x = (tank.x - tank.WIDTH/2)/8
        y = (tank.y -tank.HEIGHT/2)/8
        if self.parentTank != tank:
            return self.collide((x, y), size)
        return False

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)
        pyxel.circb(self.x, self.y, self.radius + 0, self.outlineColor)

class Tank:
    WIDTH = 14
    HEIGHT = 14
    x = WIDTH / 2 #x, y coordinates
    y = HEIGHT / 2
    xMoveBy = 0#will move by this amount in update()
    yMoveBy = 0
    health = 3
    canShoot = True
    behavior = "Searching"
    spreadDegrees = 0

    def __init__(self, tankType):
        self.direction = math.radians(0)
        self.trueDirection = math.radians(0)
        self.moveSp = 2 #pixels
        self.turnSp = math.radians(5)
        self.damage = 1 #how much damage projectiles do
        self.coolDown = 15 #frames. how long until can shoot again.
        self.lastFire = pyxel.frame_count

        self.spriteList = []
        self.spriteCorrection = {
            0:4, 1:3, 2:2, 3:1, 4:0, 5:15, 6:14, 7:13, 8:12, 9:11, 10:10, 11:9, 12:8, 13:7, 14:6, 15:5
            }#accounts for the bad layout of spritemap lol
        
        self.gun = Gun()        
        if tankType == 0: #player
            spriteY = 16
            self.gun.color = 5
            self.health = 6   
        elif tankType == 1: #red default enemy
            spriteY = 32
            self.gun.color = 9 
            self.coolDown = random.randint(50, 100)
            self.moveSp = 1
            self.health = 2
            self.spreadDegrees = 7
        elif tankType == 2: #brown shotgun enemy
            spriteY = 48
            self.gun.color = 9
            self.gun.length = 5
            self.gun.width = 2
            self.coolDown = random.randint(50, 70)
            self.damage = 0.5
            self.moveSp = 1.2
            self.spreadDegrees = 5
        elif tankType == 3: #green sniper enemy
            spriteY = 64
            self.gun.color = 10
            self.coolDown = random.randint(70, 100)
            self.moveSp = 0.5
            self.gun.length = 10
            self.damage = 2
            self.health = 2
        
        self.tankType = tankType
        for i in range(16): #gets correct spritemap according to if player or enemy
            self.spriteList.append((i*16, spriteY)) #sprite location x, y
        self.sprite = 4
        self.attackX = 0 #dictates where gun points
        self.attackY = 0


    def up(self):
        self.xMoveBy += math.cos(self.direction) * self.moveSp
        self.yMoveBy += math.sin(self.direction) * self.moveSp
    def down(self):
        self.xMoveBy -= math.cos(self.direction) * self.moveSp
        self.yMoveBy -= math.sin(self.direction) * self.moveSp
    def left(self):
        self.trueDirection -= self.turnSp
        if self.trueDirection < 0:
            self.trueDirection = (2*math.pi) - abs(self.trueDirection)
    def right(self):
        self.trueDirection += self.turnSp
        if self.trueDirection > (2*math.pi):
            self.trueDirection = self.trueDirection - (2*math.pi)
    def shoot(self):
        if pyxel.frame_count - self.lastFire >= self.coolDown and self.canShoot: 
            self.lastFire = pyxel.frame_count
            spreadDegrees = self.spreadDegrees #the spread of the shot
            bulletCount = 1 
            if self.tankType in [0, 1]: #if player or default enemy
                    pyxel.play(0, 0)
            if self.tankType == 2: #if shotgun
                bulletCount = 6
                pyxel.play(0, 2)
            if self.tankType == 3: #if sniper
                pyxel.play(0, 3)
            shot = []
            for i in range(bulletCount):
                shot.append(Projectile(self.gun.tipX, self.gun.tipY, self.gun.angle + math.radians(random.randint(-spreadDegrees, spreadDegrees)), self))
            return shot
    def coolDownStatus(self):
        out = (pyxel.frame_count - self.lastFire) / self.coolDown
        if out > 1:
            return 1
        return out
    def collide(self, coords, size):
        if circle_rectangle_collision(self.x + self.xMoveBy, self.y, self.WIDTH/2, coords[0]*8, coords[1]*8, size, size):
            self.xMoveBy = 0
        if circle_rectangle_collision(self.x, self.y + self.yMoveBy, self.WIDTH/2, coords[0]*8, coords[1]*8, size, size):
            self.yMoveBy = 0
    def boundaryCollision(self, statsHeight):
        if circle_rectangle_collision(self.x + self.xMoveBy, self.y, self.WIDTH/2, -self.moveSp, 0, self.moveSp, pyxel.height): #left wall
            self.xMoveBy = 0
            self.x = self.WIDTH/2
        if circle_rectangle_collision(self.x + self.xMoveBy, self.y, self.WIDTH/2, pyxel.width, self.moveSp, self.moveSp, pyxel.height): #right wall
            self.xMoveBy = 0
            self.x = pyxel.width - self.WIDTH/2
        if circle_rectangle_collision(self.x, self.y + self.yMoveBy, self.WIDTH/2, 0, -self.moveSp, pyxel.width, self.moveSp): #top wall
            self.yMoveBy = 0
            self.y = self.HEIGHT/2
        if circle_rectangle_collision(self.x, self.y + self.yMoveBy, self.WIDTH/2, 0, pyxel.height - statsHeight, pyxel.width, self.moveSp): #bottom wall
            self.yMoveBy = 0
            self.y = pyxel.height - self.HEIGHT/2 - statsHeight
    def canEnemySeeMe(self, enemy, boxes):
        for box in boxes:
            if does_line_intersect_rectangle((box.coords[0] * 8, box.coords[1] * 8, box.size, box.size), (enemy.tank.x, enemy.tank.y, self.x, self.y)):
                return False
        return True

    def update(self, attackX, attackY):
        self.x += self.xMoveBy
        self.y += self.yMoveBy

        if self.trueDirection == (2*math.pi):# make sure truedirection is not 360, instead is 0.
            self.trueDirection = 0
        self.direction = math.radians(22.5)*int(self.trueDirection / math.radians(22.5))
        directionID = round(self.direction / math.radians(22.5)) #a number 0-15 corresponding to a direction
        self.sprite = self.spriteCorrection[directionID] #sprite number according to sprite correction

        self.attackX = attackX #keep track of where gun was pointing last
        self.attackY = attackY
        self.xMoveBy, self.yMoveBy = 0, 0 #reset
        

    def draw(self):
        pyxel.blt(self.x-8, self.y-8, 0, self.spriteList[self.sprite][0], self.spriteList[self.sprite][1], 16, 16, 0)
        #pyxel.circ(self.x, self.y, self.WIDTH/2, 1) #hitbox
        #pyxel.line(self.x, self.y, self.x + 10 * math.cos(self.direction), self.y + 10*math.sin(self.direction), 2)
        self.gun.draw(self.x, self.y, self.attackX, self.attackY)

        
class Enemy:
    def __init__(self, tanks, selfIndex):
        self.selfIndex = selfIndex
        self.player = tanks[0]
        self.tank = tanks[selfIndex]
        self.lastKnownX = self.tank.x
        self.lastKnownY = self.tank.y
        self.lastMoved = (self.tank.x, self.tank.y)
        self.rotation = random.randint(0, 1)
        if self.tank.tankType == 1:
            self.health = 2
    def lookAt(self, x, y):
        direction = point_position(self.tank.trueDirection - math.radians(180), self.tank.x, self.tank.y, x, y, self.tank.turnSp)
        if direction == "left":
            self.tank.left()
        elif direction == "right":
            self.tank.right()

    def update(self):
        #print('\n-----------')
        #print(self.tank.behavior)

        if self.tank.tankType == 3:
            coolDown = self.tank.coolDownStatus()
            if 0.75 < coolDown:
                self.tank.gun.color = 9
            elif 0.5 < coolDown:
                self.tank.gun.color = 10
            else:
                self.tank.gun.color = 13

        if self.tank.behavior == "Active":
            self.lastKnownX = self.player.x
            self.lastKnownY = self.player.y
        
        if self.tank.behavior == "Idle" or (self.tank.behavior == "Searching" and self.distanceTo(self.lastKnownX, self.lastKnownY) <= self.tank.WIDTH * 5):
            self.tank.behavior = "Idle"
        
        if not self.tank.behavior == "Idle":
            self.lookAt(self.lastKnownX, self.lastKnownY)

        bumped = not self.moved()
        if self.tank.behavior == "Idle" and not bumped:
            self.rotation = random.randint(0, 1)
        if self.tank.behavior == "Idle" and bumped:
            if self.rotation == 0:
                self.tank.right()
            elif self.rotation == 1:
                self.tank.left()
        self.tank.up()

    def distanceTo(self, x, y):
        return distance((self.tank.x, self.tank.y), (x, y))
    
    def moved(self):
        prevLocation = (self.tank.x, self.tank.y)
        if self.tank.moveSp - distance(self.lastMoved, (self.tank.x, self.tank.y)) < 0.1:
            self.lastMoved = prevLocation
            return True
        self.lastMoved = prevLocation
        return False

    def collideTanks(self, tanks):
        for tank in tanks:
            if tank != self.tank:
                toCollide = tank
                self.tank.collide(((toCollide.x - toCollide.WIDTH/2)/8, (toCollide.y - toCollide.HEIGHT/2)/8), toCollide.WIDTH)

    def resetCooldown(self, time):
        self.tank.lastFire = time

    def draw(self): #for drawing extra stuff only for enemies
        alive = self.tank.health > 0
        if alive and self.tank.tankType == 3 and self.tank.behavior == "Active": #green enemy and sees player
            pyxel.dither(0.1)
            pyxel.line(self.tank.gun.tipX, self.tank.gun.tipY, self.player.x, self.player.y, 8)
            pyxel.dither(1)