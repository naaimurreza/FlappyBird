import sys
import pygame
import random

import pygame.font


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (550,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (550, random_pipe_pos - 170))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 800:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -90 or bird_rect.bottom >= 680:
        return False
    return True

def rotate_bird(bird):
     return pygame.transform.rotozoom(bird, bird_movement * -3.5, 1)

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (225, bird_rect.centery))
    return new_bird, new_bird_rect

def trade_mark():
    name_surface = name_font.render('@naaimurreza', True, (255,255,255))
    name_rect = name_surface.get_rect(center = (106,23))
    screen.blit(name_surface, name_rect)

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = score_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (225,150))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(225, 150))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(225, 205))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.init()
screen = pygame.display.set_mode((450,800))
clock = pygame.time.Clock()
game_font = pygame.font.Font('FlappyBird.ttf', 40)
name_font = pygame.font.Font('FlappyBird.ttf', 25)
score_font = pygame.font.Font('FlappyBird.ttf', 55)

# Game variables
gravity = 0.16
bird_movement = 0
game_active = False
score = 0
high_score = 0



bg_surface = pygame.image.load('sprites/background-day.png').convert()
#bg_surafce2 = pygame.image.load('sprites/background-day-no.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
bg_x_pos = 0

floor_surface = pygame.image.load('sprites/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 375))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('sprites/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 2250)
pipe_height = [250, 350, 400, 450, 500, 550, 580]

game_over_surface = pygame.transform.scale2x(pygame.image.load('sprites/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (225,300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 5
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (225, 375)
                gravity = 0.16
                bird_movement = -5.5
                score = 0
        if event.type == BIRDFLAP:
            if bird_index < 2:
                 bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())


    bg_x_pos += 0.3
    screen.blit(bg_surface, (bg_x_pos,0))
    screen.blit(bg_surface, (bg_x_pos - 450, 0))
    if bg_x_pos >= 450:
        bg_x_pos = 0

    if game_active:
        #Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        #Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        if len(pipe_list) > 0:
            threshold = pipe_list[len(pipe_list)-1].centerx
            if threshold == 224:
                score += 1

        trade_mark()

        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')


    #Floor
    floor_x_pos -= 1
    screen.blit(floor_surface, (floor_x_pos, 680))
    if floor_x_pos <= -230:
        floor_x_pos = 0
    screen.blit(floor_surface, (floor_x_pos,680))




    pygame.display.update()
    clock.tick(120)


