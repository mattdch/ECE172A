'''
ECE 172A, Homework 2 Maze Pathfinding
Author: regreer@ucsd.edu
Maze generator adapted from code by Łukasz Nojek
For use by UCSD ECE 172A students only.
'''

import matplotlib.pyplot as plt 
import numpy as np
import pickle

def draw_path(final_path_points, other_path_points):
	'''
	final_path_points: the list of points (as tuples or lists) comprising your final maze path. 
	other_path_points: the list of points (as tuples or lists) comprising all other explored maze points. 
	(0,0) is the start, and (49,49) is the goal.
	Note: the maze template must be in the same folder as this script.
	'''
	im = plt.imread('172maze2021.png')
	x_interval = (686-133)/49
	y_interval = (671-122)/49
	plt.imshow(im)
	fig = plt.gcf()
	ax = fig.gca()
	circle_start = plt.Circle((133,800-122), radius=4, color='lime')
	circle_end = plt.Circle((686, 800-671), radius=4, color='red')
	ax.add_patch(circle_start)
	ax.add_patch(circle_end)
	for point in other_path_points:
		if not (point[0]==0 and point[1]==0) and not (point[0]==49 and point[1]==49):
			circle_temp = plt.Circle((133+point[0]*x_interval, 800-(122+point[1]*y_interval)), radius=4, color='blue')
			ax.add_patch(circle_temp)
	for point in final_path_points:
		if not (point[0]==0 and point[1]==0) and not (point[0]==49 and point[1]==49):
			circle_temp = plt.Circle((133+point[0]*x_interval, 800-(122+point[1]*y_interval)), radius=4, color='yellow')
			ax.add_patch(circle_temp)
	plt.show()

### Your Work Below: 

pickle_maze = "172maze2021.p"
start = (0,0)
goal = (49,49)
height = 50
width = 50
maze = pickle.load(open(pickle_maze, "rb"))
cardinal = {0 : (0,1), 1: (1,0), 2: (0,-1), 3: (-1,0)}
max_iterations = 10000

def sense_maze(index, maze):
    pos = np.unravel_index(index, (height, width))
    directions = maze[pos]
    neighbors = []
    for i in range(0,4):
        if directions[i]:
            new_neighbor = tuple(sum(x) for x in zip(cardinal[i], pos))
            new_neighbor = np.ravel_multi_index(new_neighbor,(height,width))
            neighbors.append(new_neighbor)
              
    return neighbors

def dfs_maze(maze, start, goal):
    iterations = 0
    current_index = np.ravel_multi_index(start, (height, width))
    stack = []
    visited = np.repeat(0,height*width)
    parents = np.repeat(0,height*width)
    stack.append(current_index)
    
    while len(stack) != 0 and current_index != np.ravel_multi_index(goal, (height,width)) and iterations < max_iterations:
        current_index = stack[-1]
        stack.pop()
        iterations += 1
        if visited[current_index] != 1:
            visited[current_index] = 1
            neighbors = sense_maze(current_index, maze)
            for neighbor in neighbors:
                stack.append(neighbor)
                parents[neighbor] = current_index
            
    ind = 0
    final_path = []
    while ind != 2499:
        final_path.append(ind)
        ind = parents[ind]
        
    final_path = np.unravel_index(final_path, (height,width))
    final_path = list(zip(final_path[0],final_path[1]))
    nodes_visited = np.where(visited == 1)
    nodes_visited = np.unravel_index(nodes_visited, (height,width))
    nodes_visited = list(zip(nodes_visited[0][0],nodes_visited[1][0]))
    
    return final_path, nodes_visited, iterations

def bfs_maze(maze, start, goal):
    iterations = 0
    current_index = np.ravel_multi_index(start, (height, width))
    stack = []
    visited = np.repeat(0,height*width)
    parents = np.repeat(0,height*width)
    stack.append(current_index)
    
    while len(stack) != 0 and current_index != np.ravel_multi_index(goal, (height,width)) and iterations < max_iterations:
        current_index = stack[0]
        stack.pop(0)
        iterations += 1
        if visited[current_index] != 1:
            visited[current_index] = 1
            neighbors = sense_maze(current_index, maze)
            for neighbor in neighbors:
                stack.append(neighbor)
                parents[neighbor] = current_index
            
    ind = 2499
    final_path = []
    i = 0
    while ind != 0 and i < 30:
        final_path.append(ind)
        ind = parents[ind]
        i += 1
        
    final_path = np.unravel_index(final_path, (height,width))
    final_path = list(zip(final_path[0],final_path[1]))
    nodes_visited = np.where(visited == 1)
    nodes_visited = np.unravel_index(nodes_visited, (height,width))
    nodes_visited = list(zip(nodes_visited[0][0],nodes_visited[1][0]))
    
    return final_path, nodes_visited, iterations


final, visit, iteration = dfs_maze(maze, start, goal)

draw_path(final, visit)
print(iteration)