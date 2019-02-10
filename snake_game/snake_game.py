# pylint: disable=no-member
import pygame
import sys
from snake import snake
import random
from time import sleep

class food(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.eaten = False

class snake_game(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.bg_color = (87, 250, 255)
        self.foods = []

    def generate_food(self):
        if not self.foods:
            self.foods.append(food(random.randint(0, self.width - 1), random.randint(0, self.height - 1)))

    def run(self):
        my_snake = snake(self.width, self.height)
        while True:
            sleep(0.01)
            self.generate_food()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit() # quit the whole program
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_LEFT:
                        my_snake.move_direction = 'l'
                    elif event.key == pygame.K_RIGHT:
                        my_snake.move_direction = 'r'
                    elif event.key == pygame.K_UP:
                        my_snake.move_direction = 'u'
                    elif event.key == pygame.K_DOWN:
                        my_snake.move_direction = 'd'
            my_snake.move()
            dead = my_snake.dead_or_not()
            if not dead:
                my_snake.update_body(self.foods)
            else:
                print('dead')
            self.foods = [f for f in self.foods if f.eaten == False]
            self.screen.fill(self.bg_color) # reset all color
            my_snake.show(self.screen, self.bg_color)
            for f in self.foods:
                self.screen.set_at((f.x, f.y), (255, 0, 0))
            pygame.display.flip()

if __name__ == "__main__":
    game = snake_game(100, 50)
    game.run()