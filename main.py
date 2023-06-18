import pygame as pg
import sys
import random

WIDTH, HEIGHT = 1200, 670
FPS = 60
G = 1.5
SPEED = 8


class Enemy:
    def __init__(self, obj):
        self.obj = obj
        self.x = WIDTH + random.choice([0, 100, 200])
        self.y = 460 - random.choice([0, 30])

    def get_rect(self, topleft, size):
        return self.obj.get_rect(topleft=topleft, size=size)


pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Game")
icon = pg.image.load("imgs/game.png")
pg.display.set_icon(icon)

background = pg.image.load("imgs/backgr.png").convert()
background = pg.transform.scale(background, (WIDTH, HEIGHT))

enemy_list = []

right_sprites = [
    pg.image.load("imgs/right0.png").convert_alpha(),
    pg.image.load("imgs/right1.png").convert_alpha(),
    pg.image.load("imgs/right2.png").convert_alpha(),
    pg.image.load("imgs/right3.png").convert_alpha()
]
player_speed = 5
player_x = 50
player_y = 400
floor_y = 400
player_v0 = 25
jump_t = 0
is_jump = False

pg.mixer.music.load("sounds/music.mp3")
pg.mixer.music.play(loops=-1)
pg.mixer.music.set_volume(0.1)

floor = pg.Surface((2000, 200))
floor.fill((20, 18, 31))

myfont = pg.font.Font("fonts/RobotoMono-Regular.ttf", 80)
lose_text = myfont.render("Вы проиграли", True, (200, 30, 30))
lose_rect = lose_text.get_rect(center=(600, 200))
restart_text = myfont.render("Начать заново", True, (30, 200, 30))
restart_rect = restart_text.get_rect(center=(600, 400))

clock = pg.time.Clock()

ticks = 0
cd = 150.0

window = "game"
while True:
    if window == "game":
        screen.blit(background, (0, 0))
        screen.blit(floor, (0, 535))

        player_rect = right_sprites[0].get_rect(topleft=(player_x + 10, player_y), size=(60, 110))

        if ticks % int(cd) == 0:
            enemy = Enemy(pg.image.load("imgs/enemy.png").convert_alpha())
            enemy_list.append(enemy)
            SPEED += 0.15
            cd *= 0.995

        for i, enemy in enumerate(enemy_list):
            enemy_rect = enemy.get_rect(topleft=(enemy.x + 10, enemy.y), size=(44, 64))

            if player_rect.colliderect(enemy_rect):
                pg.mixer.music.stop()
                window = "lose"

            screen.blit(enemy.obj, (enemy.x, enemy.y))
            enemy.x -= SPEED

            if enemy.x < -64:
                enemy_list.pop(i)

        if not is_jump:
            screen.blit(right_sprites[ticks % 32 // 8], (player_x, player_y))

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] and player_x > 0:
            player_x -= player_speed
        elif keys[pg.K_RIGHT] and player_x < 700:
            player_x += player_speed

        if keys[pg.K_SPACE] and not is_jump:
            is_jump = True
            jump_t = 0

        if is_jump:
            screen.blit(right_sprites[1], (player_x, player_y))
            player_y = floor_y - player_v0 * jump_t + G * jump_t ** 2 / 2
            jump_t += 1

        if player_y > floor_y:
            is_jump = False
            player_y = floor_y


    elif window == "lose":
        screen.blit(background, (0, 0))
        screen.blit(lose_text, lose_rect)
        screen.blit(restart_text, restart_rect)

        mouse = pg.mouse.get_pos()
        if restart_rect.collidepoint(mouse) and pg.mouse.get_pressed()[0]:
            window = "game"
            pg.mixer.music.play()
            enemy_list.clear()
            player_x = 50
            player_y = 400
            player_v0 = 25
            jump_t = 0
            is_jump = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pg.display.update()

    ticks += 1
    clock.tick(FPS)

