import matplotlib.pyplot as plt
import numpy as np
import sys, os, time

#Function that imports a textfile and finds dimensions
def get_content_from_file(filename):
    content =  np.genfromtxt(filename, dtype='str', comments='@')
    rows = len(content)
    cols = len(content[0])
    return content, rows, cols

#Nodeclass with properties
class Node:
    def __init__(self, x, y):
        self.parent = None
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        
#Change this one 
#Makes list of nodes from the textfile import        
def generate_list_of_nodes(board):
    nodes = []
    n0 = None
    for (i, row) in enumerate(board):
        for (j, cell) in enumerate(row):
            isWall = False
            if cell == '#':
                isWall = True
            n = Node(i,j, isWall)
            if cell == 'A':
                start = Node(i,j, isWall=False)
            if cell == 'B':
                end = Node(i,j, isWall=False)
            nodes.append(n)
    return nodes, start, end

#Algorithm class
class Astar:
    def __init__(self, board, rows, cols):
        self.open = []
        self.closed = set()
        (self.nodes, self.start, self.end) = generate_list_of_nodes(board)
        self.rows = rows
        self.cols = cols

    #Calculates manhattan distance from node to end
    def calc_costs(self, node):
        return 10 * np.abs(node.x - self.end.x) + np.abs(node.y - self.end.y)
    
    #Returns a node based on x,y position
    def get_node(self, x, y):
        return self.nodes[x * self.cols + y] #2d indexing of 1d array
        
    #Gets the adjacent nodes. Need to check that we dont go out of the grid        
    def get_adjacent_nodes(self, node):
        
        nodes = []
        #Up
        if node.y < (self.cols - 1):
            nodes.append(self.get_node(node.x, node.y+1))
        #Down
        if node.y > 0:
            nodes.append(self.get_node(node.x, node.y-1))
        #left
        if node.x > 0:
            nodes.append(self.get_node(node.x-1, node.y))
        #Right
        if node.x < (self.rows - 1):
            nodes.append(self.get_node(node.x+1, node.y))
        return nodes
   
   #Change this
    #Updates the costs and parent of an adjancent node 
    def update_node(self, adj, node):
        adj.g = node.g + 10
        adj.h = self.calc_costs(adj)
        adj.parent = node
        adj.f = adj.g + adj.h
        
    #Function that gets the path by seeing who is whos parent, starting with the end
    def get_path(self):
        path_nodes = []
        node = self.end
        while node.parent is not self.start:
            node = node.parent
            path_nodes.append((node.x, node.y))
        return path_nodes
    
    #Change tHis one
    #Pretty basic function that prints the solved
    def print_solved_path(self, path_nodes):
        line = '_' * self.cols + '\n'
        board = ''
        i = 0
        for node in self.nodes:
            if node.isWall:
                line+='#'
            elif (node.x, node.y) == (self.end.x, self.end.y):
                line += 'E'
            elif (node.x, node.y) in (path_nodes):
                line += 'o'
            elif (node.x, node.y) == (self.start.x, self.start.y):
                line += 'S'
            else:
                line += '-'
            i+=1
            if i == 20:
                i = 0
                line += '\n'
                board += line
        board += '_' * self.cols + '\n'
        print board
        
    #Change some in this?
    def go(self):
        #Append start fcost and startnode to open list
        self.open.append((self.start.f, self.start))
        #While we have nodes to process: add undiscovered nodes to open
        while len(self.open):
            _, current = self.open.pop()
            #Sort the nodes in reverse order, so we pop the one with lowest f-cost
            self.open.sort(reverse=True)
            self.closed.add(current)
            #See if we came to the end, if we did, we are done.
            if (current.x,current.y) == (self.end.x, self.end.y):
                print 'Found a path, exiting'
                self.end.parent = current
                self.print_path(self.get_path())
                break
            #Check the adjacent nodes to the one we are working on
            adj_nodes = self.get_adjacent_nodes(current)
            for adj_node in adj_nodes:
                self.open.sort(reverse=True)
                #If it is not unpassable, and not yet processed
                if not adj_node.isWall and adj_node not in self.closed:

                    #If adjacent node is in open, and its g-cost is higher than itself + 10 we need to update its value, because we found a shorter path to it now.
                    if (adj_node.f, adj_node) in self.open:
                        if adj_node.g > current.g + 10:
                            self.update_node(adj_node, current)
                    #If adjacent node is not in open, we update its values, and add it to open
                    else:
                        self.update_node(adj_node, current)
                        self.open.append((adj_node.f, adj_node))
                        
#Create Astar object and solve board
def shortest_path(filename):
    content, rows, cols = get_content_from_file(filename)
    astar = Astar(content, rows, cols)
    astar.go()
    
if __name__ == '__main__':
    filename = sys.argv[1]
    shortest_path(filename)
