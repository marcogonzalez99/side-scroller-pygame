import pygame
import sys
from random import randint


def display_score():
    current_time = int((pygame.time.get_ticks() - start_time)/10)
    score_surface = test_font.render(
        f'Score:{current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    global enemy_speed
    enemy_speed *= 1.001
    enemy_speed = min(35, enemy_speed)
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= enemy_speed
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [
            obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


def collision(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 300:
        # Display the jump surface when not on surface
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]
        # Play walking animation if player is on surface


# General Setup
pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D Side-Scroller")
game_active = False
start_time = 0
score = 0
enemy_speed = 10
bg_music = pygame.mixer.Sound('music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops=-1)

test_font = pygame.font.Font("Pixeltype.ttf", 50)

# Surfaces
sky_surface = pygame.image.load("Images/sky.png").convert_alpha()
ground_surface = pygame.image.load("Images/ground.png").convert_alpha()

# score_surface = test_font.render("My Game", False, (64, 64, 64))
# score_rect = score_surface.get_rect(center=(400, 50))

go_surface = test_font.render("Game Over", False, (64, 64, 64))
go_rect = go_surface.get_rect(center=(400, 50))

# Snail Image / Obstacles
snail_frame1 = pygame.image.load("Images/snail1.png").convert_alpha()
snail_frame2 = pygame.image.load("Images/snail2.png").convert_alpha()
snail_frames = [snail_frame1, snail_frame2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]
# Fly Image / Obstacles
fly_frame1 = pygame.image.load("Images/Fly1.png").convert_alpha()
fly_frame2 = pygame.image.load("Images/Fly2.png").convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []

# Player Models
player_walk_1 = pygame.image.load("Images/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("Images/player_walk_2.png").convert_alpha()
player_jump = player_walk_1 = pygame.image.load(
    "Images/jump.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0

player_surface = player_walk[player_index]

player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

# Game Over/Intro Screen
player_stand = pygame.image.load('Images/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('Pixel Runners', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press Space to Start', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 320))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -15
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -15
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_time = int(pygame.time.get_ticks())
                game_active = True
                enemy_speed = 10

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surface.get_rect(
                        bottomright=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(
                        bottomright=(randint(900, 1100), 210)))
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]

    if game_active:
        screen.blit(sky_surface, (0, 0))  # Drawing the sky
        screen.blit(ground_surface, (0, 300))  # Drawing the ground
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity

        # Keeping player above ground
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rect)

        # Obstacles
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collision(player_rect, obstacle_rect_list)
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()  # Removing the list to restart the game
        player_rect.midbottom = (80, 300)  # Placing player on the ground
        player_gravity = 0  # Making it so he doesnt fall

        score_message = test_font.render(
            f"Your Score: {score}", False, (111, 196, 169))

        score_message_rect = score_message.get_rect(center=(400, 330))
        if score != 0:
            screen.blit(score_message, score_message_rect)
        else:
            screen.blit(game_message, game_message_rect)

        screen.blit(game_name, game_name_rect)

    pygame.display.update()
    clock.tick(60)
