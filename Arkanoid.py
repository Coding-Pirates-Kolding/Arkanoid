import pygame
import sys

# Game constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 60, 10
BALL_DIAMETER = 10
BRICK_WIDTH, BRICK_HEIGHT = 60, 15

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Game objects
paddle = pygame.Rect(WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_DIAMETER, BALL_DIAMETER)
bricks = [pygame.Rect(i * (BRICK_WIDTH + 2), j * (BRICK_HEIGHT + 2), BRICK_WIDTH, BRICK_HEIGHT) for i in range(WIDTH // (BRICK_WIDTH + 2)) for j in range(5)]
dx, dy = 3, -3

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= 5
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += 5

    # Move ball
    ball.left += dx
    ball.top += dy

    # Collide with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        dx = -dx
    if ball.top <= 0:
        dy = -dy

    # Collide with paddle
    if ball.colliderect(paddle):
        dy = -dy

    # Collide with bricks
    hit_index = ball.collidelist(bricks)
    if hit_index != -1:
        hit_brick = bricks.pop(hit_index)
        dx = -dx if hit_brick.left < ball.left < hit_brick.right or hit_brick.left < ball.right < hit_brick.right else dx
        dy = -dy if hit_brick.top < ball.top < hit_brick.bottom or hit_brick.top < ball.bottom < hit_brick.bottom else dy

    # Game over
    if ball.bottom >= HEIGHT or not bricks:
        break

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.rect(screen, WHITE, ball)
    for brick in bricks:
        pygame.draw.rect(screen, BLUE, brick)
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.wait(1000 // 60)
