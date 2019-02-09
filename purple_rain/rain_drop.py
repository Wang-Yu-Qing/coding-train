import random

class rain_drop(object):
    def __init__(self, width, height):
        self.speed = random.randint(10, 30)
        self.col = (138, 43, 226)
        self.x = random.randint(0, width - 1)
        self.y = 0 # vertical end position
        self.length = random.randint(30,60)

    def drop(self):
        self.y += self.speed

    def show(self, screen):
        pass