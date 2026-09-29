import pygame
import random
import sys
import math

pygame.init()

DISPLAY = (1000, 600)
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("asteroids but i gave you a swerve rocket")
clock = pygame.time.Clock()

class Constants:
    BG = (20, 11, 55)
    GRAVITY = 0.08
    BOUNCE = 1
    LDM = True
    COLLISION_DAMPEN = 0.5

    COLLISION_LEEWAY = 100

    class Drive:
        ACCEL_MUL = 0.075
        OMEGA_MUL = 0.175

        SWERVE = True
        DAMPEN = 0.99

class Drive:
    def __init__(self):
        self.hitbox = (20, 30)
        
        self.p = pygame.math.Vector2(DISPLAY[0]//2, DISPLAY[1]//2)
        self.v = pygame.math.Vector2(0,0)
        self.a = pygame.math.Vector2(0,0)
        self.h = 0
        self.o = 0
        self.aa = 0

    def tick(self):
        self.p+=self.v
        self.v+=self.a
        self.a=pygame.math.Vector2(0,0)
        
        self.h+=self.o
        self.o+=self.aa
        self.h%=360

        self.v*=Constants.Drive.DAMPEN
        self.o*=Constants.Drive.DAMPEN

        # self.p.x%=DISPLAY[0]
        # self.p.y%=DISPLAY[1]
        if self.p.x%DISPLAY[0]!=self.p.x: self.v.x*=-1
        if self.p.y%DISPLAY[1]!=self.p.y: self.v.y*=-1

class Boom:
    def __init__(self, pos, heading, speed=8):
        self.p = pygame.math.Vector2(pos)
        self.v = pygame.math.Vector2(0, -speed).rotate(heading)
        self.life = math.sqrt(DISPLAY[0]**2+DISPLAY[1]**2)

    def tick(self, screen):
        self.p += self.v
        self.life -= 1

        pygame.draw.circle(
            screen,
            (255, 245, 125),
            (int(self.p.x), int(self.p.y)),
            2
        )
        if self.p.x%DISPLAY[0]!=self.p.x: self.life=0
        if self.p.y%DISPLAY[1]!=self.p.y: self.life=0

class Asteroid:
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

class Collisions:
    def asteroids(objects:list[Asteroid]):
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
                    a.vel.x += 2*b.m/massSum*s*nx*Constants.COLLISION_DAMPEN
                    a.vel.y += 2*b.m/massSum*s*ny*Constants.COLLISION_DAMPEN
                    b.vel.x -= 2*a.m/massSum*s*nx*Constants.COLLISION_DAMPEN
                    b.vel.y -= 2*a.m/massSum*s*ny*Constants.COLLISION_DAMPEN

                    overlap = smallest-d
                    a.pos.x-=nx*overlap/2
                    a.pos.y-=ny*overlap/2
                    b.pos.x+=nx*overlap/2
                    b.pos.y+=ny*overlap/2
    def boom(booms, objects):
        for boom in booms:
            for ball in objects:
                dx = boom.p.x-ball.pos.x
                dy = boom.p.y-ball.pos.y

                if dx*dx + dy*dy < (ball.r*ball.r+Constants.COLLISION_LEEWAY):
                    boom.life = 0
                    objects.remove(ball)
                    break

objects:list[Asteroid] = [Asteroid() for x in range(10)]
booms:list[Boom] = []
player = Drive()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_k:
                booms.append(Boom(player.p + pygame.math.Vector2(0, -player.hitbox[1] / 2).rotate(player.h), player.h))

    keys = pygame.key.get_pressed()

    if Constants.Drive.SWERVE:
        player.a = pygame.math.Vector2((keys[pygame.K_d] or keys[pygame.K_RIGHT])-(keys[pygame.K_a] or keys[pygame.K_LEFT]), (keys[pygame.K_s] or keys[pygame.K_DOWN])-(keys[pygame.K_w] or keys[pygame.K_UP]))*Constants.Drive.ACCEL_MUL
        player.aa = (keys[pygame.K_l]-keys[pygame.K_j])*Constants.Drive.OMEGA_MUL
    else:
        player.a = pygame.math.Vector2(0, -(keys[pygame.K_w] or keys[pygame.K_UP])).rotate(player.h)*Constants.Drive.ACCEL_MUL
        player.aa = ((keys[pygame.K_d] or keys[pygame.K_RIGHT])-(keys[pygame.K_a] or keys[pygame.K_LEFT]))*Constants.Drive.OMEGA_MUL

        

    screen.fill((30, 30, 50))
    pygame.draw.polygon(screen, (255,255,255), [
        player.p + pygame.math.Vector2(0, -player.hitbox[1]/2).rotate(player.h),
        player.p + pygame.math.Vector2(-player.hitbox[0]/2, player.hitbox[1]/2).rotate(player.h),
        player.p + pygame.math.Vector2(player.hitbox[0]/2, player.hitbox[1]/2).rotate(player.h)
    ])
    # pygame.draw.polygon(screen, (255,200,200), [
    #     player.p + pygame.math.Vector2(0, player.hitbox[1]/2).rotate(player.h),
    #     player.p + pygame.math.Vector2(-player.hitbox[0]/4, player.hitbox[1]).rotate(player.h),
    #     player.p + pygame.math.Vector2(player.hitbox[0]/4, player.hitbox[1]).rotate(player.h)
    # ])

    player.tick()
    Collisions.asteroids(objects)
    Collisions.boom(booms, objects)
    for object in objects:
        object.tick(screen)
    for boom in booms:
        if boom.life > 0:
            boom.tick(screen)
        else:
            booms.remove(boom)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()