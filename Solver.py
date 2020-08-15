#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from Graph import Graph
from GA import GA

filename = input('Graph file path: ')
try:
    colors = int(input('Number of colors: '))
except ValueError:
    print('Invalid number of colors: ' + colorsStr)
    sys.exit(1)
try:
    graph = Graph(filename)
except IOError as ex:
    print('Cannot read graph file: ' + filename)
    sys.exit(1)
except ValueError as ex:
    print('Invalid graph file: ' + filename)
    sys.exit(1)
print('Solving... ')
ga = GA(graph)
solution = ga.get_solution(colors)
print('Done.')
print(solution)
solution.save()
# solution.draw()