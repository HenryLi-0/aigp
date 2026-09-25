import pygame
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

    try:
        pygame.mixer.music.load("assets/Spring_In_My_Step.ogg")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
    except:
        print("sonion ring (no audio)")

    PLAYER_HITBOX = (50, 50)
    PLAYER_IMG = pygame.transform.scale(pygame.image.load("assets/player.png").convert_alpha(), PLAYER_HITBOX)

    COLLECTIBLE_HITBOX = (30, 30)
    COLLECTIBLE_IMG = pygame.transform.scale(pygame.image.load("assets/normal.png").convert_alpha(), COLLECTIBLE_HITBOX)

    BG = pygame.transform.scale(pygame.image.load("assets/nine_paws.png").convert_alpha(), DISPLAY)
    BG.set_alpha(150)

    GRAVITY = 0.95

    FITH = [pygame.mixer.Sound("assets/fith_{}.ogg".format(x)) for x in range(1, 3+1)]
    for sound in FITH: sound.set_volume(0.2)

    PLATFORMS = [
        pygame.Rect(0, 350, 600, 50),
        pygame.Rect(100, 230, 150, 10),
        pygame.Rect(350, 170, 150, 10),
    ]

    COLLECTIBLES = [(125,200), (175,200), (225,200)] 
    COLLECTIBLES_HITBOXES = []

    def generateCollectibles(n):
        nonlocal COLLECTIBLES_HITBOXES
        for x in range(n): 
            COLLECTIBLES.append((
                random.randint(
                    math.ceil(COLLECTIBLE_HITBOX[0]/2),
                    math.floor(DISPLAY[0]-COLLECTIBLE_HITBOX[0]/2)),
                random.randint(
                    math.ceil(COLLECTIBLE_HITBOX[1]/2), 350)))
        COLLECTIBLES_HITBOXES = [
            pygame.Rect(
                int(pos[0]-COLLECTIBLE_HITBOX[0]/2),
                int(pos[1]-COLLECTIBLE_HITBOX[1]/2),
                COLLECTIBLE_HITBOX[0],
                COLLECTIBLE_HITBOX[1]
            )
            for pos in COLLECTIBLES
        ]

    generateCollectibles(0)

    x = DISPLAY[0]//2
    y = DISPLAY[1]//2
    vx = 0
    vy = 0
    r = PLAYER_HITBOX[0]//2

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

        vy += GRAVITY
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
            int(x-PLAYER_HITBOX[0]/2),
            int(y-PLAYER_HITBOX[1]/2),
            PLAYER_HITBOX[0],
            PLAYER_HITBOX[1]
        )
        playerRect = playerRectGen()

        # platform collisions of doom and despair
        ground = False
        for platform in PLATFORMS:
            if playerRect.colliderect(platform):
                if vy >= 0 and playerRect.bottom >= platform.top:
                    y = platform.top - PLAYER_HITBOX[1] / 2
                    vy = 0
                    ground = True
                elif vy < 0 and playerRect.top <= platform.bottom:
                    y = platform.bottom + PLAYER_HITBOX[1] / 2
                    vy = 0

        playerRect = playerRectGen()
        
        # side collisions
        for platform in PLATFORMS:
            if playerRect.colliderect(platform):
                if vx > 0:
                    x =platform.left-PLAYER_HITBOX[0]/2
                    vx = 0
                elif vx < 0:
                    x = platform.right+PLAYER_HITBOX[0]/2
                    vx = 0


        collected = []
        for i, hitbox in enumerate(COLLECTIBLES_HITBOXES):
            if playerRect.colliderect(hitbox):
                collected.append(i)
                FITH[random.randint(0, len(FITH)-1)].play()

        for i in reversed(collected):
            COLLECTIBLES.pop(i)
            COLLECTIBLES_HITBOXES.pop(i)

        if len(COLLECTIBLES)==0:
            generateCollectibles(random.randint(10,25)*random.randint(10,25))


        color = math.sin(time.time()*10)*50+205
        screen.fill((color, color, color))
        screen.blit(BG, (0, 0))

        ct = time.time()*2
        cr = int((math.sin(ct) + 1) * 127.5) + 50
        cg = int((math.sin(ct + 2) + 1) * 127.5) + 50
        cb = int((math.sin(ct + 4) + 1) * 127.5) + 50
        safe = lambda x: min(max(0, x), 255)
        for platform in PLATFORMS:
            pygame.draw.rect(screen, (safe(cr), safe(cg), safe(cb)), platform)
        screen.blit(
            PLAYER_IMG,
            (
                int(x-PLAYER_HITBOX[0]/2),
                int(y-PLAYER_HITBOX[1]/2)
            )
        )

        for pos in COLLECTIBLES:
            screen.blit(
                COLLECTIBLE_IMG,
                (
                    int(pos[0]-COLLECTIBLE_HITBOX[0]/2),
                    int(pos[1]-COLLECTIBLE_HITBOX[1]/2)
                )
            )

        vx*=0.99
        vy*=0.99

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.mixer.music.stop()
    pygame.quit()

asyncio.run(main())