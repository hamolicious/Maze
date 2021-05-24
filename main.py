import pygame
from time import time
from maze import Maze, Debug
from player import Player

#region pygame init
pygame.init()
size = (600, 600)
screen = pygame.display.set_mode(size)
screen.fill([255, 255, 255])
pygame.display.set_icon(screen)
clock, fps = pygame.time.Clock(), 0

delta_time = 0 ; frame_start_time = 0
#endregion

def generate_maze():
	maze = Maze(screen, size, 30)
	player = Player(screen, maze.start_cell, maze)

	return maze, player

maze, player = generate_maze()
key_lock = False

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
	frame_start_time = time()
	screen.fill(0)

	mouse_pos   = pygame.mouse.get_pos()
	mouse_press = pygame.mouse.get_pressed()
	key_press   = pygame.key.get_pressed()

	if key_press[pygame.K_r] and not key_lock:
		maze, player = generate_maze()
		key_lock = True

	if key_press[pygame.K_ESCAPE]:quit()

	if sum(key_press) == 0:
		key_lock = False

	player.update(key_press)

	maze.display()
	player.display()

	pygame.display.update()
	clock.tick(fps)
	delta_time = time() - frame_start_time
	pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')