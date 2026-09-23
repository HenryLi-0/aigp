import pygame
import random
import os

pygame.init()
DISPLAY = (600, 400)
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("ooo")
clock = pygame.time.Clock()

class Constants:
    PLAYER_HITBOX = (50,50)
    PLAYER_IMG = pygame.transform.scale(pygame.image.load(os.path.join("lab 2", "player.png")).convert_alpha(), PLAYER_HITBOX)

    BRAIN_HITBOX = (30, 30)
    BRAIN_IMG = pygame.transform.scale(pygame.image.load(os.path.join("lab 2", "uh brains.png")).convert_alpha(), BRAIN_HITBOX)

    LORD_VERITY = pygame.transform.scale(pygame.image.load(os.path.join("lab 2", "lord verity.png")).convert_alpha().set_alpha(50), DISPLAY)

    GRAVITY = 0.95

class Map:
    PLATFORMS = [
        pygame.Rect(0, 350, 600, 50),
        pygame.Rect(100, 230, 150, 10),
        pygame.Rect(350, 170, 150, 10),
    ]
    COLLECTIBLES = [
        (125,200), (175,200), (225,200),
    ]
    COLLECTIBLES_HITBOXES = [pygame.Rect(pos[0]-Constants.BRAIN_HITBOX[0]/2, pos[1]-Constants.BRAIN_HITBOX[1]/2, Constants.BRAIN_HITBOX[0], Constants.BRAIN_HITBOX[1]) for pos in COLLECTIBLES]



x, y, vx, vy, r = DISPLAY[0]/2, DISPLAY[1]/2, 0, 0, Constants.PLAYER_HITBOX[0]/2
running = True
ground = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if (x-r+vx<0 or x+r+vx>DISPLAY[0]):
        vx = -vx*0.3
    if (y-r+vy<0 or y+r+vy>DISPLAY[1]):
        vy = -vy*0.3


    screen.fill((20, 20, 40))
    screen.blit(Constants.LORD_VERITY, (0,0))

    for hitbox in Map.PLATFORMS:
        pygame.draw.rect(screen, (255, 255, 255), hitbox)
    screen.blit(Constants.PLAYER_IMG, (x-Constants.PLAYER_HITBOX[0]/2, y-Constants.PLAYER_HITBOX[1]/2))
    for pos in Map.COLLECTIBLES:
        screen.blit(Constants.BRAIN_IMG, (pos[0]-Constants.BRAIN_HITBOX[0]/2, pos[1]-Constants.BRAIN_HITBOX[1]/2))

    ground = False
    playerRect=lambda: pygame.Rect(x-Constants.PLAYER_HITBOX[0]/2, y-Constants.PLAYER_HITBOX[0]/2, Constants.PLAYER_HITBOX[0], Constants.PLAYER_HITBOX[1])
    for hitbox in Map.PLATFORMS:
        if playerRect().colliderect(hitbox):
            ground = True
            safe = 0
            vy=0
            while playerRect().colliderect(hitbox) and safe<30:
                y+=-1
                safe+=1
            y+=1

    
    playerTopRect=lambda: pygame.Rect(x-Constants.PLAYER_HITBOX[0]/2, y-Constants.PLAYER_HITBOX[0]/2-25, Constants.PLAYER_HITBOX[0], Constants.PLAYER_HITBOX[1]+25)
    # pygame.draw.rect(screen, (255,0,0), playerTopRect())
    touching = False
    for hitbox in Map.PLATFORMS:
        if playerTopRect().colliderect(hitbox):
            touching = True
    if touching:
        vy=-vy
        y+=vy
        vy*=0.3

    playerSideRect=lambda: pygame.Rect(x-Constants.PLAYER_HITBOX[0]/2-10, y-Constants.PLAYER_HITBOX[0]/2+Constants.PLAYER_HITBOX[0]/3, Constants.PLAYER_HITBOX[0]+20, Constants.PLAYER_HITBOX[1]/3)
    # pygame.draw.rect(screen, (255,0,0), playerSideRect())
    touching = False
    for hitbox in Map.PLATFORMS:
        if playerSideRect().colliderect(hitbox):
            touching = True
    if touching:
        vx=-vx
        x+=vx
        vx*=0.3

    for item in enumerate(Map.COLLECTIBLES_HITBOXES):
        if playerRect().colliderect(item[1]):
            Map.COLLECTIBLES.pop(item[0])
            Map.COLLECTIBLES_HITBOXES.pop(item[0])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        vx -= 0.5
    if keys[pygame.K_RIGHT]:
        vx += 0.5
    if keys[pygame.K_UP] and ground:
        vy += -20
    else: 
        vy+=Constants.GRAVITY

    x+=vx
    y+=vy
    if y>DISPLAY[1]-r: y=DISPLAY[1]-r
    vx*=0.99
    vy*=0.99

    pygame.display.flip()
    clock.tick(60)

