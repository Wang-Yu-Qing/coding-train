import random
import pygame


class City(object):
    def __init__(self, screen_width, screen_height, city_width, city_NO):
        # x, y location for top left corner
        self.x = random.randint(0, screen_width - 1)
        self.y = random.randint(0, screen_height - 1)
        self.width = city_width
        self.col = (255, 0, 0)
        self.center_x = self.x + int(self.width/2)
        self.center_y = self.y + int(self.width/2)
        self.NO = city_NO

    def show(self, screen):
        # for i in range(self.x, self.x + self.width):
        #     for j in range(self.y, self.y + self.width):
        #         screen.set_at((i, j), self.col)
        [[screen.set_at((i, j), self.col) for j in range(self.y, self.y + self.width)] for i in range(self.x, self.x + self.width)]

