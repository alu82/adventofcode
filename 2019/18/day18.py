import os
import colorama
from aoc.Utils import drawMixPanel
from operator import add
from string import ascii_lowercase as keys
from string import ascii_uppercase as doors
import math

YOU = '@'
PASSAGE = '.'
WALL = '#'

COLORS =  {
    WALL : colorama.Fore.BLUE,
    YOU : colorama.Fore.GREEN
}

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

class Path:

    def __init__(self, area, position, path, keys):
        self.area = area
        self.position = position
    
    def goTo(self, node):
        itemPosition = list(filter(lambda pos: self.area[pos] == node[0], self.area))[0]
        self.area[itemPosition] = YOU
        self.area[self.position] = PASSAGE
        self.position = itemPosition
    
    def getNextNodes(self, foundKeys):
        workingArea = self.area.copy()
        nextNodes = set()
        distance = 0
        starts = set([self.position])

        while len(starts) > 0:
            distance += 1
            starts = self.nextStep(workingArea, starts)
            tmpStarts = set()
            for start in starts:
                if self.area[start] in keys:
                    nextNodes.add((self.area[start], distance))
                    tmpStarts.add(start)
                if self.area[start] in doors and not self.foundKeyForDoor(self.area[start], foundKeys):
                    tmpStarts.add(start)
            starts = starts - tmpStarts
        return nextNodes

    def foundKeyForDoor(self, door, foundKeys):
        return str.lower(door) in foundKeys
            
    def nextStep(self, paths, starts):
        newStarts = set([])
        for start in starts:
            adjacents = self.getAdjacentPositions(start)
            paths.pop(start, None)
            for adjacent in adjacents:
                if adjacent in paths:
                    newStarts.add(adjacent)
        return newStarts

    def getAdjacentPositions(self, position):
        adjacents = []
        for direction in DIRECTIONS:
            adjacents.append(tuple(map(add, position, direction)))
        return adjacents


class PathFinder:

    def __init__(self, area):
        self.area = dict(filter(lambda item: item[1] != WALL, area.items()))
        self.start = list(filter(lambda node: area[node] == YOU, area))[0]
        self.distance = {}
        self.done = {}
        self.done[YOU] = 0
        for v in set(area.values()):
            if v in keys:
                self.distance[v] = math.inf
        self.pred = {}

    def dijkstra(self):
        graph = Path(self.area.copy(), self.start, [], set())
        
        self.update(YOU, graph.getNextNodes(self.getKeys(YOU)))

        while len(self.distance.keys()) > 0:
            nearest = min(self.distance, key=self.distance.get)
            self.done[nearest] = self.distance.pop(nearest)
            graph.goTo(nearest)
            print(nearest, self.getKeys(nearest), self.pred)
            self.update(nearest, graph.getNextNodes(self.getKeys(nearest)))

        print(self.distance)
        print(self.done)

    def getKeys(self, base):
        if base in self.pred:
            return list(base) + self.getKeys(self.pred[base])
        else:
            return list(base)


    def update(self, base, nextNodes):
        baseDistance = self.done[base]
        for nodeItem in nextNodes:
            node = nodeItem[0]
            distance = nodeItem[1]
            if baseDistance + distance < self.distance[node]:
                self.distance[node] = baseDistance + distance
                self.pred[node] = base



    def clonePath(self, path):
        return Path(path.area.copy(), path.position, path.path.copy(), path.keys.copy())

    

def getArea(input):
    panel = {}
    col = 0
    row = 0

    for line in input:
        for char in line.strip():
            panel[(col, row)] = char
            col += 1
        row += 1
        col = 0
    return panel


def part1(input):
    area = getArea(input)
    pathFinder = PathFinder(area) 
    pathFinder.dijkstra()

# Open input files and get intcodeprogram
script_dir = os.path.dirname(__file__)
inputFile = open(script_dir + "/input", "r")

part1(inputFile)
