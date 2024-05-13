import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Space Invaders")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load player image
player_image = pygame.image.load(r"C:\Users\yeshwanth\Pictures\Python Game\Player.png")
player_image = pygame.transform.scale(player_image, (50, 50))

# Load enemy image
enemy_image = pygame.image.load(r"C:\Users\yeshwanth\Pictures\Python Game\Enemy1.png")
enemy_image = pygame.transform.scale(enemy_image, (50, 50))

# Set up the player
player_width = 50
player_height = 50
player_x = window_width // 2 - player_width // 2
player_y = window_height - player_height - 10
player_speed = 5
player = pygame.Rect(player_x, player_y, player_width, player_height)

# Set up the enemy
enemy_width = 50
enemy_height = 50
enemy_speed = 2
num_enemies = 4  # Number of enemies in each level
enemies = []
for _ in range(num_enemies):
    enemy_x = random.randint(0, window_width - enemy_width)
    enemy_y = random.randint(50, 200)
    enemy = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    enemies.append(enemy)

# Set up the projectile
projectile_width = 5
projectile_height = 20
projectile_speed = 10
projectile = pygame.Rect(0, 0, projectile_width, projectile_height)
projectile_state = "ready"  # "ready" means the projectile is ready to be fired, "fire" means it's moving

# Set up the game clock
clock = pygame.time.Clock()

# Set up game variables
level = 1
score = 0
lives = 3
game_over = False
game_won = False

# Load heart image for lives
heart_image = pygame.image.load(r"C:\Users\yeshwanth\Pictures\Python Game\Heart.png")
heart_image = pygame.transform.scale(heart_image, (30, 30))

# Set up the dotted line
dotted_line_y = player_y + player_height + 10
dotted_line_dash_length = 10
dotted_line_gap_length = 5
dotted_line_x = 0

# Function to handle firing the projectile
def fire_projectile():
    global projectile_state
    if projectile_state == "ready":
        projectile_state = "fire"
        projectile.x = player.x + player.width // 2 - projectile.width // 2
        projectile.y = player.y

# Function to draw player's lives
def draw_lives():
    for i in range(lives):
        window.blit(heart_image, (10 + i * 35, 10))

# Function to draw the level
def draw_level():
    font = pygame.font.Font(None, 30)
    level_text = font.render("Level " + str(level), True, WHITE)
    window.blit(level_text, (window_width - level_text.get_width() - 10, 10))

# Function to draw the real-time score
def draw_score():
    font = pygame.font.Font(None, 30)
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (window_width - score_text.get_width() - 10, 50))

# Function to draw the dotted line
def draw_dotted_line():
    x = dotted_line_x
    while x < window_width:
        pygame.draw.line(window, WHITE, (x, dotted_line_y), (x + dotted_line_dash_length, dotted_line_y), 2)
        x += dotted_line_dash_length + dotted_line_gap_length

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fire_projectile()

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x < window_width - player_width:
        player.x += player_speed

    # Move the enemies
    for enemy in enemies:
        enemy.x += enemy_speed
        if enemy.x < 0 or enemy.x > window_width - enemy_width:
            enemy_speed *= -1
            enemy.y += enemy_height

        # Check if enemy crosses the dotted line
        if enemy.y >= dotted_line_y:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                enemy.x = random.randint(0, window_width - enemy_width)
                enemy.y = random.randint(50, 200)

        # Check for collision between player and enemy
        if player.colliderect(enemy):
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                enemy.x = random.randint(0, window_width - enemy_width)
                enemy.y = random.randint(50, 200)

        # Check for collision between projectile and enemies
        if projectile.colliderect(enemy):
            score += 10
            enemies.remove(enemy)
            projectile_state = "ready"

    # Move the projectile
    if projectile_state == "fire":
        projectile.y -= projectile_speed
        if projectile.y < 0:
            projectile_state = "ready"

    # Check if all enemies are destroyed
    if len(enemies) == 0:
        level += 1
        if level > 5:
            game_won = True
        else:
            num_enemies += 2
            for _ in range(num_enemies):
                enemy_x = random.randint(0, window_width - enemy_width)
                enemy_y = random.randint(50, 200)
                enemy = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
                enemies.append(enemy)

    # Clear the window
    window.fill(BLACK)

    # Draw the player and enemies
    window.blit(player_image, player)
    for enemy in enemies:
        window.blit(enemy_image, enemy)

    # Draw the projectile
    if projectile_state == "fire":
        pygame.draw.rect(window, RED, projectile)

    # Draw the lives and level
    draw_lives()
    draw_level()

    # Draw the real-time score
    draw_score()

    # Draw the dotted line
    draw_dotted_line()

    # Check game over and game won conditions
    if game_over:
        font = pygame.font.Font(None, 50)
        game_over_text = font.render("Game Over", True, WHITE)
        window.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, window_height // 2))
    elif game_won:
        font = pygame.font.Font(None, 50)
        game_won_text = font.render("You Win!", True, WHITE)
        window.blit(game_won_text, (window_width // 2 - game_won_text.get_width() // 2, window_height // 2))

    # Update the display
    pygame.display.update()

    # Set the frames per second
    clock.tick(60)

# Quit the game
pygame.quit()
