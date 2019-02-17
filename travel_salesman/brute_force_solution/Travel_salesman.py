# pylint: disable=no-member

import sys 
import random
from math import sqrt
import pygame
from City import City 
 
class Travel_salesman(object):
    def __init__(self, width, height, city_width, n_cities):
        self.width = width
        self.height = height
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg_color = (87, 250, 255)
        self.current_path = [] # the city sequence stored in self.current_path represents the current travel sequence
        self.current_path_color = (100, 200, 0)
        self.n_cities = n_cities
        for i in range(n_cities):
            self.current_path.append(City(self.width, self.height, 20, i))
        self.best_path = self.current_path.copy() # copy! not reference!
        self.best_path_distance = float('Inf')
        self.best_path_color = (150, 0, 255)
        
    @staticmethod
    def calculate_distance(p1, p2):
        return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def get_city_by_NO(self, NO):
        return [city for city in self.current_path is city.NO == NO][0]

    @staticmethod
    def update_current_path(current_path):
        """
        based on algorithm for generating lexicographic order:
        https://www.quora.com/How-would-you-explain-an-algorithm-that-generates-permutations-using-lexicographic-ordering
        """
        # step 1 ---> find x
        x = -1
        for index, city in enumerate(current_path[:-1]):
            if city.NO < current_path[index + 1].NO:
                if index > x:
                    x = index
        if x == -1:
            print('Complete')
            return True
        # step 2 ---> find y
        y = -1
        for index, city in list(enumerate(current_path))[x+1:]:
            if city.NO > current_path[x].NO:
                if index > y:
                    y = index
        # step 3 ---> swap
        current_path[x], current_path[y] = current_path[y], current_path[x]
        # step 4 ---> reverse
        # current_path = current_path[:x+1] + list(reversed(current_path[x+1:])) # this way, reference will be detached! no effect.
        i, j = x + 1, len(current_path) - 1
        while i < j:
            current_path[i], current_path[j] = current_path[j], current_path[i]
            i += 1
            j -= 1
        return False

    # def generate_random_path(self):
    #     # make random swap
    #     chosen_index = random.randint(0, self.n_cities - 2)
    #     self.current_path[chosen_index], self.current_path[chosen_index + 1] = self.current_path[chosen_index + 1], self.current_path[chosen_index]

    def show_and_calculate_current_path_distance(self):
        self.current_path_distance = 0
        for index, city in enumerate(self.current_path):
            # show the city point:
            city.show(self.screen)
            #print(city.NO, end = ', ') # show city sequence
            # draw paths and calculate current path distances
            if index < self.n_cities - 1:
                # draw path to next city if is not the last city
                current_city_position = (city.center_x, city.center_y)
                next_city_position = (self.current_path[index + 1].center_x, self.current_path[index + 1].center_y)
                pygame.draw.line(self.screen, self.current_path_color, current_city_position, next_city_position, 5)
                self.current_path_distance +=  self.calculate_distance(current_city_position, next_city_position)
        #print('')

    def show_best_path(self):
        for index in range(self.n_cities - 1):
            # no need to show the city point
            # just show the path
            current_city_position = self.best_path[index].center_x, self.best_path[index].center_y
            next_city_position = self.best_path[index + 1].center_x, self.best_path[index + 1].center_y
            pygame.draw.line(self.screen, self.best_path_color, current_city_position, next_city_position, 8)

    def update_best_path(self):
        if self.current_path_distance < self.best_path_distance:
            self.best_path = self.current_path.copy() # copy! not reference!
            self.best_path_distance = self.current_path_distance
            print('update best path with distance:{}'.format(self.best_path_distance))

    def find_path(self):
        Finish = False
        step = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit() # quit the whole program
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.screen.fill(self.bg_color)
            self.show_and_calculate_current_path_distance()
            self.update_best_path()
            self.show_best_path()
            if not Finish:
                Finish = self.update_current_path(self.current_path)
            pygame.display.flip()
            step += 1


if __name__ == "__main__":
    ts = Travel_salesman(800, 600, 20, 8)
    ts.find_path()