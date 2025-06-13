from common import find_connected_components
import numpy as np

COLORS = [0,1,2,3,4,5,6,7,8,9]

COLOR_mapping = {'black':0,'blue':1,'red':2,'green':3,'yellow':4,'gray':5,'pink':6,'orange':7,'teal':8,'brown':9}

class Shape:

    """
    Shape: a shape is a set of pixels (whose colors are drawn from a specified set of colors) that cannot be expressed as the union of two non-empty sets of pixels where no pixel from one set is adjacent to a pixel in the other set. 
    Here, adjacency can either be defined by orthogonal adjacency, or orthogonal and diagonal adjacency. 
    These will be written as a shape of connectivity 4 in the first case and a shape of connectivity 8 in the second case. 
    """

    def __init__(self,connectivity,colors,grid):
        self.connectivity = connectivity #has a value of either 4 or 8
        self.colors = colors #set of the integers representing the colors that make up the shape
        self.grid = grid #a 2D array that has a value of -1 where there is no shape and an integer representing a color when a pixel is part of a shape

    
    def equals(self,shape):
        #Two shapes are equal if all their pixels are equal.
        return self.grid==shape.grid

    def translationally_equals(self,shape):
        #Two shapes are translationally equal if one can be obtained by changing the position of each of its pixels by the same amount.
        rows_shape1 = [row for row in self.grid if [pixel for pixel in row if pixel!=-1]!=[]]
        rows_shape2 = [row for row in shape.grid if [pixel for pixel in row if pixel!=-1]!=[]]

        boxed_shape1 = [column for column in [[rows_shape1[k][i] for k in range(len(rows_shape1))]for i in range(len(rows_shape1[0]))] if [pixel for pixel in column if pixel!=-1]!=[]]
        boxed_shape2 = [column for column in [[rows_shape2[k][i] for k in range(len(rows_shape2))]for i in range(len(rows_shape2[0]))] if [pixel for pixel in column if pixel!=-1]!=[]]

        return boxed_shape1 == boxed_shape2
    
    def rotate(self,angle):
        #Rotation angle is defined in quarter turns and goes counterclockwise
        if angle%4 == 0:
            return self
        if angle%4 == 1:
            return Shape(self.connectivity,self.colors,[[self.grid[len(self.grid)-k-1][i] for k in range(len(self.grid))] for i in range(len(self.grid[0]))])
        if angle%4 == 2:
            return self.rotate(1).rotate(1)
        if angle%4 == 3:
            return self.rotate(2).rotate(1)
        
    def rotationally_equals(self,shape):
        #Two shapes are rotationally equal if one is translationally equal to the rotation of the other’s grid by either 0°, 90°, 180°, or 270°.
        return False not in [self.rotate(angle).translationally_equals(shape) for angle in range(4)]


    def distance(self,point1,point2):
        #The distance between two pixels in a shape is the minimum number of steps between adjacent pixels in the shape needed to go from one pixel to the other.
        padded_grid = [[self.grid[i][k] if (i in range(len(self.grid)) and k in range(len(self.grid[0]))) else -1 for k in range(-1,len(self.grid[0])+1)]for i in range(-1,len(self.grid)+1)] #adds a row and colum of -1 on all sides
        dist = 0
        points = [point1]
        points_seen = points
        if self.connectivity == 4:
            neighbors = [[0,1],[1,0],[0,-1],[-1,0]]
        if self.connectivity == 8:
            neighbors = [[0,1],[1,0],[0,-1],[-1,0],[1,1],[-1,1],[1,-1],[-1,-1]]
        while True:
            if point2 in points:
                return dist
            new_points = []
            for point in points:
                for neighbor in neighbors:
                        new_point = [x + y for x, y in zip(point, neighbor)]
                        if padded_grid[new_point[0]+1][new_point[1]+1] != -1 and new_point not in new_points and new_point not in points_seen:
                            new_points.append(new_point)
            points_seen.append(new_points)
            points = new_points
            dist += 1

def find_background(grid):
    #Background: the background is the set of all pixels of the most common color.
    flat_grid = [pixel for row in grid for pixel in row]
    return [[pixel if pixel==max(set(flat_grid), key=flat_grid.count) else -1 for pixel in row] for row in grid],max(set(flat_grid), key=flat_grid.count)
    
def find_shapes(grid,connectivity,colors): #finds all the shapes in a given grid
    binary_grid = [[pixel if pixel in colors else -1 for pixel in row] for row in grid] #turns all pixels that aren't the right color into -1
    shapes = [Shape(connectivity,colors,shape.tolist()) for shape in find_connected_components(np.array(binary_grid),-1,connectivity,False)] #turns the numpy arrays into shapes
    return shapes


###########################
### TESTING CONSTRAINTS ###
###########################
import random
import json
import time

def test_constraints(puzzle_func,puzzle_id,p,iters,debug=0):
    assert p!=0
    file = open("evaluation/"+puzzle_id+".json")
    data = json.load(file)
    file.close()

    examples = []
    for case in data['train']:
        input = case['input']
        output = case['output']
        examples.append([input,output])
    for case in data['test']:
        input = case['input']
        output = case['output']
        examples.append([input,output])

    tests = []
    for input,output in examples:
        tests.append(puzzle_func(input,output))
    
    for iter in range(iters):
        for input,output in examples:
            new_output = output
            while [input,new_output] in examples:
                new_output = [[pixel if random.random()>p else COLORS[random.randint(0,9)] for pixel in row] for row in output]
            tests.append(not puzzle_func(input,new_output))
            if debug==2:
                if puzzle_func(input,new_output):
                    print(input,'\n',new_output,iter)

    if debug==1:
        print(tests)

    return False not in tests

def timer(func,inputs):
    result = []
    for inpt in inputs:
        start = time.time_ns()
        func(inpt)
        result.append((time.time_ns()-start)*10**-9)
    return result