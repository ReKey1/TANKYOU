import random

class WorldItem:
    floor = (0, 0)
    pristineFloor = (1, 0)
    brokenFloor = (0, 1)
    noFloor = (1, 1)
    destructedFloor = (8, 0) #floor left after box breaks
    destructedFloor2 = (8, 1)
    spawnPoint = (5, 0)
    enemySpawnPoint = (5, 1)

    boxTL = (2, 0)
    boxTR = (3, 0)
    boxBL = (2, 1)
    boxBR = (3, 1)
    sBox = (4, 0)

    #broken version of boxes
    brBoxTL = (6, 0)
    brBoxTR = (7, 0)
    brBoxBL = (6, 1)
    brBoxBR = (7, 1)
    brSBox = (4, 1)

    normBoxes = [boxTL, boxTR, boxBL, boxBR, sBox]
    brokBoxes = [brBoxTL, brBoxTR, brBoxBL, brBoxBR, brSBox]

class Box:
    quadrant = 2
    def __init__(self, coords, type, chunk, size):
        self.coords = (int(coords[0]), int(coords[1])) #index of this box in boxlocations array
        self.size = size
        self.type = type #box type
        self.chunk = chunk
        self.currentDither = 1 #how much "dither"
        self.ditherVal = random.uniform(0.7, 1) #remember how much "dither"
        if self.type == WorldItem.sBox: #is a small box
            self.maxHealth = 2
        elif self.type in WorldItem.normBoxes: #is a large box
            self.maxHealth = 4
        self.health = self.maxHealth
    def hit(self, damage):
        self.takeDamage(damage)
        if 0 < self.health and self.health <= int(self.maxHealth/2):
            self.damaged()
            return []
        elif self.health <= 0:
            return self.destroyed()
        return []
    
    def takeDamage(self, damage):
        self.health -= damage

    def changeType(self, newType): #helper function, changes type at correct location in array
        self.type = newType

    def damaged(self):     
        if self.type == WorldItem.sBox:
            self.changeType(WorldItem.brSBox)    
        if self.type == WorldItem.boxTL:
            self.changeType(WorldItem.brBoxTL)
        self.currentDither = self.ditherVal
    def destroyed(self):
        return[self]

    def draw(self, pyxel):
        pyxel.dither(self.currentDither)
        pyxel.blt(self.coords[0]*8, self.coords[1]*8, 0, self.type[0]*8, self.type[1]*8, self.size, self.size)
        pyxel.dither(1)

class World:
    HEIGHT = 16
    WIDTH = 16
    XOFFSET = 0
    YOFFSET = 0
    def __init__(self, tilemap, xloc, yloc):
        self.spawn = (8, 8)
        self.XOFFSET = xloc * 16
        self.YOFFSET = yloc * 16
        self.tilemap = tilemap
        self.world_map = []
        self.boxLocations = []
        self.enemySpawnLocations = []
        for y in range(self.YOFFSET, self.HEIGHT + self.YOFFSET):
            self.world_map.append([])
            for x in range(self.XOFFSET, self.WIDTH + self.XOFFSET):
                tile = self.tilemap.pget(x, y)
                if tile == WorldItem.spawnPoint:
                    self.spawn = ((x - self.XOFFSET + 1)*8, (y - self.YOFFSET + 1)*8)
                if tile == WorldItem.enemySpawnPoint:
                    self.enemySpawnLocations.append(((x - self.XOFFSET + 1)*8, (y - self.YOFFSET + 1)*8))
                if tile in [WorldItem.floor, WorldItem.spawnPoint, WorldItem.enemySpawnPoint]:
                    self.world_map[y-self.YOFFSET].append(randFloor()) #generate random floor tile
                else:
                    rnd = random.randint(0, 1)
                    if rnd == 0:
                        flrType = WorldItem.destructedFloor
                    else:
                        flrType = WorldItem.destructedFloor2
                    
                    self.world_map[y-self.YOFFSET].append(flrType)
                    if tile in [WorldItem.boxTL]: #for big boxes
                        self.boxLocations.append(Box((x - self.XOFFSET, y - self.YOFFSET), tile, self, 16))
                    elif tile in [WorldItem.sBox]: #for little boxes
                        self.boxLocations.append(Box((x - self.XOFFSET, y - self.YOFFSET), tile, self, 8))
        #self.reset()    
    def reset(self):
        self.boxLocations = []
        for item in self.BOXLOCATIONS:
            self.boxLocations.append(item)
        for item in self.WORLD_MAP:
            self.world_map.append(item)

def randFloor():
    floorType = random.randint(0,100)
    if floorType == 0:
        return WorldItem.noFloor
    elif 1 <= floorType <= 10:
        return WorldItem.brokenFloor
    elif 11 <= floorType <= 20:
        return WorldItem.pristineFloor
    else:
        return WorldItem.floor

def world_item_draw(pyxel, x, y, world_item, quadrant, quadrantOffset):
    xOffset = quadrantOffset[quadrant][0]
    yOffset = quadrantOffset[quadrant][1]
    pyxel.blt(
        x*8 + xOffset,
        y*8 + yOffset,
        0,
        world_item[0]*8,
        world_item[1]*8,
        8,
        8
    )