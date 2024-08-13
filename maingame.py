from game_funcs import *
import game_engine
import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)

sprite_idle_path = "images/sprite 1.jpg"
sprite_walk_right1_path = "images/sprite 2.jpg"
sprite_walk_right2_path = "images/sprite 3.jpg"
sprite_walk_left1_path = "images/sprite 5.jpg"
sprite_walk_left2_path = "images/sprite 6.jpg"
sprite_right_end_path = "images/sprite 1.jpg"
sprite_left_end_path = "images/sprite 7.jpg"
background1_path = "images/background 1.jpg"
background2_path = "images/background 2.jpg"
main_menu_background_path = "images/zombie_main_menu.jpg"
zombie_idle_path = "images/zombie_idle.jpg"
zombie_walk_path = "images/zombie_walk_right1.jpg"
death_screen_path = "images/death_screen.jpg"
projectile_image_path = "images/projectile.png"

player_sprite_idle = pygame.transform.scale(pygame.image.load(sprite_idle_path), (50, 50))
player_sprite_walk_right1 = pygame.transform.scale(pygame.image.load(sprite_walk_right1_path), (50, 50))
player_sprite_walk_right2 = pygame.transform.scale(pygame.image.load(sprite_walk_right2_path), (50, 50))
player_sprite_walk_left1 = pygame.transform.scale(pygame.image.load(sprite_walk_left1_path), (50, 50))
player_sprite_walk_left2 = pygame.transform.scale(pygame.image.load(sprite_walk_left2_path), (50, 50))
player_sprite_right_end = pygame.transform.scale(pygame.image.load(sprite_right_end_path), (50, 50))
player_sprite_left_end = pygame.transform.scale(pygame.image.load(sprite_left_end_path), (50, 50))
background1 = pygame.transform.scale(pygame.image.load(background1_path), (WIDTH, HEIGHT))
background2 = pygame.transform.scale(pygame.image.load(background2_path), (WIDTH, HEIGHT))
main_menu_background = pygame.transform.scale(pygame.image.load(main_menu_background_path), (WIDTH, HEIGHT))
zombie_idle = pygame.transform.scale(pygame.image.load(zombie_idle_path), (50, 50))
zombie_walk = pygame.transform.scale(pygame.image.load(zombie_walk_path), (50, 50))
death_screen_background = pygame.transform.scale(pygame.image.load(death_screen_path), (WIDTH, HEIGHT))
projectile_image = pygame.transform.scale(pygame.image.load(projectile_image_path), (10, 10))

player_pos = [WIDTH // 2, HEIGHT - 100]
player_vel_y = 0
gravity = 0.5
jump_strength = -10
on_ground = True
walk_right_cycle = [player_sprite_walk_right1, player_sprite_walk_right2]
walk_left_cycle = [player_sprite_walk_left1, player_sprite_walk_left2]
current_walk_sprite = 0
walk_timer = 0
walk_delay = 10
facing_right = True
ground_level = HEIGHT - player_sprite_idle.get_height()
current_background = background1
right_edge_trigger = WIDTH - 10
left_edge_trigger = 10
left_barrier = 0

player_health = 100
zombie_damage = 10
player_speed = 5
zombie_speed = player_speed * 0.6
projectiles = []
zombies = []

def spawn_zombies(num_zombies):
    global zombies
    zombies = []
    used_positions = set()
    min_distance = 150
    for _ in range(num_zombies):
        while True:
            x = random.randint(0, WIDTH - 50)
            y = random.randint(0, HEIGHT - 150)
            if (x, y) not in used_positions:
                distance = ((x - player_pos[0]) ** 2 + (y - player_pos[1]) ** 2) ** 0.5
                if distance > min_distance:
                    used_positions.add((x, y))
                    speed = random.uniform(zombie_speed * 0.5, zombie_speed)
                    zombies.append((pygame.Rect(x, y + (ground_level - y), 50, 50), zombie_idle, speed))
                    break

def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    return
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        screen.blit(main_menu_background, (0, 0))
        start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50)
        pygame.draw.rect(screen, WHITE, start_button)
        pygame.draw.rect(screen, WHITE, quit_button)
        font = pygame.font.SysFont(None, 40)
        start_text = font.render('Start', True, (0, 0, 0))
        quit_text = font.render('Quit', True, (0, 0, 0))
        screen.blit(start_text, (start_button.x + 50, start_button.y + 10))
        screen.blit(quit_text, (quit_button.x + 60, quit_button.y + 10))
        pygame.display.flip()
        clock.tick(FPS)

