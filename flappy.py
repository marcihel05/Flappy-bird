#dodati gornji i donji rub


import random
import time
import neat
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame import mixer

WIN_WIDTH = 550
WIN_HEIGHT = 800

BIRD_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png")))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

mixer.init()
SOUNDS = [mixer.Sound(os.path.join("sounds", "die.wav")),mixer.Sound(os.path.join("sounds", "hit.wav")), mixer.Sound(os.path.join("sounds", "point.wav")),mixer.Sound(os.path.join("sounds", "wing.wav"))]

FPS = 30

pygame.font.init()

SCORE_FONT = pygame.font.SysFont("monospace", 25)
GAME_OVER_FONT = pygame.font.SysFont("monospace", 50)
overtext = GAME_OVER_FONT.render("Game Over", 1, (0,0,0))
continuetext1 = GAME_OVER_FONT.render("Press Enter", 1, (0,0,0))
continuetext2 = GAME_OVER_FONT.render("to start again", 1, (0,0,0))


class Bird:

    #tilt and flap
    ROT_VEL = 15
    MAX_ROT = 25

    def __init__(self, x, y):
        self.img = BIRD_IMG
        self.x = x
        self.y = y
        self.vel = 0
        self.tick = 0
        self.height = self.y
        self.tilt = 0

    def jump(self):
        self.vel = -10.5
        self.tick = 0
        self.y = self.y +4*self.vel
        self.height = self.y

    def move(self, win):
        if self.tick == -1:
            self.tick+=1
        self.tick +=1
        d = self.vel*self.tick + 1.5*self.tick**2   #s = v_0*t + a*t^2/2

        if d>=16:
            d = 16
        
        if d<0:
            d-=2
        
        self.y = self.y+d

        if d<0 or self.y<self.height+50: #bird goes up
            if self.tilt< self.MAX_ROT:
                self.tilt = self.MAX_ROT
            
        else: #bird goes down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
            
            

    def draw(self, win):

        rot_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rot_img.get_rect(center = self.img.get_rect(center = (self.x, self.y)).center)
        win.blit(rot_img,new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:

    def __init__(self,x):
        
        self.PIPE_BOTTOM = PIPE_IMG
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)

        self.x = x
        self.gap = 250
        self.vel = -5
        self.acc = 1.5

       # random.seed(time.time())
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.gap
        
        

    def move(self, pipe_vel):
        self.x = self.x+pipe_vel


    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def get_mask(self):
        return pygame.mask.from_surface(self.PIPE_BOTTOM), pygame.mask.from_surface(self.PIPE_TOP)
    



def check_collisions(bird, pipe):
    bird_mask = bird.get_mask()
    pipe_masks = pipe.get_mask()
    
    top_offset = ((round(pipe.x) - round(bird.x)), (round(pipe.top) - round(bird.y)))
    bottom_offset = ((round(pipe.x) - round(bird.x)), (round(pipe.bottom) - round(bird.y)))
   
    bottom_point = bird_mask.overlap(pipe_masks[0], bottom_offset)
    top_point = bird_mask.overlap(pipe_masks[1], top_offset)

    if bottom_point or top_point:
        return True
    if bird.y <=0 or bird.y > WIN_HEIGHT:
        return True
    else:
        return False
    
    
def game_over(win, pipes, score):
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return False
        win.blit(BG_IMG, (0,0))
        for i in range (len(pipes)):
            pipes[i].draw(win)
        scoretext = GAME_OVER_FONT.render("Score = "+str(score), 1, (0,0,0))
        win.blit(scoretext, (150,250))
        win.blit(overtext, (150,100))
        win.blit(continuetext1, (100,400))
        win.blit(continuetext2, (80,450))
        pygame.display.update()





def draw_window(win, bird, pipes, score):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    for i in range (len(pipes)):
        pipes[i].draw(win)
    scoretext = SCORE_FONT.render("Score = "+str(score), 1, (0,0,0))
    win.blit(scoretext, (5,10))
    pygame.display.update()



def main():
    run = True

    while run:
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
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        SOUNDS[3].play()
                        bird.jump()
        
            bird.move(win)
            for i in range (len(pipes)):
                pipes[i].move(pipe_vel)
            if check_collisions(bird, pipes[last_pipe]):
                SOUNDS[1].play()
                SOUNDS[0].play()
                play = False
        
            if passed == 0 and bird.x >= pipes[last_pipe].x+pipes[last_pipe].PIPE_TOP.get_width():
                score+=1
                SOUNDS[2].play()
                passed = 1
                if score >=15 and score%15 == 0:
                    pipe_vel*=pipe_acc
            draw_window(win, bird, pipes, score)

            if pipes[last_pipe].x < 75:
                pipes.append(Pipe(WIN_WIDTH))
                last_pipe+=1
                passed = 0
    
        if play == False:
            if game_over(win, pipes, score):
                run = False
            
                
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()



