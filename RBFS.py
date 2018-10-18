"""
    PROBLEM FORMULATION:

    1. naive: generate every possible combination of the 8-puzzle
        8! = 40,320 combinations. Not what we want!

    2. Sum of Manhattan_distances

"""
import copy
import re
import glob
import os

infinity = float('inf')

def Puzzle(dim):
    goal_state = list()
    for i in range(dim):
        goal_state.append(list())
        for j in range(dim):
            goal_state[i].append(i*dim + j)

    class Node:
        def __init__(self, state, path_cost):
            self.state = state
            self.children = list()
            self.zero_piece = [0,0]
            for i in range(dim):                                    #finding the zero piece
                for j in range(dim):
                    if state[i][j] == 0: self.zero_piece = [i,j]
            self.f = path_cost + self.manhattan_distance()        #f(n) = g(n) + h(n)

        def rbfs(self, path_cost, f_limit, path_seq):
            self.move(path_cost)                                                #create children
            while path_seq.__len__() == 0 or path_seq[-1] != goal_state:     #repeatedly recurse onto the min. f_val node
                self.children.sort(key=lambda node: node.f)                         #sort to capture changes in f values of the children
                min_f_child = self.children[0]
                if min_f_child.f > f_limit:                                         #stopping condition --> all children exceed f_limit
                    self.f = min_f_child.f
                    path_seq.pop()
                    return
                path_seq.append(min_f_child.state)
                min_f_child.rbfs(path_cost + 1, min(f_limit, self.children[1].f), path_seq)  #recurse onto lowest child, and pass the lowest f_limit possible


        #sum of manhattan distance from the current nodes state to the goal state
        """
        3 1 2    0 1 2
    
        4 7 5    3 4 5
    
        6 0 8    6 7 8
    
        algorithm to determine manhattan_distance
        determine row and column offset of each node from the goal states
        """
        def manhattan_distance(self):
            sum = 0
            for i in range(self.state.__len__()):
                for j in range(self.state[i].__len__()):
                    sum += abs(i - (self.state[i][j]//dim)) + abs(j - (self.state[i][j]%dim))
            return sum

        # Move the 0-piece up, down, left or right
        # move squares by swapping -->  can only move up, down, left or right
        # generate all moves and create 4 children for the 0 piece that gets moved
        def move(self, path_cost):

            self.children.clear()

            i = self.zero_piece[0]
            j = self.zero_piece[1]
            if i+1 < 3:
                child_state = copy.deepcopy(self.state)
                swap(i+1,j,i,j,child_state)
                self.children.append(Node(child_state, path_cost + 1))
            if i-1 >= 0:
                child_state = copy.deepcopy(self.state)
                swap(i-1,j,i,j,child_state)
                self.children.append(Node(child_state, path_cost + 1))
            if j+1 < 3:
                child_state = copy.deepcopy(self.state)
                swap(i,j+1,i,j,child_state)
                self.children.append(Node(child_state, path_cost + 1))
            if j-1 >= 0:
                child_state = copy.deepcopy(self.state)
                swap(i,j-1,i,j,child_state)
                self.children.append(Node(child_state, path_cost + 1))

            return


    def swap(i1, j1, i2, j2, list):
        temp = list[i1][j1]
        list[i1][j1] = list[i2][j2]
        list[i2][j2] = temp
        return

    # parse the file by creating a node for the state depicted in the txt file, where the empty slot is given by the zero
    # return a node with the state depcited in the file
    def parse_txt_file(filename):
        file = open(filename, "r")
        initial = []
        for line in file.readlines():
            line = line.rstrip('\n')
            line_array = re.split(r'\t+', line)
            initial.append([int(numeric_string) for numeric_string in line_array])
        return Node(initial, 0)

    # run RBFS! print out the path of states that were taken
    # 1. File is parsed, and an initial state is created.
    # 2. RBFS on the initial state is applied and it finishes with a goal state
    path = os.getcwd() + "/initial_*.txt"
    files = glob.glob(path)

    for file_name in files:

        print(file_name)
        node = parse_txt_file(file_name)
        state_seq = list()

        print("Puzzle:")
        for row in node.state:
            print(*row, sep=' ')
        print("\n")

        node.rbfs(0, infinity, state_seq)
        print("sequence for solving: ")
        for state in state_seq:
            for row in state:
                print(*row, sep=' ')
            print("\n")
        print("This puzzle took", state_seq.__len__() , "moves to solve")
        print("--------------------------------------------------------------------------")


Puzzle(3)           #8-puzzle
