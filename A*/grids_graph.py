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
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.col = (255, 255, 255)
        self.f, self.h, self.g = 0, 0, 0
        self.neighbours = []
        self.parent = None
        self.wall = False
        if random.random() < 0.3:
            self.wall = True
            self.col = (0, 0, 0)

class grids_graph(object):
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.grids = []

    def init_grids(self):
        # init grid in each pixle
        for i in range(self.width):
            self.grids.append([])
            for j in range(self.height):
                self.grids[i].append(grid(i, j))

        # add neighbours after all grids are initilized
        for i in range(self.width):
            for j in range(self.height):
                if j - 1 >= 0:
                    self.grids[i][j].neighbours.append(self.grids[i][j-1])
                if j + 1 < self.height:
                    self.grids[i][j].neighbours.append(self.grids[i][j+1])
                if i - 1 >= 0:
                    self.grids[i][j].neighbours.append(self.grids[i-1][j])
                if i + 1 < self.width:
                    self.grids[i][j].neighbours.append(self.grids[i+1][j])

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
        self.screen = pygame.display.set_mode((graph.width, graph.height), pygame.RESIZABLE)
        self.bg_color = (255, 255, 255)
        self.search_finished = False

    def find_lowest_f_grid_index(self):
        result = 0
        for i in range(len(self.open_set)):
            if self.open_set[i].f < self.open_set[result].f:
                result = i
        return result

    @staticmethod
    def mark_path(grid):
        grid.col = (0, 0, 255)
        last = grid.parent
        while last:
            #print(last.x, last.y)
            last.col = (0, 0, 255)
            last = last.parent

    @staticmethod
    def heuristic(p1, p2):
        # don't overestimates
        return sqrt(abs(p1[0] - p2[0])**2 + abs(p1[1] - p2[1])**2)

    def recolor_close_set(self):
        for g in self.close_set:
            g.col = (255, 0, 0)

    def run_search(self):
        self.start_grid.f = self.heuristic((self.start_grid.x, self.start_grid.y), (self.end_grid.x, self.end_grid.y))
        self.open_set.append(self.start_grid)
        while True:
            if self.search_finished:
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
                self.mark_path(current)
                if current == self.end_grid:
                    print('Path found!')
                    self.mark_path(current)
                    self.search_finished = True
                else:
                    self.open_set.pop(current_index)
                    self.close_set.append(current)
                    for n in current.neighbours:
                        if (n in self.close_set) or (n.wall):
                            continue
                        if n not in self.open_set:
                            self.open_set.append(n)
                            n.col = (0, 255, 0)
                            old_n_g = float('inf')
                        else:
                            old_n_g = n.g
                        if current.g + 1 < old_n_g: 
                            n.g = current.g + 1
                            n.parent = current
                            n.f = n.g + self.heuristic((n.x, n.y), (self.end_grid.x, self.end_grid.y))
                # -----------------------------------------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit() # quit the whole program
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.screen.fill(self.bg_color)
            # show grids colours
            for col in self.graph.grids:
                for r in col:
                    self.screen.set_at((r.x, r.y), r.col)
            pygame.display.flip()



if __name__ == "__main__":
    graph = grids_graph(100, 100)
    graph.init_grids()

    # for i in range(graph.height):
    #     for j in range(graph.width):
    #         print('\ngrid:', graph.grids[i][j].x, graph.grids[i][j].y)
    #         print('neighbours:')
    #         for n in graph.grids[i][j].neighbours:
    #             print(n.x, n.y, end = ', ')
    A_star = A_star_search(graph, (0, 0), (60, 78))
    A_star.run_search()