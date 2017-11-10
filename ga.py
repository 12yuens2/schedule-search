import numpy as np
import random

def random_chromosome(length):
   return np.random.choice([0,1], size=(length,)).tolist()


def roulette_selection(total_fitness, chromosomes):
    r = random.randint(0, sum)

def tournament_selection(k, chromosomes):
    competitors = []
    for i in range(k):
        competitors.append(chromosomes[i])

        
    highest_fitness = 0
    chosen_chromosome = competitors[0]
    for chromosome in competitors:
        if chromosome.fitness() > highest_fitness:
            highest_fitness = chromosome.fitness()
            chosen_chromosome = chromosome

    return chosen_chromosome


def mate(mother, father):
    crossover = random.randint(0, mother.length)
    mother_genes = mother.genes[:crossover]
    father_genes = father.genes[crossover:]

    child1 = Chromosome(mother.length)
    child1.genes = mother_genes + father_genes

    child2 = Chromosome(father.length)
    child2.genes = father_genes + mother_genes

    return [child1, child2]

        
class Chromosome:
    def __init__(self, length):
        self.length = length
        self.genes = random_chromosome(length)


    def fitness(self):
        return sum(self.genes)
        
    def __repr__(self):
        return str(self.genes)
        


class Population:
    def __init__(self, population_size, chromosome_length):
        self.size = population_size
        self.chromosomes = []
        for i in range(population_size):
            self.chromosomes.append(Chromosome(chromosome_length))

    def evolve(self):
        children = []
        while len(children) < self.size:
            mother = tournament_selection(5, self.chromosomes)
            father = tournament_selection(5, self.chromosomes)
            children += mate(mother, father)

        for child in children:
            if random.randint(0, 10) == 0:
                child.genes[random.randint(0, child.length - 1)] = random.randint(0,1)

        self.chromosomes = children
            
            


p = Population(20, 10)
print(p.chromosomes)
for i in range(100):
    p.evolve()
print(p.chromosomes)
