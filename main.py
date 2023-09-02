from typing import Any
import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

pygame.mixer.pre_init(44100, -16,2,512)
mixer.init()
pygame.init()
clock = pygame.time.Clock()
fps = 70

screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Mario Game")

# Define font
font = pygame.font.SysFont('Bauhaus 93',70)
font_score = pygame.font.SysFont('Bauhaus 93', 25)
font_level = pygame.font.SysFont('Bauhaus 93', 18)

#Return max levels fonction
def max_level():
    max = 0
    while path.exists(f'data/level{max}_data'):
        max += 1
    max -= 1
    return max

#Define colors
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)
vert = (0,255,0)
black = (0,0,0)
# Game Variables
tile_size = 25
game_over = 0
main_menu = True
max_levels = max_level()
score = 0
level = 0
if path.exists('data/complet_data'):
    pickle_in = open('data/complet_data', 'rb')
    last_level = pickle.load(pickle_in)
    if level < last_level:
        level = last_level
# load images
sun_img = pygame.image.load("img/sun.png")
bg_img = pygame.image.load("img/sky.png")
restart_img = pygame.image.load('img/restart_btn.png')

start_img = pygame.image.load("img/start_btn.png")
start_img = pygame.transform.scale(start_img, (150,60))

exit_img = pygame.image.load("img/exit_btn.png")
exit_img = pygame.transform.scale(exit_img, (150,60))

princess_started = pygame.image.load("img/princess_started.png")
princess_started = pygame.transform.scale(princess_started, (500,610))

logo_img = pygame.image.load("img/logo.png")
logo_img = pygame.transform.scale(logo_img, (500, 500))

studio_img = pygame.image.load("img/studio.png")
studio_img = pygame.transform.scale(studio_img, (100, 50))
#  load sounds
## background music
pygame.mixer.music.load("sounds/music.wav")
pygame.mixer.music.play(-1,0.0,500)

coin_fx = pygame.mixer.Sound("sounds/coin.wav")
coin_fx.set_volume(0.5)

jump_fx = pygame.mixer.Sound("sounds/jump.wav")
jump_fx.set_volume(0.5)

game_over_fx = pygame.mixer.Sound("sounds/game_over.wav")
game_over_fx.set_volume(0.5)

lava_die_fx = pygame.mixer.Sound("sounds/zingspls.wav")
lava_die_fx.set_volume(0.2)

blob_sound_fx = pygame.mixer.Sound("sounds/balk_2.mp3")
blob_sound_fx.set_volume(0.5)

player_next_level_sound_fx = pygame.mixer.Sound("sounds/glurt_4.mp3")
player_next_level_sound_fx.set_volume(1)
# fonction
def see_you_soon():
    # draw_text('SEE YOU SOON!', font_score,white, (screen_width // 2) - 60, screen_height //1.5 )
    pass
def write_curent_level(level):
    pickle_out = open(f'data/complet_data', 'wb')
    pickle.dump(level, pickle_out)
    pickle_out.close()

def format_score(score):
    if score <= 9:
        score = '000'+str(score)
    elif  score <= 99:
        score = '00'+str(score)
    elif score <= 999 :
        score = "0"+str(score)
    else :
        score = str(score)
    return score

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))

def draw_grid():
	for line in range(0, 50):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

