import pygame
import pickle
from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60

tile_size = 25
margin = 100
screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')

row = screen_height // tile_size
col = screen_width // tile_size

#load images
sun_img = pygame.image.load('img/sun.png')
sun_img = pygame.transform.scale(sun_img, (tile_size, tile_size))
bg_img = pygame.image.load('img/sky.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
dirt_img = pygame.image.load('img/dirt.png')
grass_img = pygame.image.load('img/grass.png')
blob_img = pygame.image.load('img/blob.png')
platform_x_img = pygame.image.load('img/platform_x.png')
platform_y_img = pygame.image.load('img/platform_y.png')
lava_img = pygame.image.load('img/lava.png')
coin_img = pygame.image.load('img/coin.png')
exit_img = pygame.image.load('img/exit.png')
save_img = pygame.image.load('img/save_btn.png')
load_img = pygame.image.load('img/load_btn.png')

#define game variables
clicked = False
level = 0

#define colours
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

#create empty tile list
world_data = []
for row in range(screen_height//tile_size ):
	r = [0] * (screen_width // tile_size)
	world_data.append(r)


row_count = 0
while row_count <= row:
	col_count = 0
	while col_count < col:
		if row_count == 0 or col_count == col-1 or col_count == 0:
			world_data[row_count][col_count] = 1
		if row_count == row  and col_count != 0 and col_count != col-1:
			world_data[row_count][col_count] = 2
		col_count += 1
	row_count += 1



def draw_world():
	for row in range(screen_height//tile_size):
		for col in range(screen_width // tile_size):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					#dirt blocks
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 2:
					#grass blocks
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 3:
					#enemy blocks
					img = pygame.transform.scale(blob_img, (tile_size, int(tile_size * 0.75)))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
				if world_data[row][col] == 4:
					#horizontally moving platform
					img = pygame.transform.scale(platform_x_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 5:
					#vertically moving platform
					img = pygame.transform.scale(platform_y_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 6:
					#lava
					img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
				if world_data[row][col] == 7:
					#coin
					img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
					screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
				if world_data[row][col] == 8:
					#exit
					img = pygame.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))
					screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))



#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))
	

def draw_grid():
	for c in range(screen_width//tile_size):
		#vertical lines
		pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height))
		#horizontal lines
		pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))
		

running = True
while running:

	clock.tick(fps)

	#draw background
	screen.fill(green)
	screen.blit(bg_img, (0, 0))
	screen.blit(sun_img, (50, 50))

	draw_grid()
	draw_world()
	draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
	draw_text('Press UP or DOWN to change level adn LEFT to save and RIGHT to load', font, white, tile_size, screen_height - 40)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			#check that the coordinates are within the tile area
			if x < col and y <= row:
				#update tile value
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 8:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 8
		
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		#up and down key presses to change level number
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 0:
				level -= 1
			elif event.key == pygame.K_RIGHT:
				if path.exists(f'data/level{level}_data'):
					pickle_in = open(f'data/level{level}_data', 'rb')
					world_data = pickle.load(pickle_in)
			elif event.key == pygame.K_LEFT:
				pickle_out = open(f'data/level{level}_data', 'wb')
				pickle.dump(world_data, pickle_out)
				pickle_out.close()
	pygame.display.update()

pygame.quit()