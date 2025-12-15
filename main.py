import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Create a screen
screen = pygame.display.set_mode((1300, 700))

# Title and icon
pygame.display.set_caption("Gym Cat by Meow")
icon = pygame.image.load('cool.png')
pygame.display.set_icon(icon)

# Set colors
background_color = (135, 206, 235)  # Sky Blue
border_color = (0, 0, 0)  # Black
border_thickness = 10

# Load images
player_image = pygame.image.load('kitty.png')  # Player image
point_image = pygame.image.load('dumble.png')  # Point image
enemy_image = pygame.image.load('burgir.png')  # Enemy image
front_window_image = pygame.image.load('cat.png')  # Image to display above the title

# Game duration in seconds
GAME_DURATION = 60 # 1 minutes

# Function to reset game variables
def reset_game():
    global player_x, player_y, player_width, player_height, score, points, point_timers, enemy_timers, game_over, game_won, start_time
    player_width = player_image.get_width()
    player_height = player_image.get_height()
    player_x = 650  # Center the player horizontally
    player_y = 350  # Center the player vertically
    score = 0
    points = 15  # At least 15 points on the screen
    point_timers = []  # List to keep track of points and their timers
    enemy_timers = []  # List to keep track of enemies and their timers
    generate_points_and_enemies()

    start_time = time.time()  # Record the start time of the game
    game_over = False
    game_won = False  # Reset game won/lost state

# Function to generate points and enemies randomly
def generate_points_and_enemies():
    global point_timers, enemy_timers
    point_timers = []
    enemy_timers = []

    # Generate points
    for _ in range(points):
        point_x = random.randint(20, 1300 - 20)
        point_y = random.randint(20, 700 - 20)
        point_timers.append((point_x, point_y, time.time()))  # Add the current time for the point

    # Generate enemies
    for _ in range(15):  # At least 15 enemies on screen
        enemy_x = random.randint(20, 1300 - 20)
        enemy_y = random.randint(20, 700 - 20)
        enemy_timers.append((enemy_x, enemy_y, time.time()))  # Add the current time for the enemy

# Function to regenerate points and enemies after they disappear
def regenerate_point_or_enemy():
    global point_timers, enemy_timers
    if len(point_timers) < points:
        point_x = random.randint(20, 1300 - 20)
        point_y = random.randint(20, 700 - 20)
        point_timers.append((point_x, point_y, time.time()))  # Respawn new point after disappearance

    if len(enemy_timers) < 15:
        enemy_x = random.randint(20, 1300 - 20)
        enemy_y = random.randint(20, 700 - 20)
        enemy_timers.append((enemy_x, enemy_y, time.time()))  # Respawn new enemy after disappearance

# Initial game state
reset_game()

