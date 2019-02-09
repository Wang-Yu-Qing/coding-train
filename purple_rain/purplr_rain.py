# pylint: disable=no-member
import random
from rain_drop import rain_drop
import pygame
import sys

class purple_rain(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rain_drops = []
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.bg_color = (87, 250, 255)

    def genrate_new_rain_drops(self):
        number = random.randint(10, 15)
        for _ in range(number):
            rd = rain_drop(self.width, self.height)
            self.rain_drops.append(rd)

    def make_drops(self):
        for rd in self.rain_drops:
            rd.drop()

    def update_rain_drops(self):
        # remove those drop whose begining is outside the screen (if using loop, do it in reversed order loop!)
        self.rain_drops = [rd for rd in self.rain_drops if (rd.y - rd.length) < self.height - 1]
        # show rain_drops
        [pygame.draw.line(self.screen, rd.col, (rd.x, rd.y), (rd.x, rd.y-rd.length), random.randint(2, 3)) for rd in self.rain_drops]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit() # quit the whole program
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.screen.fill(self.bg_color)
            self.genrate_new_rain_drops()
            self.make_drops()
            self.update_rain_drops()
            pygame.display.flip()          

if __name__ == "__main__":
    pr = purple_rain(600, 400)
    pr.run()

