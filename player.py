import pygame
from vector import Vec2d, Color

class Player:
	def __init__(self, screen, start_cell, maze) -> None:
		self.screen = screen
		self.current_cell = start_cell
		self.pos = self.__get_center_of_cell()
		self.maze = maze

		self.player_width = 0.3

		self.color = Color()

		self.key_lock = False

	def __get_center_of_cell(self, cell=None):
		if cell is None:
			center_pos = self.current_cell.size.copy()
		else:
			center_pos = cell.size.copy()

		center_pos.div(2)
		center_pos.add(self.current_cell.pos)

		return center_pos

	def update(self, key_press):
		if sum(key_press) == 0:
			self.key_lock = False

		gx = int(self.current_cell.pos.x / self.maze.cell_size.w)
		gy = int(self.current_cell.pos.y / self.maze.cell_size.h)

		if key_press[pygame.K_w] and not self.key_lock and 'up' not in self.current_cell.walls:
			self.key_lock = True
			gy -= 1
		if key_press[pygame.K_a] and not self.key_lock and 'left' not in self.current_cell.walls:
			self.key_lock = True
			gx -= 1
		if key_press[pygame.K_s] and not self.key_lock and 'down' not in self.current_cell.walls:
			self.key_lock = True
			gy += 1
		if key_press[pygame.K_d] and not self.key_lock and 'right' not in self.current_cell.walls:
			self.key_lock = True
			gx += 1

		if gx < 0 : gx = 0
		if gx > self.maze.maze_size.w-1 : gx = self.maze.maze_size.w-1
		if gy < 0 : gy = 0
		if gy > self.maze.maze_size.h-1 : gy = self.maze.maze_size.h-1

		self.current_cell = self.maze.grid[gy][gx]
		self.pos.linear_interpolate(self.__get_center_of_cell())

	def display(self):
		pygame.draw.circle(self.screen, self.color.get(), self.pos.get_int(), self.current_cell.size.w * self.player_width)




