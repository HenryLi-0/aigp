import pygame
import random
import math

pygame.init()

DISPLAY = (600, 400)
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("lots of smiley faces")
clock = pygame.time.Clock()

running = True

class Constants:
    # yellow, red, blue, pink
    COLORS = [(254, 221, 16), (254, 16, 16), (16, 103, 254), (254, 16, 183)]
    GRAVITY = 0.08
    BOUNCE = 1.2
    LDM = True
    DAMPEN = 0.5

class Ball:
    def __init__(self, normal = True):
        self.normal = normal
        if normal:
            self.r = (random.random()**2)*7+2
            self.x = random.uniform(self.r, DISPLAY[0]-self.r)
            self.y = random.uniform(self.r, DISPLAY[1]-self.r)
            self.vx = random.random()*3-1.5
            self.vy = random.random()*3-1.5
            self.c = Constants.COLORS[random.randint(0, len(Constants.COLORS)-1)]
            self.m = random.random()*self.r**2
        else:
            self.r = 24
            self.x = DISPLAY[0]/2
            self.y = DISPLAY[1]/2
            self.vx = 0
            self.vy = 0
            self.c = Constants.COLORS[0]
            self.m = 20000

    def tick(self, screen):
        self.x+=self.vx
        self.y+=self.vy
        if (self.x-self.r+self.vx<0 or self.x+self.r+self.vx>DISPLAY[0]):
            self.vx = -self.vx*Constants.BOUNCE
        if (self.y-self.r+self.vy<0 or self.y+self.r+self.vy>DISPLAY[1]):
            self.vy = -self.vy*Constants.BOUNCE

        x = self.x
        y = self.y
        r = self.r

        pygame.draw.circle(screen, self.c, (x, y), r)
        if not(Constants.LDM) or not(self.normal):
            pygame.draw.circle(screen, (0,0,0), (x, y-r/6+r/8), r*0.6)
            pygame.draw.circle(screen, self.c, (x, y-r/3+r/10), r*0.7)
            pygame.draw.ellipse(screen, (0,0,0), (x+r*0.25-r*0.08, y-r*0.16-r*0.16, r*0.16, r*0.32))
            pygame.draw.ellipse(screen, (0,0,0), (x-r*0.25-r*0.08, y-r*0.16-r*0.16, r*0.16, r*0.32))

def gravity(objects:list[Ball]):
    for i in range(len(objects)):
        a = objects[i]
        for ie in range(i+1, len(objects)):
            b = objects[ie]
            dx=b.x-a.x
            dy=b.y-a.y
            sd=dx*dx+dy*dy

            smallest = a.r + b.r
            sd = max(sd, smallest**2)
            d = math.sqrt(sd)

            force = Constants.GRAVITY * a.m * b.m / sd
            nx = dx/d
            ny = dy/d

            a.vx += force*nx/a.m
            a.vy += force*ny/a.m
            b.vx -= force*nx/b.m
            b.vy -= force*ny/b.m

def collisions(objects:list[Ball]):
    for i in range(len(objects)):
        a = objects[i]
        for ie in range(i+1, len(objects)):
            b = objects[ie]
            dx=b.x-a.x
            dy=b.y-a.y
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

                rvx = b.vx-a.vx
                rvy = b.vy-a.vy
                s=rvx*nx+rvy*ny
                if s>0: continue

                massSum = a.m+b.m
                a.vx += 2*b.m/massSum*s*nx*Constants.DAMPEN
                a.vy += 2*b.m/massSum*s*ny*Constants.DAMPEN
                b.vx -= 2*a.m/massSum*s*nx*Constants.DAMPEN
                b.vy -= 2*a.m/massSum*s*ny*Constants.DAMPEN

                overlap = smallest-d
                a.x-=nx*overlap/2
                a.y-=ny*overlap/2
                b.x+=nx*overlap/2
                b.y+=ny*overlap/2    

objects:list[Ball] = [Ball() for x in range(200)]
objects.append(Ball(False))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((20, 20, 40))

    gravity(objects)
    collisions(objects)
    for object in objects:
        object.tick(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()