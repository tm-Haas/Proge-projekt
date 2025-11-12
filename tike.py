import pygame

pygame.init()
screen = pygame.display.set_mode((600, 300))

player_x = 300 #aluse keskpunkt
player_y = 270 #aluse keskpunkt
player_high = 30 
speed = 0.1

bullets =[]
bullet_speed = 0.2
bullet_width = 4
bullet_height = 8

running = True
while running:

    screen.fill((5, 5, 5))

    player_points = [
        (player_x, player_y - player_high), 
        (player_x - player_high // 2, player_y),
        (player_x + player_high // 2, player_y),
    ]

    pygame.draw.polygon(screen, (250, 250, 250), player_points) #kolmnurk

    for bullet in bullets:
        bullet[1] -= bullet_speed
        pygame.draw.rect(screen, (250, 250, 250), bullet)

    pygame.display.update()

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_x - bullet_width // 2, player_y - player_high, bullet_width, bullet_height])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x - player_high // 2 > 0:
        player_x -= speed
    if keys[pygame.K_RIGHT] and player_x + player_high // 2 < 600:
        player_x += speed

pygame.quit()
