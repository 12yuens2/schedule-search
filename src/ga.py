import numpy as np
import random
import operator
import subprocess

def random_chromosome(length):
   return np.random.choice([0,1], size=(length,)).tolist()


def roulette_selection(total_fitness, chromosomes):
    r = random.randint(0, total_fitness)

    sum = 0
    for chromosome in chromosomes:
        sum += chromosome.fitness()

        if sum >= r:
            return chromosome
 

def tournament_selection(k, chromosomes):
    competitors = []
    for i in range(k):
        r = random.randint(0, len(chromosomes) - 1)
        competitors.append(chromosomes[r])
        
    highest_fitness = 0
    chosen_chromosome = competitors[0]
    for chromosome in competitors:
        if chromosome.fitness > highest_fitness:
            highest_fitness = chromosome.fitness
            chosen_chromosome = chromosome

    return chosen_chromosome


def mate(mother, father):
    crossover = random.randint(0, mother.length)

    child1 = Chromosome(mother.length)
    child1.genes = mother.genes[:crossover] + father.genes[crossover:]

    child2 = Chromosome(father.length)
    child2.genes = father.genes[:crossover] + mother.genes[crossover:]

    return [child1, child2]

        
class Chromosome:
    def __init__(self, length):
        self.length = length
        self.genes = random_chromosome(length)
        self.fitness = 0

    def mutate(self):
        for i in range(len(self.genes)):
            if (random.randint(0, self.length/10)) == 0:
                self.genes[i] = 1 - self.genes[i]

    def __repr__(self):
        return str(self.genes)
        


class Population:
    def __init__(self, population_size, chromosome_length):
        self.size = population_size
        self.chromosomes = []
        for i in range(population_size):
            self.chromosomes.append(Chromosome(chromosome_length))

    def fitness(self):
        total_fitness = 0
        for chromosome in self.chromosomes:
            total_fitness += chromosome.fitness

        return total_fitness / self.size

    def evolve(self, num_elites):
        children = []
        
        children += self.elites(num_elites)

        total_fitness = 0
        for chromosome in self.chromosomes:
            total_fitness += chromosome.fitness
        
        while len(children) < self.size:
            mother = tournament_selection(3, self.chromosomes)
            father = tournament_selection(3, self.chromosomes)
            children += mate(mother, father)

        for child in children[num_elites:]:
            child.mutate()

        self.chromosomes = children

    def elites(self, num_elites):
        last_gen = self.chromosomes
        fitness_map = {k: v for (k, v) in zip(last_gen, [c.fitness for c in last_gen])}

        best = sorted(fitness_map.items(), key=operator.itemgetter(1))
        best.reverse()

        return [elite[0] for elite in best[:num_elites]]
        

def get_cpu_time(file):
    f = subprocess.check_output(["tail", "--lines=2", file]).decode("utf-8")
    output = f.split("\t")

    return (output[output.index("Total_time=") + 1])
