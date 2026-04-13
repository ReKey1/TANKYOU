import pyxel, random, math
from tank import Tank, Enemy
from ui import *
from world import *

class App:
    GAMEHEIGHT = 256
    GAMEWIDTH = 256
    STATSHEIGHT = 20
    MAPLISTX = 6 #max map index you can choose from
    MAPLISTY = 1
    quadrantOffset = {1:(128, 0), 2:(0, 0), 3:(0, 128), 4:(128, 128)}
    GAMESTATES = ["Death", "Pause", "Game", "Countdown"]
    GAMESTATE = "Pause"
    countdownLength = 3

    def __init__(self):
        pyxel.init(self.GAMEWIDTH, self.GAMEHEIGHT + self.STATSHEIGHT, title="TANK YOU")
        self.start()
        pyxel.run(self.update, self.draw)
    def start(self):
        pyxel.camera(0, -self.STATSHEIGHT)
        self.currentBoxLocations = [] #array all box locations on the map at the moment.
        self.tanks = []
        self.tanks.append(Tank(0)) #create player object. player is index 0. 
        self.player = self.tanks[0]
        self.stats = stats(self.STATSHEIGHT, self.player)
        self.crossheir = crossHeir(self.STATSHEIGHT)
        pyxel.load("tank_sprites.pyxres") #load tank sprites
        self.allChunks = [] #list of possible chunks
        for y in range(self.MAPLISTY + 1):
            for x in range(self.MAPLISTX + 1):
                self.allChunks.append(World(pyxel.tilemaps[0], x, y))
        
        self.reset()
    def enemyList(self, enemyNum):
        sniperCost = 3
        sniperRate = 2/10 * enemyNum
        shotgunCost = 2
        shotgunRate = 3/10 * enemyNum
        currency = enemyNum
        enemies = []
        for i in range(enemyNum):
            if currency <= 0:
                return enemies
            
            randomNum = random.randint(0, enemyNum)
            if randomNum <= sniperRate and currency - sniperCost >= 0:
                currency -= sniperCost
                enemies.append(Tank(3))
            elif randomNum <= shotgunRate and currency - shotgunCost >= 0:
                currency -= shotgunCost
                enemies.append(Tank(2))
            elif currency >= 1:
                currency -= 1
                enemies.append(Tank(1))
        return enemies

        
    def reset(self):
        pyxel.sounds[0].set("g3rg4", "TT", "4040", "N", 2) #bullet shoot sound player and red enemy
        pyxel.sounds[1].set(notes='C2', tones='p', volumes='25', effects='N', speed=4) #bullet bounce sound
        pyxel.sounds[2].set("g1ra0", "p", "66", "N", 5)#bullet shoot sound of shotgun
        pyxel.sounds[3].set("g1rg2", "p", "6622", "N", 5)#bullet shoot sound of sniper
        pyxel.sounds[4].set("a0", "n", "6622", "N", 15) #sound of getting hit
        
        self.lastHit = -1000
        self.stats.level += 1
        self.player.canShoot = True
        self.currentBoxLocations = []
        self.projectiles = []
        self.tanks = [self.tanks[0]]
        self.chunks = []
        self.enemySpawn = []
        for i in range(4):
            randChunk = self.allChunks[random.randint(0, len(self.allChunks) - 1)]
            self.chunks.append(randChunk)
            for box in randChunk.boxLocations: #make a new array for the box locations currently on the screen.
                coords = (box.coords[0] + self.quadrantOffset[i + 1][0]/8, box.coords[1] + self.quadrantOffset[i + 1][1]/8)
                self.currentBoxLocations.append(Box(coords, box.type, box.chunk, box.size))
            if i != 1: #don't spawn enemies in same chunk player spawns in 
                for coordinate in randChunk.enemySpawnLocations:
                    self.enemySpawn.append((coordinate[0] + self.quadrantOffset[i + 1][0], coordinate[1] + self.quadrantOffset[i + 1][1]))
        
        #create enemy tanks here!
        enemyNum = int(0.5 * (self.stats.level-1)) + 1
        if enemyNum > len(self.enemySpawn) - 1:
            enemyNum = len(self.enemySpawn)
        newEnemies = self.enemyList(enemyNum)

        for newEnemy in newEnemies:
            spawn = self.enemySpawn[random.randint(0, len(self.enemySpawn)-1)]
            newEnemy.x = spawn[0]
            newEnemy.y = spawn[1]
            self.tanks.append(newEnemy)
            self.enemySpawn.remove(spawn)
        self.enemies = []
        for enemyIndex in range(len(self.tanks[1:])):
            self.enemies.append(Enemy(self.tanks, enemyIndex + 1))

        self.player.x, self.player.y = self.chunks[1].spawn[0], self.chunks[1].spawn[1]

    def update(self):
        if pyxel.btnp(pyxel.KEY_1):
            pyxel.play(0, 4)
        rumble(self.lastHit, 10, self.STATSHEIGHT) #move the camera if player is hit
        if self.GAMESTATE in ["Death", "Pause", "Countdown"]:
            paused = True
            self.player.attackX = pyxel.mouse_x
            self.player.attackY = pyxel.mouse_y - self.STATSHEIGHT
            if self.GAMESTATE == "Pause":
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.startTime = pyxel.frame_count #remember when the screen was clicked to start countdown and timer
                    for enemy in self.enemies:
                        enemy.resetCooldown(self.startTime + self.countdownLength * 30)
                    self.GAMESTATE = "Countdown"
        else:
            paused = False
        
        self.crossheir.update()#update crossheir
        self.stats.update()
        
        if len(self.tanks) == 1 and self.GAMESTATE != "Pause": #reset stage when no enemies are left and all enemy bullets are gone.
            self.player.canShoot = False #stop shooting
            resetStage = True
            for projectile in self.projectiles: #check if enemy bullets still here
                if projectile.parentTank != self.player:
                    resetStage = False
                    break
            if resetStage:
                self.reset()
                self.GAMESTATE = "Pause"

        if self.player.health <= 0 and self.GAMESTATE != "Death": #die when health reaches 0
            self.GAMESTATE = "Death"
            self.deathDither = 0
        if self.GAMESTATE == "Death":#to reset game
            if pyxel.btnp(pyxel.KEY_R):
                self.start()
                self.GAMESTATE = "Pause"
        if not paused: #run game
            self.GAMEUPDATE()

    def GAMEUPDATE(self):
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):#update for player inputs
            self.player.up()
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.player.down()
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.player.right()
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.player.left()
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.shoot(self.player)
        for wall in self.currentBoxLocations: #player collide with walls
                self.player.collide(wall.coords, wall.size)
        self.player.boundaryCollision(self.STATSHEIGHT) #player collide with screen borders
        self.player.update(pyxel.mouse_x, pyxel.mouse_y - self.STATSHEIGHT)#update player

        for enemy in self.enemies: #collide with other enemies
            enemy.collideTanks(self.tanks)
        
        for enemy in self.enemies:
            if self.player.canEnemySeeMe(enemy, self.currentBoxLocations):
                enemy.tank.behavior = "Active"
            elif self.player.behavior != "Idle":
                enemy.tank.behavior = "Searching"

        for enemy in self.tanks[1:]:#update tank and tank barrel positions for enemy tanks
            for wall in self.currentBoxLocations:
                enemy.collide(wall.coords, wall.size)
            enemy.boundaryCollision(self.STATSHEIGHT)
            if enemy.behavior == "Searching" or enemy.behavior == "Idle":
                enemy.update(enemy.x + math.cos(enemy.trueDirection)*enemy.gun.length, enemy.y + math.sin(enemy.trueDirection)*enemy.gun.length)
            elif enemy.behavior == "Active":
                enemy.update(self.player.x, self.player.y)
            self.shoot(enemy)
        for enemy in self.enemies: #update enemies
            enemy.update()

        projectileToDelete = [] #keeps track of things to delete
        boxToDelete = [] #same but for boxes

        for projectile in self.projectiles:#update projectile positions
            if projectile.update(): #if projectile needs to be destroyed
                projectileToDelete.append(projectile)
            else:
                for box in self.currentBoxLocations:
                    if projectile.collide(box.coords, box.size):
                        toDelete = box.hit(projectile.damage)
                        if not len(toDelete) == 0: #if box has been destroyed
                            for box in toDelete:
                                boxToDelete.append(box)
                if projectile.parentTank != self.player and projectile.collideTank(self.player, self.player.WIDTH/2):
                    pyxel.play(0, 4)
                    self.player.health -= projectile.damage #player hit
                    self.lastHit = pyxel.frame_count
                    projectileToDelete.append(projectile)
                elif projectile.parentTank == self.player:
                    for tank in self.tanks[1:]:
                        if projectile.collideTank(tank, tank.WIDTH):
                            tank.health -= projectile.damage #enemy hit
                            projectileToDelete.append(projectile)

        for enemy in self.tanks[1:]:
            if enemy.health <= 0:
                self.stats.score += 1
                self.tanks.remove(enemy)

        for projectile in projectileToDelete: #remove projectiles that are out of bounds
            if projectile in self.projectiles:
                self.projectiles.remove(projectile)
            
        for box in boxToDelete: #remove unneeded boxes
            if box in self.currentBoxLocations:
                pyxel.play(0, 1)
                self.currentBoxLocations.remove(box)
        
    def draw(self):
        pyxel.cls(0)
        for i in range(4):
            for y in range(self.chunks[i].HEIGHT): #draw map
                for x in range(self.chunks[i].WIDTH):
                    world_item = self.chunks[i].world_map[y][x]
                    world_item_draw(pyxel, x, y, world_item, i+1, self.quadrantOffset)
        for box in self.currentBoxLocations: #draw boxes
            box.draw(pyxel)
        for tank in self.tanks:
            tank.draw()
        for enemy in self.enemies:
            enemy.draw()
        for projectile in self.projectiles:
            projectile.draw()

        if self.GAMESTATE == "Pause":
            pauseScreen(self, "CLICK SCREEN TO START", 0.5)
        if self.GAMESTATE == "Countdown":
            length = self.countdownLength
            remainingFrames = length * 30 + self.startTime - pyxel.frame_count
            remaining = round(remainingFrames / 30, 1)
            dither = 0.5 * (remaining / length)
            pauseScreen(self, str(remaining), dither)
            if remaining <= 0:
                self.GAMESTATE = "Game"
        
        self.stats.draw()#draw top stats display
        
        if self.GAMESTATE == "Death":
            if self.deathDither < 1:
                self.deathDither += 0.01
            deathScreen(self.STATSHEIGHT, self.stats, self.deathDither)
        self.crossheir.draw(self.player.coolDownStatus())#draw crossheir
 
    def shoot(self, tank): #function helps append projectiles to array.
        projectiles = tank.shoot()
        if projectiles != None:
            for projectile in projectiles:
                self.projectiles.append(projectile)

App()