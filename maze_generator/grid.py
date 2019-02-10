import pygame

class grid(object):
    def __init__(self, x, y, w):
        """
        x, y is the grid's top left point's raw pixle
        """
        self.x, self.y = x, y
        self.w = w
        self.walls = {'left':True, 'up':True, 'right':True, 'down':True}

    def show(self, screen):
        if self.walls['up']:
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x+self.w, self.y), 1)
        if self.walls['down']:
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y-self.w), (self.x+self.w, self.y-self.w), 1)
        if self.walls['left']:
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x, self.y+self.w), 1)
        if self.walls['right']:
            pygame.draw.line(screen, (255, 0, 0), (self.x+self.w, self.y), (self.x+self.w, self.y+self.w), 1)