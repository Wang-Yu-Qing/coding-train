# pylint: disable=no-member
import pygame
from grid import grid
import sys

class maze_generator(object):
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
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.bg_color = (0, 250, 0)
    
    def show_grids(self):
        for col in self.grids:
            for g in col:
                g.show(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit() # quit the whole program
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.screen.fill(self.bg_color)
            self.show_grids()
            pygame.display.flip()

if __name__ == "__main__":
    mg = maze_generator()
    mg.run()