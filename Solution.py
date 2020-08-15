#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from Drawer import Drawer

class Solution:
    def __init__(self, chromosome, graph, colors, generations, time):
        self.chromosome = chromosome
        self.graph = graph
        self.colors = colors
        self.generations = generations
        self.time = time # in nanoseconds
        
    def draw(self):
        if self.chromosome == None:
            return None
        # return Drawer(self)
        
    def save(self):
        f = open(self.graph.filename + '.' + str(self.colors) + '.solution', 'w')
        f.write(str(self))
        f.close()
        
    def __str__(self):
        newline = '\n'
        if self.chromosome == None:
            solution = '(no solution)' + newline
        else:
            solution = newline
            for v in range(len(self.chromosome)):
                solution += str(v + 1) + ' ' + str(self.chromosome[v]) + newline
        return \
               'Vertices: ' + str(self.graph.v()) + newline + \
               'Edges: ' + str(self.graph.e()) + newline + \
               'Colors: ' + str(self.colors) + newline + \
               'Generations: ' + str(self.generations) + newline + \
               'Time: ' + '%.3f' % self.time + 's' + newline + \
               'Solution: ' + solution