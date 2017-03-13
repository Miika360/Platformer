import pygame, random

pygame.init()

gameTrue = True
screenWidth = 1500
screenHeight = 800
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont("Arial", 40)

#colors
white = (255, 255, 255)
black = (0, 0, 0)
playerColor = (0, 255, 0)
zombieColor = (255, 0, 0)
gravity = 0.5
score = 0
reset = False
scrolling = 7
ropes = 5


zombieStart = 4
maxZombies = 15
zombieSpawnTime = 2.5
zombieList = []
platforms = []
platformList = []

playerX = 800
playerY = 500
playerSize = 30

backroundpic = pygame.image.load("C:\\Users\\Miika\\Backround1.png")
platformpic=  pygame.image.load("C:\\Users\Miika\\Platform1.png")
zombiepic = pygame.image.load("C:\\Users\\Miika\\Zombie1.png")
playerpic = pygame.image.load("C:\\Users\\Miika\\Player1.png")
playerpic2 = pygame.transform.flip(playerpic, True, False)
zombiepic2 = pygame.transform.flip(zombiepic, True, False)

alive = True
moving = False

gameDisplay = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Platformer")

def intro():
    intro = True
    gameDisplay.blit(backroundpic, (0,0))
    gameDisplay.blit(font.render(("Press W to start!"), 1, (255,255,255)), (400,400))
    pygame.display.update()
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    intro = False

def death():
    global platformList, platforms, zombieList, score, playerX, playerY, gameTrue, alive, reset, ropes
    dead = True
    gameDisplay.blit(backroundpic, (0,0))
    gameDisplay.blit(font.render(("YOU DIED!"), 1, (255,0,0)), (200,200))
    gameDisplay.blit(font.render(("Press Q to quit, R to restart."), 1, (255,255,255)), (400,400))
    pygame.display.update()
    while dead:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    dead = False
                    gameTrue = False
                elif event.key == pygame.K_r:
                    dead = False
                    player1.reset()
                    playerX = 800
                    playerY = 500
                    score = 0
                    zombieList = []
                    platformList = []
                    platforms = []
                    zomb.spawn()
                    ropes = 5
                    alive = True

class zombie():
    def __init__(self):

        self.zombieJump = random.randrange(8,12)
        self.zombieOnGround = False
        self.zombieSpeed = random.randrange(5,10)
        self.zombieSize = 30
        self.zombievsp = 0
        self.zombiehsp = 0
        self.zombieY = 0
        self.zombieX = random.randrange(0,screenWidth - self.zombieSize)

    def update(self):
        global alive

        if self.zombieX >= playerX + playerSize -10: self.zombiehsp = -self.zombieSpeed
        elif self.zombieX + self.zombieSize <= playerX +10: self.zombiehsp = self.zombieSpeed
        else: self.zombiehsp = 0
        if self.zombievsp <= 40: self.zombievsp += gravity

        if self.zombieY >= playerY + playerSize and self.zombieOnGround:
            self.zombievsp = -self.zombieJump

        self.zombieOnGround = False

        if self.zombieY + self.zombieSize + self.zombievsp >= screenHeight:
            self.zombievsp = 0
            self.zombieY = screenHeight - self.zombieSize
            self.zombieOnGround = True

        for platform in platforms:
            platformX, platformY, platformXsize, platformYsize = platform
            if self.zombieX + self.zombieSize > platformX and self.zombieX < platformX + platformXsize:
                if self.zombieY + self.zombieSize <= platformY and self.zombieY + self.zombieSize + self.zombievsp >= platformY:
                    self.zombieY = platformY - self.zombieSize
                    self.zombievsp = 0
                    self.zombieOnGround = True
                if self.zombieY + self.zombievsp <= platformY + platformYsize and self.zombieY > platformY + platformYsize:
                    self.zombievsp = 0
                    self.zombieY = platformY + platformYsize
            if self.zombieY + self.zombieSize > platformY and self.zombieY < platformY + platformYsize:
                if self.zombieX + self.zombiehsp <= platformX + platformXsize and self.zombieX + self.zombieSize > platformX +10:
                    self.zombiehsp = 0
                    self.zombieX = platformX + platformXsize
                elif self.zombieX + self.zombieSize + self.zombiehsp >= platformX and self.zombieX < platformX + platformXsize -10:
                    self.zombiehsp = 0
                    self.zombieX = platformX - self.zombieSize


        self.zombiehsp -= scrolling

        self.zombieX += self.zombiehsp
        self.zombieY += self.zombievsp

        if self.zombieX + self.zombieSize > playerX and self.zombieX < playerX + playerSize and self.zombieY + self.zombieSize > playerY and self.zombieY < playerY + playerSize:
            alive = False

        if self.zombiehsp + scrolling < 0:
            gameDisplay.blit(zombiepic2,(self.zombieX, self.zombieY))
        else:
            gameDisplay.blit(zombiepic, (self.zombieX, self.zombieY))

