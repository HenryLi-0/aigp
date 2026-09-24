import pygame
import os
import time
import math
import random
import asyncio

async def main():
    pygame.init()
    pygame.mixer.init()
    DISPLAY = (600, 400)
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("ooo")
    clock = pygame.time.Clock()

    pygame.mixer.music.load(os.path.join("lab 2", "Spring In My Step.mp3"))
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1)

    class Constants:
        PLAYER_HITBOX = (50, 50)
        PLAYER_IMG = pygame.transform.scale(pygame.image.load(os.path.join("lab 2", "player.png")).convert_alpha(), PLAYER_HITBOX)

        COLLECTIBLE_HITBOX = (30, 30)
        COLLECTIBLE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("lab 2", "normal.png")).convert_alpha(), COLLECTIBLE_HITBOX)

        BG = pygame.transform.scale(pygame.image.load(os.path.join("lab 2", "nine paws.png")).convert_alpha(), DISPLAY)
        BG.set_alpha(150)

        GRAVITY = 0.95

    class Map:
        PLATFORMS = [
            pygame.Rect(0, 350, 600, 50),
            pygame.Rect(100, 230, 150, 10),
            pygame.Rect(350, 170, 150, 10),
        ]

        COLLECTIBLES = [(125,200), (175,200), (225,200)] 

        def generateCollectibles(n):
            for x in range(n): 
                Map.COLLECTIBLES.append((
                    random.randint(
                        math.ceil(Constants.COLLECTIBLE_HITBOX[0]/2),
                        math.floor(DISPLAY[0]-Constants.COLLECTIBLE_HITBOX[0]/2)),
                    random.randint(
                        math.ceil(Constants.COLLECTIBLE_HITBOX[1]/2), 350)))
            Map.COLLECTIBLES_HITBOXES = [
                pygame.Rect(
                    int(pos[0]-Constants.COLLECTIBLE_HITBOX[0]/2),
                    int(pos[1]-Constants.COLLECTIBLE_HITBOX[1]/2),
                    Constants.COLLECTIBLE_HITBOX[0],
                    Constants.COLLECTIBLE_HITBOX[1]
                )
                for pos in Map.COLLECTIBLES
            ]

    Map.generateCollectibles(0)

    x = DISPLAY[0]//2
    y = DISPLAY[1]//2
    vx = 0
    vy = 0
    r = Constants.PLAYER_HITBOX[0]//2

    running = True
    ground = False


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            vx -= 0.5
        if keys[pygame.K_RIGHT]:
            vx += 0.5
        if keys[pygame.K_UP] and ground:
            vy = -20

        vy += Constants.GRAVITY
        x += vx
        y += vy

        if x-r<0:
            x=r
            vx*=-0.3

        if x+r>DISPLAY[0]:
            x=DISPLAY[0]-r
            vx*=-0.3

        if y-r<0:
            y=r
            vy*=-0.3

        if y+r>DISPLAY[1]:
            y=DISPLAY[1]-r
            vy=0

        playerRectGen = lambda: pygame.Rect(
            int(x-Constants.PLAYER_HITBOX[0]/2),
            int(y-Constants.PLAYER_HITBOX[1]/2),
            Constants.PLAYER_HITBOX[0],
            Constants.PLAYER_HITBOX[1]
        )
        playerRect = playerRectGen()

        # platform collisions of doom and despair
        ground = False
        for platform in Map.PLATFORMS:
            if playerRect.colliderect(platform):
                if vy >= 0 and playerRect.bottom >= platform.top:
                    y = platform.top - Constants.PLAYER_HITBOX[1] / 2
                    vy = 0
                    ground = True
                elif vy < 0 and playerRect.top <= platform.bottom:
                    y = platform.bottom + Constants.PLAYER_HITBOX[1] / 2
                    vy = 0

        playerRect = playerRectGen()
        
        # side collisions
        for platform in Map.PLATFORMS:
            if playerRect.colliderect(platform):
                if vx > 0:
                    x =platform.left-Constants.PLAYER_HITBOX[0]/2
                    vx = 0
                elif vx < 0:
                    x = platform.right+Constants.PLAYER_HITBOX[0]/2
                    vx = 0


        collected = []
        for i, hitbox in enumerate(Map.COLLECTIBLES_HITBOXES):
            if playerRect.colliderect(hitbox):
                collected.append(i)
                temp = pygame.mixer.Sound(os.path.join("lab 2", "fith {}.wav".format(random.randint(1,3))))
                temp.set_volume(0.2)
                temp.play()

        for i in reversed(collected):
            Map.COLLECTIBLES.pop(i)
            Map.COLLECTIBLES_HITBOXES.pop(i)

        if len(Map.COLLECTIBLES)==0:
            Map.generateCollectibles(random.randint(10,25)*random.randint(10,25))


        color = math.sin(time.time()*10)*50+205
        screen.fill((color, color, color))
        screen.blit(Constants.BG, (0, 0))

        ct = time.time()*2
        cr = int((math.sin(ct) + 1) * 127.5) + 50
        cg = int((math.sin(ct + 2) + 1) * 127.5) + 50
        cb = int((math.sin(ct + 4) + 1) * 127.5) + 50
        safe = lambda x: min(max(0, x), 255)
        for platform in Map.PLATFORMS:
            pygame.draw.rect(screen, (safe(cr), safe(cg), safe(cb)), platform)
        screen.blit(
            Constants.PLAYER_IMG,
            (
                int(x-Constants.PLAYER_HITBOX[0]/2),
                int(y-Constants.PLAYER_HITBOX[1]/2)
            )
        )

        for pos in Map.COLLECTIBLES:
            screen.blit(
                Constants.COLLECTIBLE_IMG,
                (
                    int(pos[0]-Constants.COLLECTIBLE_HITBOX[0]/2),
                    int(pos[1]-Constants.COLLECTIBLE_HITBOX[1]/2)
                )
            )

        vx*=0.99
        vy*=0.99

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()

asyncio.run(main())