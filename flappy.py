import pygame
import sys
import random


def draw_floor():
    window.blit(floor_image, (floor_x_pos, 600))
    window.blit(floor_image, (floor_x_pos + 576, 600))

def create_obstacle():
    random_pipe_pos = random.choice(obstacle_height)
    bottom_obstacle = obstacle_image.get_rect(midtop = (800, random_pipe_pos))
    top_obstacle = obstacle_image.get_rect(midbottom = (800, random_pipe_pos - 200))
    return bottom_obstacle, top_obstacle

def move_obstacles(obstacles):
    for obstacle in obstacles:
        obstacle.centerx -= 5
    return obstacles

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        if obstacle.bottom >= 700:
            window.blit(obstacle_image, obstacle)
        else:
            flip_obstacle = pygame.transform.flip(obstacle_image, False, True)
            window.blit(flip_obstacle, obstacle)

def remove_obstacles(obstacles):
    for obstacle in obstacles:
        if obstacle.centerx == -600:
            obstacles.remove(obstacle)
    return obstacles

def check_collision(obstacles):
    for obstacle in obstacles:
        if bird_rect.colliderect(obstacle):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False
    return True

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
	return new_bird,new_bird_rect

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		window.blit(score_surface,score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		window.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,850))
		window.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score


pygame.init()
window = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Flappy Bird")
#Frames per second(or pictures) infulence how fast a game runs
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)


# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

#loading images in the game
bg_image = pygame.image.load('assets/background-day.png').convert()
#Tranforming the image to fully fit in the game window
trans_image = pygame.transform.scale(bg_image, (700, 700))

floor_image = pygame.image.load('assets/base.png')
floor_image = pygame.transform.scale2x(floor_image)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_image = bird_frames[bird_index]
bird_rect = bird_image.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

obstacle_image = pygame.image.load('assets/pipe-green.png').convert()
obstacle_image = pygame.transform.scale2x(obstacle_image)
obstacle_list = []
SPAWNOBSTACLE = pygame.USEREVENT
pygame.time.set_timer(SPAWNOBSTACLE, 1200)
obstacle_height = [350, 375, 400, 500, 450]

game_over_image = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_image.get_rect(center = (288,512))



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                obstacle_list.clear()
                bird_rect.center = (100,512)
                bird_movement = 0
                score = 0
        
        if event.type == SPAWNOBSTACLE:
            obstacle_list.extend(create_obstacle())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
                
            bird_image,bird_rect = bird_animation()
     
    window.blit(trans_image, (0, 0))


    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_image)
        bird_rect.centery += bird_movement
        window.blit(rotated_bird, bird_rect)
        game_active = check_collision(obstacle_list)

        obstacle_list = move_obstacles(obstacle_list)
        obstacle_list = remove_obstacles(obstacle_list)
        draw_obstacles(obstacle_list)

        score += 0.01
        score_display('main_game')
    
    else:
        window.blit(game_over_image,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120) #120 frames per second
