import pyxel, random

class stats:
    score = 0
    level = 0
    def __init__(self, height, player):
        self.player = player
        self.height = height
        self.fullHealth = self.player.health 
        self.healthFollower = self.fullHealth
    def update(self):
         if self.healthFollower > self.player.health:
              self.healthFollower -= 0.05
    def draw(self):
        health = self.player.health
        pyxel.rect(0, -self.height, pyxel.width, self.height, 0)
        pyxel.rect(0, -self.height, pyxel.width * (self.healthFollower / self.fullHealth), self.height, 5)
        pyxel.rect(0, -self.height, pyxel.width * (health / self.fullHealth), self.height, 1)
        pyxel.line(0, -1, pyxel.width, -1, 13)

        if health < 0:
             health = 0
        pyxel.text(1, -self.height + 1, "Level "+ str(self.level), 7)
        pyxel.text(1, -self.height + 7, "Score " + str(self.score), 7)
        #pyxel.text(1, -self.height + 13, "Health " + str(health), 7)

class crossHeir:
    def __init__(self, STATSHEIGHT):
        self.x = 0
        self.y = 0
        self.size = 3
        self.hidden = False
        self.STATSHEIGHT = STATSHEIGHT

    def update(self):
        self.x = pyxel.mouse_x
        self.y = pyxel.mouse_y - self.STATSHEIGHT
    def hide(self):
        self.hidden = True
    def show(self):
        self.hiddne = False

    def draw(self, coolDown): #cooldown 0-11
        if not self.hidden:
            pyxel.circb(self.x, self.y, self.size * coolDown, 7)
            pyxel.line(self.x, self.y, self.x, self.y, 7)

def deathScreen(statsHeight, stats, dither):
     pyxel.dither(dither)
     pyxel.rect(0, -statsHeight, pyxel.width, pyxel.height + statsHeight, 0)
     score = stats.score
     level = stats.level
     deathMessage = "G A M E   O V E R"
     score = "F I N A L   S C O R E :  " + str(score)
     level = "L E V E L   R E A C H E D :  " + str(level)
     message = "press R to restart"
     pyxel.text(pyxel.width/2 - len(deathMessage)*2, (pyxel.height/2 - statsHeight) - 10, deathMessage, 5)
     pyxel.text(pyxel.width/2 - len(score)*2, (pyxel.height/2 - statsHeight) - 2, score, 6)
     pyxel.text(pyxel.width/2 - len(level)*2, (pyxel.height/2 - statsHeight) + 6, level, 6)
     pyxel.text(pyxel.width/2 - len(message)*2, (pyxel.height/2 - statsHeight) + 22, message, 5)

def ditherScreen(ditherAmount):
        pyxel.dither(ditherAmount)
        pyxel.rect(0, 0, pyxel.width, pyxel.height, 0)
        pyxel.dither(1)

def pauseScreen(self, message, dither): #show pauseScreen overlay
        ditherScreen(dither)
        pyxel.circb(self.player.x, self.player.y, self.player.WIDTH, 10)
        for enemy in self.enemies:
            tankX = enemy.tank.x
            tankY = enemy.tank.y
            width = enemy.tank.WIDTH * 1.5
            height = enemy.tank.HEIGHT * 1.5
            pyxel.rectb(tankX - width/2, tankY - height/2, width, height, 8)
            pyxel.text(tankX + width/2 + 2, tankY, "DANGER", 8)
        pyxel.text(self.player.x + self.player.WIDTH + 2, self.player.y, "WASD or arrow keys to move\n Click to shoot", 10)
        pyxel.text(pyxel.mouse_x - len(message)*2, pyxel.mouse_y - self.STATSHEIGHT - 10, message, 7)

def rumble(start, length, statsHeight):
    rumble = 1
    if start + length >= pyxel.frame_count:
        pyxel.camera(0 + random.randint(-rumble, rumble), -statsHeight + random.randint(-rumble, rumble))
    else:
        pyxel.camera(0, -statsHeight)