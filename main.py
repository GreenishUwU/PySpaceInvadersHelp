import pygame
from pygame import mixer
pygame.font.init()
import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import math
import random
import time

# set up display #
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Invaders - Remastered")
# initiate game #
pygame.init()

# load aliens #
ALIEN1 = pygame.image.load(os.path.join("sprites","alien1_frame1.png"))
ALIEN2 = pygame.image.load(os.path.join("sprites","alien2_frame1.png"))
ALIEN3 = pygame.image.load(os.path.join("sprites","alien3_frame1.png"))

# load player player #
PLAYER_SHIP = pygame.image.load(os.path.join("sprites", "spaceship.png"))

# projectiles #
LASER = pygame.image.load(os.path.join("sprites","laser3_frame1.png"))

# load background #
BG = pygame.transform.scale(pygame.image.load(os.path.join("sprites","background.png")), (WIDTH,HEIGHT))

# create general class for player and aliens #
class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

# create specific class for players #
class Player(Ship):
    def __init__(self, x,y, health=100):
        super().__init__(x, y, health)
        self.player_img = PLAYER_SHIP
        self.laser_img = LASER
        # mask #
        self.mask = pygame.mask.from_surface(self.player_img)
        self.max_health = health

# create specific class for enemies #
class Enemy(Ship):
    ALIEN_CHOICE = [ALIEN1, ALIEN2, ALIEN3]
    def __init__(self, x, y, color, health=100):
        super().__init__(x,y, health)
        self.ship_img = self.ALIEN_CHOICE[color]
        # mask #
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel): # movement variables for enemies
        self.y += vel 

def main():
    run = True
    FPS = 30
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("Pixeboy", 50) # yes i know that this font is not real, but I was trying to use custom fonts, then realised that the font which python uses when there is no font is the one that I want, so I've decided to just let it be it and do whatever it wants #
    
    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 14

    player = Player(300, 650)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0,0))
        # write test #
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))

        WIN.blit(lives_label, (10,10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i  in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(Enemy.ALIEN_CHOICE))
                enemies.append(enemy)

        # check for quit #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # horizontal controls #
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0: # go left #
            player.x -= player_vel
        
        if keys[pygame.K_RIGHT] and player.x + player_vel + 25 < WIDTH: # go right # no dynamic pixel extension because player.get_width() is annoying #
            player.x += player_vel
        # vertical controls #
        if keys [pygame.K_UP] and player.y - player_vel > 0: # go up #
            player.y -= player_vel
        
        if keys [pygame.K_DOWN] and player.y + player_vel + 25 < HEIGHT: # go down # no dynamic pixel extension because player.get_height() is annoying #
            player.y += player_vel
        
        for enemy in enemies:
            enemy.move(enemy_vel)

        redraw_window()

        
main()