# Main loop
running = True
game_started = False
while running:
    # Fill the background with a color (sky blue in this case)
    screen.fill(background_color)

    if not game_started:
        # Display the front window image above the title
        front_window_rect = front_window_image.get_rect(center=(650, 150))  # Position the image at the top center
        screen.blit(front_window_image, front_window_rect)

        # Display game title
        font_title = pygame.font.Font(None, 100)  # Bigger font for the title
        title_text = font_title.render("Gym Cat by Meow", True, (0, 0, 65))  # Game name
        title_rect = title_text.get_rect(center=(650, 250))  # Centered title below the image
        screen.blit(title_text, title_rect)

        # Display game description
        font_desc = pygame.font.Font(None, 48)  # Smaller font for the description
        desc_text = font_desc.render("This game is for all gym lovers. I hope you like it!", True, (251, 0, 0))
        desc_rect = desc_text.get_rect(center=(650, 350))  # Centered description
        screen.blit(desc_text, desc_rect)

        # Display instruction to start the game
        font_start = pygame.font.Font(None, 40)  # Instruction text font
        start_text = font_start.render("Press ENTER to Start", True, (0, 0, 65))
        start_rect = start_text.get_rect(center=(650, 450))
        screen.blit(start_text, start_rect)

        # Event handling for starting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Check for ENTER key
                    game_started = True
                    start_time = time.time()  # Reset the start time when the game starts
    else:
        # Calculate elapsed time and remaining time
        elapsed_time = time.time() - start_time
        remaining_time = max(0, GAME_DURATION - elapsed_time)

        # Check if time is over and display result
        if remaining_time == 0 and score < 50:
            game_over = True
            game_won = False  # Player lost
        elif score >= 30:
            game_over = True
            game_won = True  # Player won

        # Draw borders
        pygame.draw.rect(screen, border_color, (0, 0, 1300, 700), border_thickness)

        # Draw player
        screen.blit(player_image, (player_x, player_y))

        # Get the current time for checking expiration of points and enemies
        current_time = time.time()

        # Draw points and check for expiration
        for point_x, point_y, created_time in point_timers[:]:  # Iterate over a copy
            if current_time - created_time < 7:  # If the point is still valid (within 7 seconds)
                screen.blit(point_image, (point_x - 10, point_y - 10))  # Center the point
            else:
                point_timers.remove((point_x, point_y, created_time))  # Remove expired point

        # Regenerate points if necessary
        regenerate_point_or_enemy()

        # Draw enemies and check for expiration
        for enemy_x, enemy_y, created_time in enemy_timers[:]:  # Iterate over a copy
            if current_time - created_time < 7:  # If the enemy is still valid (within 7 seconds)
                screen.blit(enemy_image, (enemy_x - 10, enemy_y - 10))  # Center the enemy
            else:
                enemy_timers.remove((enemy_x, enemy_y, created_time))  # Remove expired enemy

        # Regenerate enemies if necessary
        regenerate_point_or_enemy()

        # Display score in the top right corner
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        text_rect = score_text.get_rect(topright=(1280, 10))  # Positioning the score
        screen.blit(score_text, text_rect)

        # Display the timer in the top left corner
        timer_text = font.render(f"Time Left: {int(remaining_time)}s", True, (0, 0, 0))
        timer_rect = timer_text.get_rect(topleft=(10, 10))  # Positioning the timer
        screen.blit(timer_text, timer_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_x -= 5
            if keys[pygame.K_RIGHT]:
                player_x += 5
            if keys[pygame.K_UP]:
                player_y -= 5
            if keys[pygame.K_DOWN]:
                player_y += 5

            # Keep player within borders
            player_x = max(border_thickness, min(player_x, 1300 - border_thickness - player_width))
            player_y = max(border_thickness, min(player_y, 700 - border_thickness - player_height))

            # Check for collision with points
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
            for point in point_timers[:]:  # Iterate over a copy
                point_x, point_y, created_time = point
                point_rect = pygame.Rect(point_x - 10, point_y - 10, 20, 20)
                if player_rect.colliderect(point_rect):
                    score += 1
                    point_timers.remove(point)  # Remove the collected point
                    regenerate_point_or_enemy()  # Immediately regenerate a new point

            # Check for collision with enemies (reduce score)
            for enemy in enemy_timers[:]:  # Iterate over a copy
                enemy_x, enemy_y, created_time = enemy
                enemy_rect = pygame.Rect(enemy_x - 10, enemy_y - 10, 20, 20)
                if player_rect.colliderect(enemy_rect):
                    score -= 1
                    enemy_timers.remove(enemy)  # Remove the enemy on collision
                    regenerate_point_or_enemy()  # Immediately regenerate a new enemy

        # Handle game over and win scenarios
        if game_over:
            # Display win or lose message
            if game_won:
                end_text = font.render("You Win! Press R to Restart", True, (0, 0, 0))
            else:
                end_text = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
            end_rect = end_text.get_rect(center=(650, 350))
            screen.blit(end_text, end_rect)

            # Event handling for restarting the game
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:  # Check if R key is pressed to restart
                reset_game()
                game_started = False

    pygame.display.update()

# Quit Pygame
pygame.quit()
