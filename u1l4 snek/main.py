'''this code was pulled straight from the lesson notes, i did not write this, the lesson did'''

import pygame
import random
import sys

# 1. Initialize Pygame
pygame.init()

# 2. Grid and Window Constants
GRID_SIZE = 20
GRID_COUNT = 20
WINDOW_SIZE = GRID_SIZE * GRID_COUNT  # 400x400 pixels

# 3. Create the Canvas
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# 4. Color Definitions (RGB Format)
BACKGROUND_COLOR = (30, 30, 40)
SNAKE_COLOR = (46, 204, 113)
FOOD_COLOR = (231, 76, 60)

# Snake Setup: Starts at grid coordinates (5, 10) with a 3-block body length
snake_body = [[5, 10], [4, 10], [3, 10]]
snake_direction = "RIGHT"  # Options: "UP", "DOWN", "LEFT", "RIGHT"

# Food Setup: Places food at a random grid block
food_position = [random.randint(0, GRID_COUNT - 1), random.randint(0, GRID_COUNT - 1)]

# 5. Core Game Loop Flag
running = True

while running:
    # Handle Close Window Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Capture Keystrokes
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake_direction != "DOWN":
                snake_direction = "UP"
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake_direction != "UP":
                snake_direction = "DOWN"
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake_direction != "RIGHT":
                snake_direction = "LEFT"
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake_direction != "LEFT":
                snake_direction = "RIGHT"

    # 1. Compute New Head Position
    head_x, head_y = snake_body[0][0], snake_body[0][1]
    if snake_direction == "UP":
        head_y -= 1
    elif snake_direction == "DOWN":
        head_y += 1
    elif snake_direction == "LEFT":
        head_x -= 1
    elif snake_direction == "RIGHT":
        head_x += 1
    new_head = [head_x, head_y]

    # 2. Lose Condition A: Out-of-bounds walls collision
    if head_x < 0 or head_x >= GRID_COUNT or head_y < 0 or head_y >= GRID_COUNT:
        print("💥 Game Over: You hit the wall!")
        running = False
        continue

    # 3. Lose Condition B: Self-cannibalism collision
    if new_head in snake_body:
        print("💥 Game Over: You bit yourself!")
        running = False
        continue

    # Insert the new calculated head position
    snake_body.insert(0, new_head)

    # 4. Growth Mechanic: Check if snake consumes food
    if new_head == food_position:
        # Spawn new random food item
        food_position = [random.randint(0, GRID_COUNT - 1), random.randint(0, GRID_COUNT - 1)]
    else:
        # If no food is eaten, remove tail segment to maintain proper length
        snake_body.pop()


    # Clear screen with background color
    screen.fill(BACKGROUND_COLOR)

    # Render Food Block (Multiply grid coordinates by block scale size)
    food_rect = pygame.Rect(food_position[0] * GRID_SIZE, food_position[1] * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2)
    pygame.draw.rect(screen, FOOD_COLOR, food_rect)

    # Render Snake Body blocks
    for segment in snake_body:
        segment_rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2)
        pygame.draw.rect(screen, SNAKE_COLOR, segment_rect)


    # Render changes onto the screen
    pygame.display.flip()
    
    clock.tick(10)  # Controls game speed (10 frames per second)

pygame.quit()
sys.exit()
