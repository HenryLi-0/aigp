import pygame
import random
import sys
import math

pygame.init()

DISPLAY = (600, 400)
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("asteroids of doom and despair (evil version)")
clock = pygame.time.Clock()

class Constants:
    BG = (20, 11, 55)
    GRAVITY = 0.08
    BOUNCE = 1
    LDM = True
    DAMPEN = 0.5

class Ball:
    def __init__(self):
        self.r = random.random()*15+5
        self.pos = pygame.math.Vector2(random.uniform(self.r, DISPLAY[0]-self.r), random.uniform(self.r, DISPLAY[1]-self.r))
        self.vel = pygame.math.Vector2((random.randint(0,1)*2-1)*(random.random()*5), (random.randint(0,1)*2-1)*(random.random()*5))
        mm = lambda x: min(max(0, round(x) + random.random()*10-5), 255)
        temp = random.randint(100, 200)
        self.c = [mm(temp) for x in range(3)]
        self.m = random.random()*self.r**2

    def tick(self, screen):
        self.pos += self.vel
        if (self.pos.x-self.r+self.vel.x<0 or self.pos.x+self.r+self.vel.x>DISPLAY[0]):
            self.vel.x = -self.vel.x*Constants.BOUNCE
        if (self.pos.y-self.r+self.vel.y<0 or self.pos.y+self.r+self.vel.y>DISPLAY[1]):
            self.vel.y = -self.vel.y*Constants.BOUNCE

        x = self.pos.x
        y = self.pos.y
        r = self.r

        pygame.draw.circle(screen, self.c, (x, y), r)
        if not(Constants.LDM):
            pygame.draw.circle(screen, (0,0,0), (x, y-r/6+r/8), r*0.6)
            pygame.draw.circle(screen, self.c, (x, y-r/3+r/10), r*0.7)
            pygame.draw.ellipse(screen, (0,0,0), (x+r*0.25-r*0.08, y-r*0.16-r*0.16, r*0.16, r*0.32))
            pygame.draw.ellipse(screen, (0,0,0), (x-r*0.25-r*0.08, y-r*0.16-r*0.16, r*0.16, r*0.32))

def collisions(objects:list[Ball]):
    for i in range(len(objects)):
        a = objects[i]
        for ie in range(i+1, len(objects)):
            b = objects[ie]
            dx=b.pos.x-a.pos.x
            dy=b.pos.y-a.pos.y
            sd=dx*dx+dy*dy
            smallest = a.r + b.r

            if sd == 0:
                dx = 0.01
                dy = 0.01
                sd = dx*dx+dy*dy

            d=math.sqrt(sd)

            if d<smallest:
                nx = dx/d
                ny = dy/d

                rvx = b.vel.x-a.vel.x
                rvy = b.vel.y-a.vel.y
                s=rvx*nx+rvy*ny
                if s>0: continue

                massSum = a.m+b.m
                a.vel.x += 2*b.m/massSum*s*nx*Constants.DAMPEN
                a.vel.y += 2*b.m/massSum*s*ny*Constants.DAMPEN
                b.vel.x -= 2*a.m/massSum*s*nx*Constants.DAMPEN
                b.vel.y -= 2*a.m/massSum*s*ny*Constants.DAMPEN

                overlap = smallest-d
                a.pos.x-=nx*overlap/2
                a.pos.y-=ny*overlap/2
                b.pos.x+=nx*overlap/2
                b.pos.y+=ny*overlap/2    

objects:list[Ball] = [Ball() for x in range(10)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 50))

    collisions(objects)
    for object in objects:
        object.tick(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()