class zombieSpawn():
    def __init__(self):
        self.counter = 0
    def spawn(self):
        for i in range(zombieStart):
            zombieList.append(zombie())
    def zombieSpawnUpdate(self):
        global score, ropes
        self.counter += 1
        if self.counter == zombieSpawnTime * FPS:
            zombieList.append(zombie())
            self.counter = 0
            score += 1
            if score%10 == 0:
                ropes += 1
        if len(zombieList) > maxZombies:
           del zombieList[0]

class player():
    def __init__(self):

        self.hspeed = 0
        self.vspeed = 0
        self.mspeed = 10
        self.jump = 12
        self.jumps = 0
        self.maxjumps = 2
        self.left = 0
        self.right = 0
        self.againstWall = False
        self.direction = "right"
        self.ropePull = False
        self.closestPlat = None

    def ropePullMethod(self):
        self.closestPlat = None
        for platform in platforms:
            X, Y, Xsize, Ysize = platform
            if playerX +playerSize/2 >= X and playerX + playerSize/2 <= X + Xsize:
                if playerY > Y + Ysize:
                    if self.closestPlat == None or playerY - Y + Ysize > self.closestPlat:
                        self.closestPlat = Y + Ysize
        if self.closestPlat != None:
            if playerY > self.closestPlat:
                self.hspeed = -scrolling
                self.vspeed = -10
                pygame.draw.rect(gameDisplay, (255,255,255),(playerX + 12, self.closestPlat, 6, playerY - self.closestPlat))
        else:
            pygame.draw.rect(gameDisplay, (255,255,255),(playerX + 12, playerY, 6, -playerY))
            self.ropePull = False
            self.jumps = 1

    def reset(self):
        self.hspeed = 0
        self.vspeed = 0
        self.mspeed = 10
        self.jump = 12
        self.jumps = 0
        self.maxjumps = 2
        self.left = 0
        self.right = 0
        self.againstWall = False
        self.direction = "right"
        self.ropePull = False
        self.closestPlat = None

    def update(self):
        global playerX, playerY, moving, ropes

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ropes > 0:
                    ropes -= 1
                    self.ropePull = True
                if event.key == pygame.K_SPACE:
                    if self.againstWall:
                        self.vspeed = -self.jump
                        self.jumps = 1
                    elif self.jumps < self.maxjumps:
                        self.vspeed = -self.jump
                        self.jumps += 1
                if event.key == pygame.K_a: self.left = -1
                if event.key == pygame.K_d: self.right = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a: self.left = 0
                if event.key == pygame.K_d: self.right = 0

        if self.vspeed <= 40: self.vspeed += gravity
        self.move = self.left + self.right
        self.hspeed = self.mspeed * self.move
        self.hspeed -= scrolling

        if self.ropePull:
            player1.ropePullMethod()

        #PLATFORM COLLISION
        self.againstWall = False
        for platform in platforms:
            platformX, platformY, platformXsize, platformYsize = platform
            if playerX + playerSize > platformX and playerX < platformX + platformXsize:
                if playerY + playerSize <= platformY and playerY + playerSize + self.vspeed >= platformY:
                    playerY = platformY - playerSize
                    self.vspeed = 0
                    self.jumps = 0
                elif playerY + self.vspeed < platformY + platformYsize and playerY > platformY + platformYsize:
                    self.vspeed = 0
                    playerY = platformY + platformYsize
                    self.ropePull = False
            if playerY + playerSize > platformY and playerY < platformY + platformYsize:
                if playerX + self.hspeed <= platformX + platformXsize and playerX > platformX +10:
                    self.hspeed = 0
                    playerX = platformX + platformXsize
                    self.againstWall = True
                elif playerX + playerSize + self.hspeed >= platformX and playerX <= platformX + platformXsize -10:
                    self.hspeed = 0
                    playerX = platformX - playerSize
                    self.againstWall = True


        #SCREEN COLLISION
        if playerY + self.vspeed + playerSize >= screenHeight:
            self.vspeed = 0
            playerY = screenHeight - playerSize
            self.jumps = 0
        if playerY + self.vspeed < 0:
            self.vspeed = 0
            playerY = 0
        if playerX + self.hspeed + playerSize > screenWidth:
            self.hspeed = 0
            playerX = screenWidth - playerSize
        if playerX + self.hspeed < 0:
            self.hspeed = 0
            playerX = 0

        playerX += self.hspeed
        playerY += self.vspeed

        if self.move > 0: self.direction = "right"
        elif self.move < 0: self.direction = "left"

        if self.direction == "right": gameDisplay.blit(playerpic, (playerX, playerY))
        elif self.direction == "left": gameDisplay.blit(playerpic2, (playerX, playerY))

