#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random, time
from Solution import Solution

class GA:
    def __init__(self, graph, max_generations = 20000, population_size = 50, fitness_threshold = 4):
        if graph == None or max_generations < 1 or population_size < 2:
            raise ValueError()
        self.graph = graph
        self.graph_v = self.graph.v()
        self.max_generations = max_generations
        self.population_size = population_size
        # fitness threshold for choosing a parent selection and mutation algorithm
        self.fitness_threshold = fitness_threshold
        self.rand = random
        
    def get_solution(self, colors):
        self.colors = colors
        start_time = time.time()
        population = Population(self.graph, self.graph_v, self.population_size, self.fitness_threshold, self.rand, self.colors)
        while population.best_fitness() != 0 and population.generation() < self.max_generations:
            population.next_generation()
        end_time = time.time()
        if population.best_fitness() == 0:
            return Solution(population.best_individual(), self.graph, colors, population.generation(), end_time - start_time)
        return Solution(None, self.graph, colors, population.generation(), end_time - start_time)
    
class Population:
    def __init__(self, graph, graph_v, population_size, fitness_threshold, rand, colors):
        self.graph = graph
        self.graph_v = graph_v
        self.population_size = population_size
        self.fitness_threshold = fitness_threshold
        self.rand = rand
        self.colors = colors
        self.__generation = 0
        
        self.population = []
        for i in range(self.population_size):
            self.population.append(Individual(self.graph, self.graph_v, self.fitness_threshold, self.rand, self.colors))
            self.population[i].random_individual()
        self.sort()
        
    def next_generation(self):
        half_size = self.population_size // 2
        children = []
        for i in range(half_size):
            parents = self.__select_parents()
            child = Individual(self.graph, self.graph_v, self.fitness_threshold, self.rand, self.colors)
            child.crossover(parents)
            child.mutate()
            children.append(child)
        for i in range(half_size):
            self.population[self.population_size - i - 1] = children[i]
        self.sort()
        self.__generation += 1
        
    def best_individual(self):
        return self.population[0].chromosome
    
    def best_fitness(self):
        return self.population[0].fitness
    
    def generation(self):
        return self.__generation
    
    def __select_parents(self):
        return self.select_parents1() if self.best_fitness() > self.fitness_threshold else self.select_parents2()
    
    def select_parents1(self):
        temp_parent1 = self.rand.choice(self.population)
        while True:
            temp_parent2 = self.rand.choice(self.population)
            if temp_parent1 == temp_parent2:
                break
        parent1 = temp_parent2 if temp_parent1.fitness > temp_parent2.fitness else temp_parent1 
        while True:
            temp_parent1 = self.rand.choice(self.population)
            while True:
                temp_parent2 = self.rand.choice(self.population)
                if temp_parent1 == temp_parent2:
                    break
            parent2 = temp_parent2 if temp_parent1.fitness > temp_parent2.fitness else temp_parent1 
            if parent1 == parent2:
                break
        return Parents(parent1, parent2)
    
    def select_parents2(self):
        return Parents(self.population[0], self.population[1])
    
    def sort(self):
        n = self.population_size
        while True:
            newn = 0
            for i in range(1, n):
                if self.population[i - 1].fitness > self.population[i].fitness:
                    self.population[i], self.population[i - 1] = self.population[i - 1], self.population[i]
                    newn = i
            if n != 0:
                break
                
class Individual:
    def __init__(self, graph, graph_v, fitness_threshold, rand, colors):
        self.graph = graph
        self.graph_v = graph_v
        self.fitness_threshold = fitness_threshold
        self.rand = rand
        self.colors = colors        
        
    def random_individual(self):
        # each element of chromosome represents a color
        self.chromosome = []
        for i in range(self.graph_v):
            self.chromosome.append(self.rand.randint(0, self.colors - 1))
        self.update_fitness()
        
    def crossover(self, parents):
        self.chromosome = []
        crosspoint = self.rand.randint(0, self.graph_v - 1)
        c = 0
        while c <= crosspoint:
            self.chromosome.append(parents.parent1.chromosome[c])
            c += 1
        while c < self.graph_v:
            self.chromosome.append(parents.parent2.chromosome[c])
            c += 1
        self.update_fitness()
        
    def mutate(self):
        if self.fitness > self.fitness_threshold:
            self.mutate1()
        else:
            self.mutate2()
            
    def mutate1(self):
        for v in range(self.graph_v):
            for w in self.graph.adj(v):
                if self.chromosome[v] == self.chromosome[w]:
                    valid_colors = set()
                    for c in range(self.colors):
                        valid_colors.add(c)
                    for u in self.graph.adj(v):
                        valid_colors.discard(self.chromosome[u])
                    valid_colors = list(valid_colors)
                    if len(valid_colors) > 0:
                        self.chromosome[v] = valid_colors[self.rand.randint(0, len(valid_colors) - 1)]
                    break
        self.update_fitness()
        
    def mutate2(self):
        for v in range(self.graph_v):
            for w in self.graph.adj(v):
                if self.chromosome[v] == self.chromosome[w]:
                    self.chromosome[v] = self.rand.randint(0, self.colors - 1)
                    break
        self.update_fitness()
        
    def update_fitness(self):
        f = 0
        for v in range(self.graph_v):
            for w in self.graph.adj(v):
                if self.chromosome[v] == self.chromosome[w]:
                    f += 1
        # fitness is defined as the number of 'bad' edges, i.e., edges connecting two
        # vertices with the same color
        self.fitness = f // 2
        
    def __eq__(self, o):
        if o != None and isinstance(o, Individual):
            return self.fitness == o.fitness
        return NotImplemented
            
class Parents:
    def __init__(self, parent1, parent2):
        self.parent1 = parent1
        self.parent2 = parent2