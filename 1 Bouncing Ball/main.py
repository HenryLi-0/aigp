import pygame
import random

pygame.init()

DISPLAY = (600, 400)
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("ooo")
clock = pygame.time.Clock()

x, y, vx, vy, r = 300, 200, -50, 30, 24
running = True

# yellow, red, blue, pink
COLORS = [(254, 221, 16), (254, 16, 16), (16, 103, 254), (254, 16, 183)]
color = COLORS[0]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if (x-r+vx<0 or x+r+vx>DISPLAY[0]):
        vx = -vx*0.9
        temp = color
        while temp==color:
            color = COLORS[random.randint(0, len(COLORS)-1)]
    if (y-r+vy<0 or y+r+vy>DISPLAY[1]):
        vy = -vy*0.9

    screen.fill((20, 20, 40))

    pygame.draw.circle(screen, color, (x, y), r)
    pygame.draw.circle(screen, (0,0,0), (x, y-r/6+r/8), r*0.6)
    pygame.draw.circle(screen, color, (x, y-r/3+r/10), r*0.7)
    pygame.draw.ellipse(screen, (0,0,0), (x+r*0.25-r*0.08, y-r*0.16-r*0.16, r*0.16, r*0.32))
    pygame.draw.ellipse(screen, (0,0,0), (x-r*0.25-r*0.08, y-r*0.16-r*0.16, r*0.16, r*0.32))

    vy+=0.5
    x+=vx
    y+=vy
    if y>DISPLAY[1]-r: y=DISPLAY[1]-r
    vx*=0.99
    vy*=0.99

    pygame.display.flip()
    clock.tick(60)

pygame.quit()