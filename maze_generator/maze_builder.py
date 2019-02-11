# pylint: disable=no-member
import pygame
from grid import grid
import sys
import time

class maze_builder(object):
    def __init__(self):
        self.width = 800
        self.height = 600
        self.grid_width = 20
        self.nrows = int(self.height/self.grid_width)
        self.ncols = int(self.width/self.grid_width)
        # init grids: top left(0 ,0), bottom right(ncols-1, nrows-1)
        self.grids = []
        for i in range(self.ncols):
            self.grids.append([])
            for j in range(self.nrows):
                self.grids[i].append(grid(i*self.grid_width, j*self.grid_width, self.grid_width))
        # add each grid's neighbours
        for i in range(self.ncols):
            for j in range(self.nrows):
                if i > 0:
                    self.grids[i][j].neighbours['left'] = self.grids[i-1][j]
                if i < self.ncols - 1:
                    self.grids[i][j].neighbours['right'] = self.grids[i+1][j]
                if j > 0:
                    self.grids[i][j].neighbours['up'] = self.grids[i][j-1]
                if j < self.nrows - 1:
                    self.grids[i][j].neighbours['down'] = self.grids[i][j+1]
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.bg_color = (87, 150, 200)

    def build_finish(self):
        for col in self.grids:
            for g in col:
                if not g.checked:
                    return False
        return True
    
    def show_grids(self):
        for col in self.grids:
            for g in col:
                g.show(self.screen)

    def show_current_grids(self, current):
        for i in range(current.x + 1, current.x + current.w - 1):
            for j in range(current.y + 1, current.y + current.w - 1):
                self.screen.set_at((i, j), (255, 0, 0))

    def run(self):
        self.stack = [] # FILO
        curr_grid = self.grids[0][0]
        curr_grid.checked = True
        while True:
            time.sleep(0.05)
            if self.build_finish():
                print('buid finish!')
            else:
                # ---------- Recursive backtracker DFS algorithm: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker
                next_grid = curr_grid.get_an_unchecked_neighbour()
                if next_grid: # if there is a valid unchecked neighbour
                    next_grid['neighbour'].checked = True
                    self.stack.append(curr_grid)
                    curr_grid.remove_wall(next_grid)
                    curr_grid = next_grid['neighbour']
                else: # no valid unchecked neighbour
                    curr_grid = self.stack.pop(-1)
                # -----------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit() # quit the whole program
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.screen.fill(self.bg_color)
            self.show_grids()
            self.show_current_grids(curr_grid)
            pygame.display.flip()

if __name__ == "__main__":
    mg = maze_builder()
    mg.run()