import pygame
from pygame.transform import scale
from vector import Vec2d, Color
from random import choice, randint

class Debug:
	mouse_pos = Vec2d()
	mouse_press = []

class Cell:
	def __init__(self, pos, size) -> None:
		self.pos = Vec2d(pos)
		self.size = Vec2d(size)

		self.wall_colour = Color(0)
		self.floor_colour = Color(200)
		self.start_colour = Color(50, 150, 50)
		self.end_colour = Color(150, 50, 50)

		self.is_visited = False
		self.is_start = False
		self.is_end = False

		self.__wall_points = [
			(Vec2d(0, 0) * self.size) + self.pos, # 0
			(Vec2d(1, 0) * self.size) + self.pos, # 1
			(Vec2d(1, 1) * self.size) + self.pos, # 2
			(Vec2d(0, 1) * self.size) + self.pos, # 3
		]
		self.walls = ['up', 'down', 'left', 'right']

	def __draw_wall(self, screen, wall_point1, wall_point2):
		pygame.draw.line(screen, self.wall_colour.get(), wall_point1.get_int(), wall_point2.get_int(), 3)

	def display(self, screen):
		c = self.floor_colour

		if self.is_start : c = self.start_colour
		if self.is_end : c = self.end_colour

		pygame.draw.rect(screen, c.get(), (self.pos.get_int(), self.size.get_int()), 0)

		for wall in self.walls:
			if wall == 'up'    : self.__draw_wall(screen, self.__wall_points[0], self.__wall_points[1])
			if wall == 'down'  : self.__draw_wall(screen, self.__wall_points[3], self.__wall_points[2])
			if wall == 'left'  : self.__draw_wall(screen, self.__wall_points[0], self.__wall_points[3])
			if wall == 'right' : self.__draw_wall(screen, self.__wall_points[1], self.__wall_points[2])

class Maze:
	def __init__(self, screen, screen_size, maze_size) -> None:
		self.screen = screen
		self.screen_size = Vec2d(screen_size)
		self.maze_size = Vec2d(maze_size)

		self.cell_size = self.screen_size.copy()
		self.cell_size.div(self.maze_size)

		self.start_cell = None
		self.end_cell = None

		self.grid = []
		self.__generate_grid()
		self.__generate_maze()

	def __generate_grid(self):
		for y in range(self.maze_size.h):
			row = []
			for x in range(self.maze_size.w):
				cell_pos = Vec2d(x, y) * self.cell_size
				row.append(Cell(cell_pos, self.cell_size))

			self.grid.append(row)

	def get_cell_neighbours(self, pos):
		gx = int(pos.x / self.cell_size.w)
		gy = int(pos.y / self.cell_size.h)

		neighbours = []
		for index in [Vec2d(gx + 1, gy + 0), Vec2d(gx + 0, gy + 1), Vec2d(gx - 1, gy + 0), Vec2d(gx + 0, gy - 1)]:
			if index.x >= 0 and index.x <= self.maze_size.x-1 and index.y >= 0 and index.y <= self.maze_size.y-1:
				neighbours.append(self.grid[index.y][index.x])

		return neighbours

	def __remove_cell_wall(self, cell, wall_name):
		if wall_name in cell.walls:
			cell.walls.remove(wall_name)

	def __break_wall_between_cells(self, cell1, cell2):
		cp1 = cell1.pos
		cp2 = cell2.pos

		if cp1.x == cp2.x and cp1.y > cp2.y: # UP
			self.__remove_cell_wall(cell1, 'up')
			self.__remove_cell_wall(cell2, 'down')

		if cp1.x == cp2.x and cp1.y < cp2.y: # DOWN
			self.__remove_cell_wall(cell1, 'down')
			self.__remove_cell_wall(cell2, 'up')

		if cp1.x > cp2.x and cp1.y == cp2.y: # LEFT
			self.__remove_cell_wall(cell1, 'left')
			self.__remove_cell_wall(cell2, 'right')

		if cp1.x < cp2.x and cp1.y == cp2.y: # RIGHT
			self.__remove_cell_wall(cell1, 'right')
			self.__remove_cell_wall(cell2, 'left')

	def __generate_maze(self):
		stack = []
		initial_cell = self.grid[randint(0, self.maze_size.w-1)][0]
		initial_cell.is_visited = True
		initial_cell.is_start = True
		stack.append(initial_cell)

		end_cell = self.grid[randint(0, self.maze_size.w-1)][self.maze_size.w-1]
		end_cell.is_end = True

		self.start_cell = initial_cell
		self.end_cell = end_cell

		while len(stack) != 0:
			current_cell = stack.pop(-1)
			neighbours = self.get_cell_neighbours(current_cell.pos)

			unviseted_neighbours = [cell for cell in neighbours if not cell.is_visited]

			if len(unviseted_neighbours) > 0:
				stack.append(current_cell)
				chosen_cell = choice(unviseted_neighbours)

				self.__break_wall_between_cells(current_cell, chosen_cell)
				chosen_cell.is_visited = True

				stack.append(chosen_cell)

	def display(self):
		for row in self.grid:
			for cell in row:
				cell.display(self.screen)
