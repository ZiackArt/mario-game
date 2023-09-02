import pygame
from pygame.locals import *

pygame.init()

screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Mario Game")

# Game Variables
tile_size = 25

# load images
sun_img = pygame.image.load("img/sun.png")
bg_img = pygame.image.load("img/sky.png")

def draw_grid():
	for line in range(0, 50):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))



class World():
    def __init__(self, data):
        
        self.tile_list = []
        # load image
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')
        row, col = data
        row_count = 0
        while row_count < row:
            col_count = 0
            while col_count < col:
                # if row_count == 0 or col_count == col-1 or col_count == 0 :
                #     img = pygame.transform.scale(dirt_img,(tile_size,tile_size))
                #     img_rect = img.get_rect()
                #     img_rect.x = col_count * tile_size
                #     img_rect.y = row_count * tile_size
                #     tile = (img, img_rect)
                #     self.tile_list.append(tile)
                if row_count == row - 1 :
                    img = pygame.transform.scale(grass_img,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            print('col ', col_count)
            row_count += 1
        print('row ', row_count)

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
          



# world_data =  [
#       [1,1,1,1,1,1,1,1,1,1],
#       [1,0,0,0,0,0,0,0,0,1],
#       [1,0,0,0,0,0,0,0,0,1],
#       [1,0,0,0,0,0,0,0,0,1],
#       [1,0,0,0,0,0,0,0,0,1],
#       [1,1,1,1,1,1,1,1,1,1]
# ]
world = World([screen_height // tile_size, screen_width // tile_size])

running = True
while running:
    screen.blit(bg_img,(0,0))
    screen.blit(sun_img,(50,50))
    draw_grid()
    world.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running =False
    

    pygame.display.update()

pygame.quit()