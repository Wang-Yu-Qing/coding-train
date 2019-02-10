# pylint: disable=no-member
import random
import pygame


class snake(object):
    def __init__(self, width, height):
        # x, y position for snake head
        self.x, self.y = random.randint(0, width - 1), random.randint(0, height - 1)
        self.width, self.height = width, height
        self.head = self.x, self.y
        self.left_limit = 0
        self.right_limit = width - 1
        self.upper_limit = 0
        self.lower_limit = height
        self.body = [(self.x, self.y)] # head in the last position
        self.move_direction = random.choice(['l', 'r', 'u', 'd'])
        self.get_food = False

    def reset(self):
        self.__init__(self.width, self.height)

    def dead_or_not(self):
        for b in self.body[:-1]:
            if (b[0], b[1]) == (self.x, self.y):
                self.reset()
                return True
        return False

    def move_left(self):
        if self.x == self.left_limit:
            self.reset()
            print('dead')
        else:    
            self.x -= 1
    
    def move_right(self):
        if self.x == self.right_limit:
            self.reset()
            print('dead')
        else:
            self.x += 1

    def move_up(self):
        if self.y == self.upper_limit:
            self.reset()
            print('dead')
        else:
            self.y -= 1

    def move_down(self):
        if self.y == self.lower_limit:
            print('dead')
            self.reset()
        else:
            self.y += 1

    def move(self):
        if self.move_direction == 'l':
            self.move_left()
        elif self.move_direction == 'r':
            self.move_right()
        elif self.move_direction == 'u':
            self.move_up()
        elif self.move_direction == 'd':
            self.move_down()

    def eat(self, foods):
        for food in foods:
            if (self.x, self.y) == (food.x, food.y):
                print('eat')
                food.eaten = True
                self.get_food = True
                self.body.append((food.x, food.y))
                return 
        self.get_food = False # didn't eat any food

    def update_body(self, foods):
        """
        key function
        """
        self.eat(foods)
        if not self.get_food:
            # shift every body part
            for i in range(len(self.body) - 1):
                self.body[i] = self.body[i + 1]
            self.body[-1] = self.x, self.y # update head to new position

    def show(self, screen, bg_color):
        #print(self.x, self.y)
        [screen.set_at((bd[0], bd[1]), (0, 0, 0)) for bd in self.body]
        

