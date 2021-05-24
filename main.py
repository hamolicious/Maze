import pygame
from time import time
from maze import Maze, Debug

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
	return Maze(screen, size, 30)

maze = generate_maze()
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
		maze = generate_maze()
		key_lock = True

	if key_press[pygame.K_ESCAPE]:quit()

	if sum(key_press) == 0:
		key_lock = False

	Debug.mouse_pos = None
	Debug.mouse_press = mouse_press

	maze.display()

	pygame.display.update()
	clock.tick(fps)
	delta_time = time() - frame_start_time
	pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')