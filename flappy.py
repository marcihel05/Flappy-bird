import random
import time
import neat
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

WIN_WIDTH = 550
WIN_HEIGHT = 800

BIRD_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png")))
PIPE_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe_top.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe_bottom.png")))]
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

FPS = 30


class Bird:

    #tilt and flap
    ROT_VEL = 20
    MAX_ROT = 90

    def __init__(self, x, y):
        self.img = BIRD_IMG
        self.x = x
        self.y = y
        self.vel = 0
        self.tick = 0
        self.height = self.y

    def jump(self):
        self.vel = -10.5
        self.tick = 0
        self.y = self.y +13*self.vel
        self.height = self.y

    def move(self):
        self.tick +=1
        d = self.vel + self.tick + 1.5*self.tick**2   #s = v_0*t + a*t^2/2

        if d>=16:
            d = 16
        
        if d<0:
            d-=2
        
        self.y = self.y+d

        #tilt and flap

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
    
    def get_mask(self):
        return pygem.mask.from_surface(self.img)

class Pipe:

    PIPE_TOP = PIPE_IMGS[0]
    PIPE_BOTTOM = PIPE_IMGS[1]

    def __init__(self,x):
        self.x = x
        self.dist = 100
        self.vel = -5
        self.acc = 1.5
        
        random.seed(time.time())
        self.bottom = random.randint(75, 450)
        self.top = self.bottom+self.dist
        

    def move(self, pipe_vel):
        self.x = self.x+pipe_vel


    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, 0-self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, WIN_HEIGHT-self.bottom))

   # def get_rect(self):


    
def draw_window(win, bird, pipes,score):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    for i in range (len(pipes)):
        pipes[i].draw(win)
    myfont = pygame.font.SysFont("monospace", 16)
    scoretext = myfont.render("Score = "+str(score), 1, (0,0,0))
    win.blit(scoretext, (5,10))
    pygame.display.update()


def main():
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Flappy bird')
    bird = Bird(200, 200)
    pipes = [Pipe(500)]
    last_pipe = 0
    play = True
    passed = 0
    score = 0
    pipe_vel = -5
    pipe_acc = 1.25
    clock = pygame.time.Clock()

    while play:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
        
        bird.move()
        for i in range (len(pipes)):
            pipes[i].move(pipe_vel)
        #check for crash
            #todo
        
        if passed == 0 and bird.x > pipes[last_pipe].x+30:
            score+=1
            passed = 1
            if score >=15 and score%15 == 0:
                pipe_vel*=pipe_acc
        draw_window(win, bird, pipes, score)

        if pipes[last_pipe].x < 75:
            pipes.append(Pipe(WIN_WIDTH))
            last_pipe+=1
            passed = 0
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()



