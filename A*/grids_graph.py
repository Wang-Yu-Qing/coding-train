# pylint: disable=no-member
"""
normal grid colour: white
close set grid colour: red
open set grid colour: yellow
wall grid colour: black
path grid colour: blue
"""
import pygame
import sys
from math import sqrt
import random

class grid(object):
    def __init__(self, x, y, w):
        # x, y for top left pixle
        self.x, self.y = x, y
        self.center_x, self.center_y = self.x + w/2 - 1, self.y + w/2 -1
        self.index_x, self.index_y = int(self.x/w), int(self.y/w)
        self.w = w
        self.col = (255, 255, 255)
        self.f, self.h, self.g = 0, 0, 0
        self.neighbours = []
        self.parent = None
        self.wall = False
        if random.random() < 0.3:
            self.wall = True
            self.col = (0, 0, 0)

    def show(self, screen):
        # for i in range(self.x, self.x + self.w):
        #     for j in range(self.y, self.y + self.w):
        #         screen.set_at((i, j), self.col)
        [[screen.set_at((i, j), self.col) for j in range(self.y, self.y + self.w)] for i in range(self.x, self.x + self.w)]




class grids_graph(object):
    def __init__(self, width, height, grid_width):
        self.width, self.height = width, height
        self.grid_width = grid_width
        self.n_grids_x, self.n_grids_y = int(self.width/self.grid_width), int(self.height/self.grid_width)
        self.grids = []

    def init_grids(self):
        # init grid in each pixle
        for i in range(self.n_grids_x):
            self.grids.append([])
            for j in range(self.n_grids_y):
                self.grids[i].append(grid(i * self.grid_width, j * self.grid_width, self.grid_width))
        # add neighbours (grid object, distance) after all grids are initilized
        for i in range(self.n_grids_x):
            for j in range(self.n_grids_y):
                if j - 1 >= 0: # top
                    self.grids[i][j].neighbours.append((self.grids[i][j-1], 1))
                if j + 1 < self.n_grids_y: # down
                    self.grids[i][j].neighbours.append((self.grids[i][j+1], 1))
                if i - 1 >= 0: # left
                    self.grids[i][j].neighbours.append((self.grids[i-1][j], 1))
                if i + 1 < self.n_grids_x: # right
                    self.grids[i][j].neighbours.append((self.grids[i+1][j], 1))
                # diags:
                if (i + 1 < self.n_grids_x) and (j + 1 < self.n_grids_y):
                    self.grids[i][j].neighbours.append((self.grids[i+1][j+1], sqrt(2)))
                if (i + 1 < self.n_grids_x) and (j - 1 >= 0):
                    self.grids[i][j].neighbours.append((self.grids[i+1][j-1], sqrt(2)))
                if (i - 1 >= 0) and (j + 1 < self.n_grids_y):
                    self.grids[i][j].neighbours.append((self.grids[i-1][j+1], sqrt(2)))
                if (i - 1 >= 0) and (j - 1 >= 0):
                    self.grids[i][j].neighbours.append((self.grids[i-1][j-1], sqrt(2)))
    
    def show_grids(self, screen):
        # for col in self.grids:
        #     for g in col:
        #         g.show(screen)
        [[g.show(screen) for g in col] for col in self.grids]

class A_star_search(object):
    def __init__(self, graph, start, end):
        self.graph = graph
        self.open_set = []
        self.close_set = []
        # make sure the start and end is not wall
        self.start_grid = self.graph.grids[start[0]][start[1]]
        self.start_grid.wall = False
        self.start_grid.col = (0, 255, 100)
        self.end_grid = self.graph.grids[end[0]][end[1]]
        self.end_grid.wall = False
        self.end_grid.col = (0, 255, 100)
        pygame.init()
        self.screen = pygame.display.set_mode((graph.width, graph.height))
        self.bg_color = (255, 255, 255)
        self.search_finished = False

    def find_lowest_f_grid_index(self):
        result = 0
        for i in range(len(self.open_set)):
            if self.open_set[i].f < self.open_set[result].f:
                result = i
        return result

    @staticmethod
    def mark_path(grid, print_path):
        if print_path:
            print('({}, {})'.format(grid.index_x, grid.index_y), end = '<-')
        grid.col = (0, 0, 255)
        last = grid.parent
        while last:
            if print_path:
                print('({},{})'.format(last.index_x, last.index_y), end = '<-')
            last.col = (0, 0, 255)
            last = last.parent

    def heuristic(self, g1, g2):
        p1 = g1.center_x, g1.center_y
        p2 = g2.center_x, g2.center_y
        # don't overestimates
        return sqrt(abs(p1[0] - p2[0])**2 + abs(p1[1] - p2[1])**2)/self.graph.grid_width

    def recolor_close_set(self):
        for g in self.close_set:
            g.col = (200, 100, 0)

    def run_search(self):
        self.start_grid.f = self.heuristic(self.start_grid, self.end_grid)
        self.open_set.append(self.start_grid)
        while True:
            if self.search_finished:
                #print('finish!')
                pass
            else:
                # remove current path
                self.recolor_close_set()
                # A* searching --------------------------------------------------------------
                if not self.open_set:
                    print('Path not found!')
                    self.search_finished = True
                    continue
                current_index = self.find_lowest_f_grid_index()
                current = self.open_set[current_index]
                # show current path, remove below
                self.mark_path(current, print_path = False)
                if current == self.end_grid:
                    print('Path found!')
                    self.mark_path(current, print_path = True)
                    self.search_finished = True
                else:
                    self.open_set.pop(current_index)
                    self.close_set.append(current)
                    for n, d in current.neighbours:
                        if (n in self.close_set) or (n.wall):
                            continue
                        if n not in self.open_set:
                            self.open_set.append(n)
                            n.col = (0, 255, 0)
                            old_n_g = float('inf')
                        else:
                            old_n_g = n.g
                        if current.g + d < old_n_g: # distance to travel from current node to this neighbour
                            n.g = current.g + d
                            n.parent = current
                            n.f = n.g + self.heuristic(n, self.end_grid)
                # -----------------------------------------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit() # quit the whole program
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.screen.fill(self.bg_color)
            # show grids colours
            self.graph.show_grids(self.screen)
            pygame.display.flip()


if __name__ == "__main__":
    graph = grids_graph(800, 600, 10)
    graph.init_grids()
    A_star = A_star_search(graph, (0, 0), (15, 10))
    A_star.run_search()