def death_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if retry_button.collidepoint(mouse_pos):
                    return True
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        screen.blit(death_screen_background, (0, 0))
        retry_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50)
        pygame.draw.rect(screen, WHITE, retry_button)
        pygame.draw.rect(screen, WHITE, quit_button)
        font = pygame.font.SysFont(None, 40)
        retry_text = font.render('Retry', True, (0, 0, 0))
        quit_text = font.render('Quit', True, (0, 0, 0))
        screen.blit(retry_text, (retry_button.x + 50, retry_button.y + 10))
        screen.blit(quit_text, (quit_button.x + 60, quit_button.y + 10))
        pygame.display.flip()
        clock.tick(FPS)

def draw_health_bar(surface):
    pygame.draw.rect(surface, (255, 0, 0), (10, 10, 200, 20))
    pygame.draw.rect(surface, (0, 255, 0), (10, 10, player_health * 2, 20))

def check_zombie_collision():
    global player_health
    player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)
    for zombie, _, _ in zombies:
        if player_rect.colliderect(zombie):
            player_health -= zombie_damage
            if player_health <= 0:
                player_health = 0
                return True
    return False

def check_projectile_collision():
    global zombies
    for projectile in projectiles:
        projectile_rect = pygame.Rect(projectile[0], projectile[1], 10, 10)
        for i, (zombie, _, _) in enumerate(zombies):
            if projectile_rect.colliderect(zombie):
                del zombies[i]
                projectiles.remove(projectile)
                break

def main():
    global player_pos, player_vel_y, gravity, on_ground, current_walk_sprite, walk_timer, walk_delay, facing_right, ground_level, current_background, right_edge_trigger, left_edge_trigger, left_barrier, player_health, zombie_damage, player_speed, zombie_speed, projectiles, zombies

    main_menu()
    spawn_zombies(random.randint(1, 3))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and on_ground:
                    player_vel_y = jump_strength
                    on_ground = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                projectile_dx = 10 if facing_right else -10
                projectile_dy = (mouse_y - (player_pos[1] + player_sprite_idle.get_height() // 2)) // 10
                projectiles.append((player_pos[0] + (50 if facing_right else -10), player_pos[1] + 25, projectile_dx, projectile_dy))

        keys = pygame.key.get_pressed()
        moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]

        if moving_left:
            player_pos[0] -= player_speed
            walk_timer += 1
            facing_right = False
            if walk_timer >= walk_delay:
                current_walk_sprite = (current_walk_sprite + 1) % len(walk_left_cycle)
                walk_timer = 0
        elif moving_right:
            player_pos[0] += player_speed
            walk_timer += 1
            facing_right = True
            if walk_timer >= walk_delay:
                current_walk_sprite = (current_walk_sprite + 1) % len(walk_right_cycle)
                walk_timer = 0
        else:
            if on_ground:
                current_walk_sprite = 0  

        player_vel_y += gravity
        player_pos[1] += player_vel_y

        if player_pos[1] >= ground_level:
            player_pos[1] = ground_level
            player_vel_y = 0
            on_ground = True

        for projectile in projectiles:
            projectile[0] += projectile[2]
            projectile[1] += projectile[3]

        projectiles[:] = [p for p in projectiles if 0 <= p[0] <= WIDTH and 0 <= p[1] <= HEIGHT]

        for i, (zombie_rect, zombie_sprite, speed) in enumerate(zombies):
            if zombie_rect.x < player_pos[0]:
                zombie_rect.x += speed
            elif zombie_rect.x > player_pos[0]:
                zombie_rect.x -= speed
            if zombie_rect.y < player_pos[1]:
                zombie_rect.y += speed
            elif zombie_rect.y > player_pos[1]:
                zombie_rect.y -= speed
            zombies[i] = (zombie_rect, zombie_sprite, speed)

        check_projectile_collision()

        if check_zombie_collision():
            if death_screen():
                player_health = 100
                spawn_zombies(random.randint(1, 3))
            else:
                pygame.quit()
                sys.exit()

        if player_pos[0] >= right_edge_trigger:
            current_background = background2
            player_pos[0] = left_edge_trigger
        elif player_pos[0] <= left_edge_trigger and current_background == background2:
            current_background = background1
            player_pos[0] = right_edge_trigger

        screen.blit(current_background, (0, 0))
        if facing_right:
            screen.blit(walk_right_cycle[current_walk_sprite] if moving_right else player_sprite_right_end, player_pos)
        else:
            screen.blit(walk_left_cycle[current_walk_sprite] if moving_left else player_sprite_left_end, player_pos)
        for projectile in projectiles:
            screen.blit(projectile_image, (projectile[0], projectile[1]))
        for zombie, zombie_sprite, _ in zombies:
            screen.blit(zombie_sprite, zombie.topleft)
        draw_health_bar(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
