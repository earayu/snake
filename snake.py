import pygame, sys, random
from pygame.locals import *

# TODO 移动平滑，速度根据长度改变，随机出生地点，重构代码

#################################### 游戏基本设置
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720
CELL_SIZE = 15
MOVE_SIZE = CELL_SIZE
assert WINDOW_WIDTH % CELL_SIZE == 0 and WINDOW_HEIGHT % CELL_SIZE == 0, '窗口大小不合适'


FPS = 10

#################################### 颜色
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLACK = (0,0,0)
DARKGRAY  = ( 40,  40,  40)
BGC = WHITE # 背景颜色

#################################### 游戏逻辑
SNAKE_LEN = 5 # 蛇的长度

# 蛇移动的方向和距离
SNAKE_LEFT = (-MOVE_SIZE,0)
SNAKE_RIGHT = (MOVE_SIZE,0)
SNAKE_UP = (0,-MOVE_SIZE)
SNAKE_DOWN = (0,MOVE_SIZE)
# 初始化方向
SNAKE_DIR = SNAKE_RIGHT
SNAKE_COLOR = RED

APPLE = None

#################################### 离散变量，需要重构
add = False



class Snake():
    def __init__(self, lens=SNAKE_LEN, direction=SNAKE_DIR, color=SNAKE_COLOR, cell_size=CELL_SIZE, move_size=MOVE_SIZE):
        self.len = lens
        self.direction = direction
        self.color = color
        self.cell_size = cell_size
        self.move_size = move_size

        self.nodes = []
        self.dirs = []


        for i in reversed(range(lens)):
            self.nodes.append(pygame.Rect(i * cell_size, 0, cell_size, cell_size))
            self.dirs.append([direction, direction])

        self._tailNode = self.nodes[-1]


    def add(self):
        global add
        self.len += 1
        _tail_node = self._tailNode
        _tail_dir = self.nodes[-1]
        self.nodes.append(pygame.Rect(_tail_node.x, _tail_node.y, self.cell_size, self.cell_size))
        self.dirs.append([_tail_dir[0], _tail_dir[1]])
        add = False  # todo

    def crash(self):
        head = self.nodes[0]
        for node in self.nodes[1:]: # 撞到自己
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

    # 吃到苹果
    def eatApple(self, apple):
        global add
        if self.nodes[0].colliderect(apple):
            add = True

    def draw(self, SURFACE):
        for node in self.nodes:
            pygame.draw.rect(SURFACE, self.color, node)

    def march(self):
        self._tailNode = self.nodes[-1]

        for i in range(len(self.dirs)):
            self.dirs[i][0] = self.dirs[i][1]
            if i == 0:
                self.dirs[0][1] = self.direction
            else:
                self.dirs[i][1] = self.dirs[i - 1][0]
            self.nodes[i] = self.nodes[i].move(self.dirs[i][1])








class Apple(pygame.sprite.Sprite):
    def __init__(self):
        self.apple = pygame.Rect(CELL_SIZE*random.randint(0,(WINDOW_WIDTH/CELL_SIZE)-1), CELL_SIZE*random.randint(0,(WINDOW_HEIGHT/CELL_SIZE)-1), CELL_SIZE, CELL_SIZE)

# 在地图上随机生成一个APPLE
def genApple():
    return pygame.Rect(CELL_SIZE*random.randint(0,(WINDOW_WIDTH/CELL_SIZE)-1), CELL_SIZE*random.randint(0,(WINDOW_HEIGHT/CELL_SIZE)-1), CELL_SIZE, CELL_SIZE)

def drawScore(score):
    scoreSurf = BASICFONT.render('score: %s' % (score), True, DARKGRAY)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOW_WIDTH - 120, 10)
    SURFACE.blit(scoreSurf, scoreRect)


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
    pygame.time.wait(500)

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




# 吃到苹果
def eatApple(rect):
    if APPLE.colliderect(rect):
        return True
    return False

def snake_run(SURFACE):
    global snake,APPLE,add
    SURFACE.fill(BGC)

    snake.draw(SURFACE)

    if APPLE is None:
        APPLE = genApple()
    pygame.draw.rect(SURFACE, GREEN, APPLE)

    if eatApple(snake.nodes[0]):
        add = True
        APPLE = None

    if snake.crash():
        if showGameOverScreen():
            snake = Snake()

    drawScore(snake.len - SNAKE_LEN)
    pygame.display.update()


def eventProcessor():
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if snake.direction is not SNAKE_RIGHT:
                    snake.direction = SNAKE_LEFT
            if event.key == K_RIGHT:
                if snake.direction is not SNAKE_LEFT:
                    snake.direction = SNAKE_RIGHT
            if event.key == K_UP:
                if snake.direction is not SNAKE_DOWN:
                    snake.direction = SNAKE_UP
            if event.key == K_DOWN:
                if snake.direction is not SNAKE_UP:
                    snake.direction = SNAKE_DOWN


    # 代码放这里减小延迟
    snake.march()
    if add:
        snake.add()

def mainLoop():
    while True:
        eventProcessor()
        snake_run(SURFACE)
        fpsClock.tick(FPS)


if __name__ == '__main__':
    # 初始化贪吃蛇
    pygame.init()
    pygame.display.set_caption("snake")
    SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    fpsClock = pygame.time.Clock()
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    snake = Snake()
    mainLoop()