def reset_level(level):
    player.reset(50,screen_height-300)
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()
    platform_group.empty()
    
    if path.exists(f'data/level{level}_data'):
        pickle_in = open(f'data/level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    return world

class Button():
    def __init__(self, x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        screen.blit(self.image, self.rect)
        return action

class Player():
    def __init__(self, x, y):
        self.reset(x,y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 8
        col_thresh = 20
        
        if game_over == 0:
            #get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_r]:
                global score 
                score = 0
                reset_level(level)
                
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                

            # Handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]




            # add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y


            #Check for collision
            self.in_air = True
            for tile in world.tile_list:
                #check for collission in x direction
            
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the groun jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y =0
                    # check if below the groun falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False ):
                game_over = -1
                
                game_over_fx.play()

            #check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False ):
                game_over = -1
                lava_die_fx.play()
                game_over_fx.play()

            #check for collision with exitl
            if pygame.sprite.spritecollide(self, exit_group, False ):
                game_over = 1
                player_next_level_sound_fx.play()


            #check for collision with platforms
            for platform in platform_group:
                #collision in the x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #collision in the y direction
                if platform.rect.colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
                    #below
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False 
                        dy = 0
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction
                
            # udate palyer coordinates
            self.rect.x += dx
            self.rect.y += dy


            # if self.rect.bottom > screen_height:
            #     self.rect.bottom = screen_height
            #     dy = 0

        elif game_over == -1:
            self.image = self.dead_image
            draw_text('GAME OVER!', font,red, (screen_width // 2) - 190, screen_height //2 - 80 )
            if self.rect.y > 40 :
                self.rect.y -= 3

        #draw player into screen
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255,255,255), self.rect,2)
        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,5):
            img_right = pygame.image.load(f"img/guy{num}.png")
            img_right = pygame.transform.scale(img_right, (22,42))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load("img/ghost.png")
        self.dead_image = pygame.transform.scale(self.dead_image, (42,42))
        self.image = self.images_right[self.index]

        # self.image = pygame.transform.scale(img, (20,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

class World():
    def __init__(self, data):
        
        self.tile_list = []
        # load image
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 2)
                    blob_group.add(blob)
                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size,1,0)
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size , 0 , 1)
                    platform_group.add(platform)
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + 1 + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count  * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size//2))
                    exit_group.add(exit)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
            # pygame.draw.rect(screen, (255,255,255), tile[1],2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/blob.png")
        self.image = pygame.transform.scale(self.image, (30,20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter= 0

    def update(self):

        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 20:
            self.move_direction *= -1
            self.move_counter *= -1

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y,move_x,move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("img/platform.png")
        self.image = pygame.transform.scale(img, (tile_size,tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter= 0
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 20:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("img/lava.png")
        self.image = pygame.transform.scale(img, (tile_size,tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("img/coin.png")
        self.image = pygame.transform.scale(img, (tile_size // 2 ,tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("img/exit.png")
        self.image = pygame.transform.scale(img, (tile_size,int(tile_size * 1.5) ))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


player = Player(50,screen_height-300)

blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# create ummy coin for showing the score 
# score_coin = Coin(tile_size, tile_size )
# coin_group.add(score_coin)
# load data

if path.exists(f'data/level{level}_data'):
    pickle_in = open(f'data/level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

# create Button
restart_button = Button(screen_width // 2 - 50  , screen_height //2 + 20 , restart_img)
start_btn = Button(screen_width // 2 - 250   , screen_height //2 + 220 , start_img)
exit_btn = Button(screen_width // 2  + 60 , screen_height //2 + 220, exit_img)

running = True
while running:
    clock.tick(fps)
    screen.blit(bg_img,(0,0))
    screen.blit(sun_img,(50,50))
    # draw_grid()

    if main_menu:
        # screen.blit(princess_started, (  , ))
        screen.blit(logo_img, (tile_size +220 , tile_size - 20) )
        screen.blit(studio_img,(screen_width // 2 - 70, screen_height // 1.5 + 90) )
        # draw_text('WELCOME TO LINA GAME ', font,black, (screen_width // 3) - 193, screen_height //2 - 80 )
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            main_menu = False
            blob_sound_fx.play()
            pygame.time.delay(200)
        if start_btn.draw():
            main_menu = False
            blob_sound_fx.play()
            pygame.time.delay(200)
        if exit_btn.draw():
            see_you_soon()
            running = False
    else:

        world.draw()
        
        if game_over == 0:
            blob_group.update()
            platform_group.update()
            # update score 
            #check if a coin has been collected
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()
                
            draw_text("X" + format_score(score), font_score, white, tile_size + 2, 22)
            draw_text("Level  " + str(level), font_level, black, tile_size + 2 , 45)


        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        # if player has died 
        if game_over == -1:
            key = pygame.key.get_pressed()
            if restart_button.draw() or key[pygame.K_RETURN] or key[pygame.K_SPACE] :
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0
        # if player has completed the the level 
        elif game_over == 1:
            #reset and go to next level
            level += 1
            if level <=  max_levels:
                # reset level 
                world_data = []
                world = reset_level(level)
                game_over = 0
                write_curent_level(level)
            else :
                draw_text('YOU WIN!', font,blue, (screen_width // 2) - 140, screen_height //2 - 80 )
                if restart_button.draw():
                    level = 0
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0
                    write_curent_level(level)

        game_over = player.update(game_over)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            see_you_soon()
            running =False
    

    pygame.display.update()

pygame.time.delay(500)
pygame.quit()