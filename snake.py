import pygame
import os
import random

pygame.init()

WIDTH, HEIGHT = 900, 500
SNAKE_WIDTH, SNAKE_HEIGHT = 40, 40



pygame.display.set_caption("Snake Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (75,0,130)
GREEN = (0, 100, 0)
RED = (255, 0, 0)
FPS = 8

HIGHSCORE = 0

TEXT_FONT = pygame.font.SysFont("comicsans", 40)

APPLE_EATEN = pygame.USEREVENT + 1
DEAD = pygame.USEREVENT + 2

BACKGROUND = pygame.Rect(0, 0, WIDTH, HEIGHT)
GRID = pygame.transform.scale(
    pygame.image.load("snake_background.png"), (400, 400)
)


def handle_movement(direction, snake):
    previous_position_x = 0
    previous_position_y = 0
    current_position_x = 0
    current_position_y = 0
    for i in range(len(snake)):
        

        if i == 0:
            previous_position_x, previous_position_y = snake[i].x, snake[i].y
            new_position_x, new_position_y = previous_position_x, previous_position_y
            colision = False
            if direction == 'R':
                new_position_x += SNAKE_WIDTH
            if direction == 'L':
                new_position_x -= SNAKE_WIDTH
            if direction == 'U':
                new_position_y -= SNAKE_WIDTH
            if direction == 'D':
                new_position_y += SNAKE_WIDTH

            if new_position_x < 0 or new_position_x > 360 or new_position_y < 0 or new_position_y > 360:
                pygame.event.post(pygame.event.Event(DEAD))
                return
            for part in snake:
                if part.collidepoint(new_position_x, new_position_y):
                    pygame.event.post(pygame.event.Event(DEAD))
                    return
            else:
                snake[0].x = new_position_x
                snake[0].y = new_position_y
        else:
            # Store current position
            current_position_x = snake[i].x
            current_position_y = snake[i].y

            # Move bodypart forward
            snake[i].x = previous_position_x
            snake[i].y = previous_position_y

            # Reset for next bodypart
            previous_position_x = current_position_x
            previous_position_y = current_position_y

def apple_eaten(snake, apple):
    if apple.colliderect(snake[0]):
        pygame.event.post(pygame.event.Event(APPLE_EATEN))
        
        # Extending snake
        last_part = snake[-1]
        second_last_part = snake[-2]
        
        dx = last_part.x - second_last_part.x
        dy = last_part.y - second_last_part.y

        new_part_x = last_part.x + dx
        new_part_y = last_part.y + dy
        new_part = pygame.Rect(new_part_x, new_part_y, SNAKE_WIDTH, SNAKE_WIDTH)
        snake.append(new_part)

        # Repositioning apple outside of snake
        available_tiles = []
        for i in range(10):
            for j in range(10):
                tile_occupied = False
                for part in snake:
                    if part.collidepoint(i * SNAKE_WIDTH, j * SNAKE_WIDTH):
                        tile_occupied = True
                        break
                if not tile_occupied:
                    available_tiles.append((i, j))
        if available_tiles:
            position_index = random.randint(0, len(available_tiles) - 1)
            new_position = available_tiles[position_index]

            apple.x = new_position[0] * SNAKE_WIDTH
            apple.y = new_position[1] * SNAKE_WIDTH
            
            pygame.display.update()
        
    
def game_over():
    play_again = pygame.Rect(WIDTH//2, HEIGHT//2, )

def draw_window(snake, apple, points):
    pygame.draw.rect(screen, GREEN, BACKGROUND)

    screen.blit(GRID, (0, 0))
    pygame.draw.rect(screen, RED, apple)

    score_text = TEXT_FONT.render(
        "Score: " + str(points), 1, (255, 255, 255)
    )
    screen.blit(score_text, (GRID.get_width() + 50, 50))
    color = 1
    for part in snake:
        if color:
          pygame.draw.rect(screen, BLUE, part)
          color = 0
        else:
          pygame.draw.rect(screen, (75,0,130), part)
          color = 1

    pygame.display.update()


def main():
    run = True
    apple = pygame.Rect(200 + 3 * SNAKE_WIDTH, 200, SNAKE_WIDTH, SNAKE_HEIGHT)
    snake = []
    for i in range(3): 
      snake.append(pygame.Rect(80 - i * SNAKE_WIDTH, 200, SNAKE_WIDTH, SNAKE_HEIGHT))
    
    
    direction = 'R'
    last_direction = 'R'

    points = 0
    change_direction = []

    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)

        # Handling of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                # Directions = ['U', 'D', 'L', 'R']

                if event.key == pygame.K_RIGHT and last_direction != 'L':
                    change_direction.append('R')
                    last_direction = 'R'
                if event.key == pygame.K_LEFT and last_direction != 'R':
                    change_direction.append('L')
                    last_direction = 'L'
                if event.key == pygame.K_UP and last_direction != 'D':
                    change_direction.append('U')
                    last_direction = 'U'
                if event.key == pygame.K_DOWN and last_direction != 'U':
                    change_direction.append('D')
                    last_direction = 'D'
            # Handling eating of apple
            if event.type == APPLE_EATEN:
                points += 1

            if event.type == DEAD:
                HIGHSCORE = points
                run = False
                pygame.time.delay(3000)
                main()


        if change_direction:
            direction = change_direction[0]
            change_direction.pop(0)

        handle_movement(direction, snake)        
        apple_eaten(snake, apple)
        
        draw_window(snake, apple, points)

    pygame.quit()


if __name__ == "__main__":
    main()
