from lpsolve55 import *
import numpy as np
import random as rd
import math

class Graph:
    __vertexes = ['S', 'D']
    __edges = []
    __vertexCount = 2
    __lpResult = 0
    __paths = None
    
    def getNames(self): # возвращает массив имён рёбер для задания переменных lp-файла вида x<имя ребра>
        return [item[0] for item in self.__edges]
    
    def getWeights(self): # возвращает массив весов рёбер графа
        return np.array([item[1] for item in self.__edges], dtype=float)

    def __addVertex(self, name): # private-метод добавления вершины графа
        self.__vertexes.insert(-1, name)
        self.__vertexCount += 1

    def __addEdge(self, direction): # private-метод добавления ребра графа
        self.__edges.append([direction, 0])

    def __weighGraph(self): # private-метод для взвешивания графа
        for i in range(len(self.__edges)):
            self.__edges[i][1] = rd.randrange(5, 15)
    
    def __findPaths(self):
        result = []
        for i in range(self.__vertexCount - 2):
            tmp = [self.__edges[i][0]]
            for j in range(i+1, len(self.__edges)):
                if self.__edges[j][0][-1] == tmp[0][-1] or self.__edges[j][0][0] == tmp[0][-1]:
                    tmp.append(self.__edges[j][0])
            result.append(tmp)
        self.__paths = result
    
    def generateGraph(self): # метод генерации графа произвольным образом
        for _ in range(rd.randrange(4, 10)):
            self.__addVertex(str(self.__vertexCount - 1))
        for i in range(self.__vertexCount):
            for j in range(i+1, self.__vertexCount):
                if i == 0 and j == self.__vertexCount - 1:
                    continue
                else:
                    self.__addEdge(self.__vertexes[i] + self.__vertexes[j])
        self.__weighGraph()
        self.__findPaths()

    def constructGraph(self, x): # метод вычисления координат размещения вершин графа на плоскости
        alpha, R = (math.pi * 2) / self.__vertexCount, x // 2
        return [[R + (R - 25) * math.cos(alpha * i), 
                 R - (R - 25) * math.sin(alpha * i), 
                 self.__vertexes[i]] for i in range(self.__vertexCount)]
    
    def lpsolving(self): # метод записи lp-файла и решения задачи линейного программирования
        names = ['x'+eName for eName in self.getNames()]
        weights = [value for value in self.getWeights()]

        lp = lpsolve('make_lp', 0, len(self.__edges))
        lpsolve('set_verbose', lp, 'IMPORTANT')

        for i in range(len(names)):
            lpsolve('set_col_name', lp, i+1, names[i])
        
        lpsolve('set_obj_fn', lp, [1 for _ in range(self.__vertexCount - 2)] + [0 for _ in range(len(self.__edges) - self.__vertexCount + 2)])
        lpsolve('set_maxim', lp)

        for i in range(self.__vertexCount - 2):
            values = []
            for j in range(len(self.__edges)):
                if names[j][1:] in self.__paths[i] and values.count(1) != i+1:
                    values.append(1)
                elif names[j][1:] not in self.__paths[i]:
                    values.append(0)
                else:
                    values.append(-1)
            lpsolve('add_constraint', lp, values, 'EQ', 0.0)

        for i in range(len(self.__edges)):
            lpsolve('set_upbo', lp, i+1, weights[i])

        lpsolve('write_lp', lp, 'NetProject\\view.lp')
        lpsolve('solve', lp)
        self.__lpResult = str(lpsolve('get_objective', lp))
        lpsolve('delete_lp', lp)

        return self.__lpResult
