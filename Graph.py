#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Graph:
    def __init__(self, filename):
        self.__e = 0
        self.__adj = None
        
        self.filename = filename
        try:
            with open(filename, 'r') as f:
                for line in f:
                    p = line.split(' ')
                    if len(p) == 3 and p[0] == 'p' and p[1] == 'edge' and self.__adj == None:
                        self.__v = int(p[2])
                        self.__adj = [0] * self.__v
                        for v in range(self.__v):
                            self.__adj[v] = []
                    elif len(p) == 3 and p[0] == 'e' and self.__adj != None:
                        self.add_edge(int(p[1]) - 1, int(p[2]) - 1)
        except IOError as ex:
            raise ex
        except Exception as ex:
            raise ValueError()
        
    def v(self):
        return self.__v
    
    def e(self):
        return self.__e
    
    def add_edge(self, v, w):
        if v < 0 or v >= self.__v or w < 0 or w >= self.__v:
            raise IndexError()
        if v == w:
            raise ValueError()
        self.__adj[v].append(w)
        self.__adj[w].append(v)
        self.__e += 1
        
    def adj(self, v):
        if v < 0 or v >= self.__v:
            raise IndexError()
        return self.__adj[v]