def platform(platformX, platformY, platformXsize, platformYsize, color = white):
    global platforms
    platforms.append([platformX, platformY, platformXsize, platformYsize])
    pygame.draw.rect(gameDisplay, color, [platformX, platformY, platformXsize, platformYsize])

class platform1():
    def __init__(self):
        global platforms
        self.platformX = round(random.randrange(screenWidth, screenWidth + 100))
        self.platformY = random.randrange(round(screenHeight * 2 / 3), round(screenHeight-30))
        self.platformXsize = 200
        self.platformYsize = 30

    def platformUpdate(self):
        self.platformX -= scrolling
        platforms.append([self.platformX, self.platformY, self.platformXsize, self.platformYsize])
        gameDisplay.blit(platformpic, (self.platformX, self.platformY))

class platform2():
    def __init__(self):
        global platforms
        self.platformX = round(random.randrange(screenWidth, screenWidth + 100))
        self.platformY = random.randrange(round(screenHeight/3),round(screenHeight*2/3))
        self.platformXsize = 200
        self.platformYsize = 30

    def platformUpdate(self):
        self.platformX -= scrolling
        platforms.append([self.platformX, self.platformY, self.platformXsize, self.platformYsize])
        gameDisplay.blit(platformpic, (self.platformX, self.platformY))

class platform3():
    def __init__(self):
        global platforms
        self.platformX = round(random.randrange(screenWidth, screenWidth + 100))
        self.platformY = random.randrange(30,round(screenHeight/3))
        self.platformXsize = 200
        self.platformYsize = 30

    def platformUpdate(self):
        self.platformX -= scrolling
        platforms.append([self.platformX, self.platformY, self.platformXsize, self.platformYsize])
        gameDisplay.blit(platformpic, (self.platformX, self.platformY))

def platformSpawn():
    global platformList
    spawn = True
    for platform in platforms:
        X, Y, SizeX, SizeY = platform
        if X + SizeX + 100 < 0: del platformList[0]
        if X + SizeX > screenWidth -100: spawn = False
    if spawn:
        spawnNumber = random.randrange(1000)
        if spawnNumber > 200:
            platformList.append(platform1())
        spawnNumber = random.randrange(1000)
        if spawnNumber > 300:
            platformList.append(platform2())
        spawnNumber = random.randrange(1000)
        if spawnNumber > 400:
            platformList.append(platform3())

player1 = player()
zomb = zombieSpawn()

intro()
zomb.spawn()
while gameTrue:

    gameDisplay.blit(backroundpic, (0,0))

    for platform in platformList:
        platform.platformUpdate()
    platformSpawn()

    player1.update()

    zomb.zombieSpawnUpdate()
    for zombies in zombieList:
        zombies.update()
    platforms = []
   
    gameDisplay.blit(font.render("Score: " + str(score), 1, (255,255,255)), (40,40))
    gameDisplay.blit(font.render("Ropes: " + str(ropes), 1, (255,255,255)), (40,90))

    pygame.display.update()
    clock.tick(FPS)

    if not alive:
        death()
pygame.quit()
quit()