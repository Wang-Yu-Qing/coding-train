import random
import numpy as np

Unicode_index = [32, 46] + list(range(65, 91)) + list(range(97, 123)) # generate unicode 32, 46, 49~91, 93~122

class element(object):
    def __init__(self, gene):
        self.gene = gene
        self.fitness = 0
    
    def calculate_fitness(self, target):
        self.fitness = sum([t == e for t, e in zip(list(target), list(self.gene))]) ** 2

    def crossover(self, mate):
        child_gene = ''
        ##--> one from father and one from mother way:
        # for i in range(len(self.gene)):
        #     if i % 2 == 0:
        #         child_gene += self.gene[i]
        #     else:
        #         child_gene += mate.gene[i]
        ##--> first half from father, second half from mother way:
        # middle = int(len(self.gene)/2)
        # for i in range(len(self.gene)):
        #     if i < middle:
        #         child_gene += self.gene[i]
        #     else:
        #         child_gene += mate.gene[i]
        ##--> random way:
        for i in range(len(self.gene)):
            if random.random() < 0.5:
                child_gene += self.gene[i]
            else:
                child_gene += mate.gene[i]
        return child_gene

    def mutation(self, mutation_rate):
        global Unicode_index
        gene = list(self.gene)
        for i in range(len(gene)):
            if random.random() < mutation_rate:
                gene[i] = chr(random.choice(Unicode_index))
        self.gene = ''.join(gene)
            

class Solution(object):
    def __init__(self, target, population_size = 150, mutation_rate = 0.01):
        self.target = target
        self.target_len = len(target)
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = []
        self.total_generations = 1
        self.initialize()

    def initialize(self):
        global Unicode_index
        for _ in range(self.population_size):
            gene = ''.join([chr(random.choice(Unicode_index)) for _ in range(self.target_len)])
            self.population.append(element(gene))
        self.best_element = self.population[0]

    def compute_elements_fitness(self):
        #self.best_element = self.population[0] # no need to do this, just compare with the best_element from last generation
        self.total_fitness = 0
        for e in self.population:
            e.calculate_fitness(self.target)
            if e.fitness >= self.best_element.fitness:
                self.best_element = e
            self.total_fitness += e.fitness
        self.average_fitness = self.total_fitness/self.population_size
        print('best:', self.best_element.gene, 
              'best fitness:{}/{}'.format(self.best_element.fitness, len(self.target)**2), 
              'AF:', round(self.average_fitness, 2),
              'TG:', self.total_generations, 'MR', self.mutation_rate, end = '\r')

    def generate_matingpool(self):
        self.mating_pool = []
        for e in self.population:
            for _ in range(int(e.fitness) * 70):
                self.mating_pool.append(e)

    def choose_a_mate(self):
        """
        accept reject method that can replace the self.generate_matingpool function
        https://www.youtube.com/watch?v=816ayuhDo0E&index=7&list=PLRqwX-V7Uu6bJM3VgzjNV5YxVxUwzALHV
        """
        while True:
            # random choose a element from population
            candidate = random.choice(self.population)
            # random choose a number between 0 and maxfitness
            fitness_threshold = random.choice(range(self.best_element.fitness))
            # if candidate's fitness is less than the fitness threshold, reject it
            if candidate.fitness <= fitness_threshold:
                continue
            else:
                return candidate

    def generate_next_generation(self):
        #self.generate_matingpool()
        next_generation = []
        for _ in range(self.population_size):
            # chose two parents to generate child:
            #parent_A, parent_B = random.choice(self.mating_pool), random.choice(self.mating_pool)
            parent_A, parent_B = self.choose_a_mate(), self.choose_a_mate()
            child_gene = parent_A.crossover(parent_B)
            child = element(child_gene)
            child.mutation(self.mutation_rate)
            next_generation.append(child)
        self.population = next_generation
        self.total_generations += 1



    def run(self):
        while self.best_element.gene != self.target:
            self.compute_elements_fitness()
            self.generate_next_generation()
        print('\nDone!')

if __name__ == "__main__":
    # change the target to any sentence/words with letters within Unicode_index if you want
    s = Solution(target = 'To be or not to be this is a question.', mutation_rate = 0.01)
    #s = Solution(target = 'To be or not to be', mutation_rate = 0.05)
    #s = Solution(target = 'mother fucker.', mutation_rate = 0.01)
    s.run()
