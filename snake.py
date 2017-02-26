import pygame, sys, random
from pygame.locals import *

# TODO 移动平滑，速度根据长度改变，随机出生地点，重构代码

#################################### 游戏基本设置
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 10
MOVE_SIZE = CELL_SIZE
assert WINDOW_WIDTH % CELL_SIZE == 0 and WINDOW_HEIGHT % CELL_SIZE == 0, '窗口大小不合适'


FPS = 10


#################################### 游戏逻辑
SNAKE_LEN = 5 # 蛇的长度

# 蛇移动的方向和距离
SNAKE_LEFT = (-MOVE_SIZE,0)
SNAKE_RIGHT = (MOVE_SIZE,0)
SNAKE_UP = (0,-MOVE_SIZE)
SNAKE_DOWN = (0,MOVE_SIZE)
# 初始化方向
SNAKE_DIR = SNAKE_RIGHT

APPLE = None




#################################### 颜色
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLACK = (0,0,0)
DARKGRAY  = ( 40,  40,  40)
BGC = WHITE # 背景颜色


#################################### 离散变量，需要重构
a = None
b = None
add = False


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        self.apple = pygame.Rect(CELL_SIZE*random.randint(0,(WINDOW_WIDTH/CELL_SIZE)), CELL_SIZE*random.randint(0,(WINDOW_HEIGHT/CELL_SIZE)), CELL_SIZE, CELL_SIZE)

# 在地图上随机生成一个APPLE
def genApple():
    return pygame.Rect(CELL_SIZE*random.randint(0,(WINDOW_WIDTH/CELL_SIZE)), CELL_SIZE*random.randint(0,(WINDOW_HEIGHT/CELL_SIZE)), CELL_SIZE, CELL_SIZE)

# 初始化可爱的小蛇
def initSnake():
    global SNAKE_DIR, SNAKE_LEN
    SNAKE_LEN = 5
    SNAKE_DIR = SNAKE_RIGHT
    nodes = []
    dir = []
    for i in reversed(range(SNAKE_LEN)):
        nodes.append(pygame.Rect(i*CELL_SIZE,0,CELL_SIZE,CELL_SIZE))
        dir.append([SNAKE_DIR,SNAKE_DIR])
    return nodes,dir

# 增加一格蛇的长度
def snake_add(a,b):
    global SNAKE_LEN, nodes, dirs, add
    SNAKE_LEN += 1
    nodes.append(pygame.Rect(a.x,a.y,CELL_SIZE,CELL_SIZE))
    dirs.append([b[0],b[1]])
    add = False

# 吃到苹果
def eatApple(rect):
    if APPLE.colliderect(rect):
        APPLE
        return True
    return False

# 撞死
def crash(nodes):
    head = nodes[0]
    for node in nodes[1:]: # 撞到自己
        if node.colliderect(head):
            return True
    if head.left < 0:
        return True
    if head.right > WINDOW_WIDTH:
        return True
    if head.top < 0:
        return True
    if head.bottom > WINDOW_HEIGHT:
        return True

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30)
    SURFACE.blit(pressKeySurf, pressKeyRect)

def terminate():
    pygame.quit()
    sys.exit()

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, BLACK)
    overSurf = gameOverFont.render('Over', True, BLACK)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOW_WIDTH / 2, 10)
    overRect.midtop = (WINDOW_WIDTH / 2, gameRect.height + 10 + 25)

    SURFACE.blit(gameSurf, gameRect)
    SURFACE.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == None:
                    pass
                else:
                    # pygame.event.get()
                    return event.key

nodes,dirs = initSnake()

pygame.init()

pygame.display.set_caption("snake")

SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

fpsClock = pygame.time.Clock()

BASICFONT = pygame.font.Font('freesansbold.ttf', 18)


while True:
    SURFACE.fill(BGC)

    for node in nodes:
        pygame.draw.rect(SURFACE, RED, node)

    if APPLE is None:
        APPLE = genApple()
    pygame.draw.rect(SURFACE, GREEN, APPLE)

    if eatApple(nodes[0]):
        add = True
        a, b = nodes[-1], dirs[-1]
        APPLE = None

    if crash(nodes):
        if showGameOverScreen():
            nodes, dirs = initSnake()


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if SNAKE_DIR is not SNAKE_RIGHT:
                    SNAKE_DIR = SNAKE_LEFT
            if event.key == K_RIGHT:
                if SNAKE_DIR is not SNAKE_LEFT:
                    SNAKE_DIR = SNAKE_RIGHT
            if event.key == K_UP:
                if SNAKE_DIR is not SNAKE_DOWN:
                    SNAKE_DIR = SNAKE_UP
            if event.key == K_DOWN:
                if SNAKE_DIR is not SNAKE_UP:
                    SNAKE_DIR = SNAKE_DOWN


    for i in range(len(dirs)):
        dirs[i][0] = dirs[i][1]
        if i==0:
            dirs[0][1] = SNAKE_DIR
        else:
            dirs[i][1] = dirs[i-1][0]
        nodes[i] = nodes[i].move(dirs[i][1])

    if add:
        snake_add(a,b)

    fpsClock.tick(FPS)




