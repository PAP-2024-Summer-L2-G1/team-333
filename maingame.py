from game_funcs import *
import game_engine
import pygame
import sys

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

player_sprite_idle = pygame.image.load(sprite_idle_path)
player_sprite_walk_right1 = pygame.image.load(sprite_walk_right1_path)
player_sprite_walk_right2 = pygame.image.load(sprite_walk_right2_path)
player_sprite_walk_left1 = pygame.image.load(sprite_walk_left1_path)
player_sprite_walk_left2 = pygame.image.load(sprite_walk_left2_path)
player_sprite_right_end = pygame.image.load(sprite_right_end_path)
player_sprite_left_end = pygame.image.load(sprite_left_end_path)
background1 = pygame.image.load(background1_path)
background2 = pygame.image.load(background2_path)
main_menu_background = pygame.image.load(main_menu_background_path)

player_sprite_idle = pygame.transform.scale(player_sprite_idle, (50, 50))
player_sprite_walk_right1 = pygame.transform.scale(player_sprite_walk_right1, (50, 50))
player_sprite_walk_right2 = pygame.transform.scale(player_sprite_walk_right2, (50, 50))
player_sprite_walk_left1 = pygame.transform.scale(player_sprite_walk_left1, (50, 50))
player_sprite_walk_left2 = pygame.transform.scale(player_sprite_walk_left2, (50, 50))
player_sprite_right_end = pygame.transform.scale(player_sprite_right_end, (50, 50))
player_sprite_left_end = pygame.transform.scale(player_sprite_left_end, (50, 50))
background1 = pygame.transform.scale(background1, (WIDTH, HEIGHT))
background2 = pygame.transform.scale(background2, (WIDTH, HEIGHT))
main_menu_background = pygame.transform.scale(main_menu_background, (WIDTH, HEIGHT))

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

main_menu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    moving_right = keys[pygame.K_RIGHT]
    moving_left = keys[pygame.K_LEFT]

    if moving_left and player_pos[0] > left_barrier:
        player_pos[0] -= 5
        walk_timer += 1
        facing_right = False
        if walk_timer >= walk_delay:
            current_walk_sprite = (current_walk_sprite + 1) % len(walk_left_cycle)
            walk_timer = 0
    elif moving_right:
        player_pos[0] += 5
        walk_timer += 1
        facing_right = True
        if walk_timer >= walk_delay:
            current_walk_sprite = (current_walk_sprite + 1) % len(walk_right_cycle)
            walk_timer = 0
    else:
        if on_ground:
            if facing_right:
                current_walk_sprite = len(walk_right_cycle)
            else:
                current_walk_sprite = len(walk_left_cycle)

    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = jump_strength
        on_ground = False

    player_vel_y += gravity
    player_pos[1] += player_vel_y

    if player_pos[1] >= ground_level:
        player_pos[1] = ground_level
        player_vel_y = 0
        on_ground = True

    if player_pos[0] >= right_edge_trigger and current_background == background1:
        current_background = background2
        player_pos[0] = left_edge_trigger + 5
    elif player_pos[0] <= left_edge_trigger and current_background == background2:
        current_background = background1
        player_pos[0] = right_edge_trigger - 5

    screen.blit(current_background, (0, 0))

    if moving_left:
        screen.blit(walk_left_cycle[current_walk_sprite % len(walk_left_cycle)], player_pos)
    elif moving_right:
        screen.blit(walk_right_cycle[current_walk_sprite % len(walk_right_cycle)], player_pos)
    else:
        if on_ground:
            if facing_right:
                screen.blit(player_sprite_right_end, player_pos)
            else:
                screen.blit(player_sprite_left_end, player_pos)
        else:
            if facing_right:
                screen.blit(player_sprite_right_end, player_pos)
            else:
                screen.blit(player_sprite_left_end, player_pos)

    pygame.display.flip()

    clock.tick(FPS)