import pygame

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Game time variables
current_day = 1
current_month = 1
current_year = 2200
days_per_month = 30

# Speed settings
speed_multipliers = {
    "slow": 2.0,     # 1 real second = 0.5 in-game days
    "normal": 1.0,   # 1 real second = 1 in-game day
    "fast": 0.5      # 1 real second = 2 in-game days
}
game_speed = "normal"  # Default speed
seconds_per_day = speed_multipliers[game_speed]

# Time tracking
real_time_accumulator = 0.0

# Game loop variables
running = True
fps = 60  # Frames per second for rendering

while running:
    # Calculate time passed since the last frame
    dt = clock.tick(fps) / 1000.0  # Time in seconds for this frame
    real_time_accumulator += dt  # Accumulate elapsed real time

    # Process Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Change game speed with keys (e.g., 1 for slow, 2 for normal, 3 for fast)
            if event.key == pygame.K_1:
                game_speed = "slow"
                seconds_per_day = speed_multipliers[game_speed]
                print("Game speed set to slow")
            elif event.key == pygame.K_2:
                game_speed = "normal"
                seconds_per_day = speed_multipliers[game_speed]
                print("Game speed set to normal")
            elif event.key == pygame.K_3:
                game_speed = "fast"
                seconds_per_day = speed_multipliers[game_speed]
                print("Game speed set to fast")

    # Simulation time management
    while real_time_accumulator >= seconds_per_day:
        real_time_accumulator -= seconds_per_day
        current_day += 1

        # Check for end of the month
        if current_day > days_per_month:
            current_day = 1
            current_month += 1

            # Check for end of the year
            if current_month > 12:
                current_month = 1
                current_year += 1

            # Trigger the monthly simulation update
            print(f"Simulation update for month {current_month}/{current_year}")

    # Render your game here
    print(f"In-game date: {current_day}/{current_month}/{current_year}")

# Quit Pygame
pygame.quit()
