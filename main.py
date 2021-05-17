import pygame
import sys
import random
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

pygame.mouse.set_visible(0)

WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0, 128)
BLUE = (0, 0, 255, 128)
YELLOW = (255, 255, 0, 128)
BACKGROUND_COLOR = (0, 0, 0, 128)


player_size = 30
player_pos = [WIDTH/2 - player_size/2, HEIGHT - player_size * 2]


enemy_size = 50
#enemy_pos = [random.randint(0, WIDTH-enemy_size), 0]
enemy_list = []
enemies_num = 10


vel = 10
SPEED = 10
score = 0

rocketImg = pygame.image.load("rocket2.png")
rocketImg = pygame.transform.scale(rocketImg, (player_size, player_size * 4))



screen = pygame.display.set_mode((WIDTH, HEIGHT))

myFont = pygame.font.SysFont("monospace", 30)

pygame.display.set_caption("Spadające kwadraty")

clock = pygame.time.Clock()

anotherSurface = screen.convert_alpha()

trackImg = pygame.image.load("track.png")

pygame.mouse.set_visible(0)

FPS = 30

running = True


def create_enemies():
    delay = random.random()
    if len(enemy_list) <= enemies_num and delay < 0.2:
        x_pos = random.randrange(0, WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def draw_enemies():
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))


def update_enemy_pos():
    global score
    for idx, enemy_pos in enumerate(enemy_list):
        if HEIGHT > enemy_pos[1] >= 0:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1


def collision_check():
    for enemy_pos in enemy_list:
        p_x = player_pos[0]
        p_y = player_pos[1]
        e_x = enemy_pos[0]
        e_y = enemy_pos[1]
        if p_x < e_x < (p_x + player_size) or e_x < p_x < (e_x + enemy_size):
            if p_y < (e_y + enemy_size) < (p_y + player_size) or p_y < e_y < (p_y + player_size):
                pygame.display.update()
                print(score)
                pygame.quit()
                sys.exit()

def set_level():
    global SPEED
    if score <= 50:
        SPEED = SPEED
    if 50 < score <= 100:
        SPEED = 12
    if 100 < score <= 200:
        SPEED = 14
    if 200 < score <= 300:
        SPEED = 16
    if 300 < score <= 400:
        SPEED = 18
    if 400 < score <= 500:
        SPEED = 20


while running:

    collision_check()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    x = player_pos[0]
    y = player_pos[1]
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
    if keys[pygame.K_LEFT] and x <= vel:
        x -= x
    if keys[pygame.K_RIGHT] and x < WIDTH - player_size - vel:
        x += vel
    if keys[pygame.K_RIGHT] and (WIDTH - (x + player_size)) <= vel:
        x += WIDTH - (x + player_size)
    player_pos = [x, y]

    screen.fill(BACKGROUND_COLOR)

    set_level()
    create_enemies()
    draw_enemies()
    update_enemy_pos()
    screen.blit(rocketImg, (player_pos[0], player_pos[1]))
    #screen.blit(anotherSurface, (0, 0))


    text_score = "Score:" + str(score)
    text_speed = "Speed:" + str(SPEED * 100) + "km/h!"
    label_score = myFont.render(text_score, 1, YELLOW)
    label_speed = myFont.render(text_speed, 1, YELLOW)
    screen.blit(label_score, (WIDTH - 200, HEIGHT - 40))
    screen.blit(label_speed, (0, HEIGHT - 40))

    #pygame.draw.rect(anotherSurface, RED, (player_pos[0], player_pos[1], player_size, player_size))

    pygame.display.update()

    clock.tick(FPS)
