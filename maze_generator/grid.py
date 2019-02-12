import pygame
import random


class grid(object):
    def __init__(self, x, y, w):
        """
        x, y is the grid's top left point's raw pixle
        """
        self.x, self.y = x, y
        self.w = w
        self.walls = {'left':True, 'up':True, 'right':True, 'down':True}
        self.checked = False
        self.neighbours = {'left':None, 'right':None, 'up':None, 'down':None}

    def show(self, screen):
        # first mark then draw wall, otherwise the wall will be override by the mark!
        # mark if checked (fill the pixles within the boundary)
        if self.checked:
            for i in range(self.x, self.x + self.w):
                for j in range(self.y, self.y + self.w):
                    screen.set_at((i, j), (255, 255, 255)) 
        # show walls:
        if self.walls['up']:
            pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (self.x+self.w-1, self.y), 1)
        if self.walls['down']:
            pygame.draw.line(screen, (0, 0, 0), (self.x, self.y+self.w-1), (self.x+self.w-1, self.y+self.w-1), 1)
        if self.walls['left']:
            pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (self.x, self.y+self.w-1), 1)
        if self.walls['right']:
            pygame.draw.line(screen, (0, 0, 0), (self.x+self.w-1, self.y), (self.x+self.w-1, self.y+self.w-1), 1)

    def get_an_unchecked_neighbour(self):
        try:
            neighbours = {p:n for p, n in self.neighbours.items() if n is not None}
            unchecked_neighbours = [{'position':p, 'neighbour':n} for p, n in neighbours.items() if not n.checked]
            neighbour = random.choice(unchecked_neighbours)
            return neighbour
        except IndexError:
            return None 

    def remove_wall(self, neighbour):
        np = neighbour['position']
        if np == 'left':
            self.walls['left'] = False
            neighbour['neighbour'].walls['right'] = False
        if np == 'right':
            self.walls['right'] = False
            neighbour['neighbour'].walls['left'] = False
        if np == 'up':
            self.walls['up'] = False
            neighbour['neighbour'].walls['down'] = False
        if np == 'down':
            self.walls['down'] = False
            neighbour['neighbour'].walls['up'] = False