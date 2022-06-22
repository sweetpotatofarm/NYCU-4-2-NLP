# Author: Chu-Hao Hsiao
# Student ID: 0716026
# HW ID: hw1
# Due Date: 03/18/2021

import numpy as np
import pandas as pd

# read weight table
L_df = pd.read_csv('costs1.csv')
W_df = pd.read_csv('costs2.csv')

# first var: source string, second var: target string, third var: weight data frame
def min_edit_dist(src, tar, df):
    # calculate total cost by DP_matrix using dynamic programming
    DP_matrix = [[0 for j in range(len(tar)+1)] for i in range(len(src)+1)]
    # record operation by backtrace_matrix
    backtrace_matrix = [[0 for j in range(len(tar)+1)] for i in range(len(src)+1)]
    # the size of the matrices should be (length of source + 1) * (length of target + 1)
    row_size = len(src)+1
    col_size = len(tar)+1
    # initialize the matrices
    for i in range(row_size):
        DP_matrix[i][0] = i
        backtrace_matrix[i][0] = 'up'
    for j in range(col_size):
        DP_matrix[0][j] = j
        backtrace_matrix[0][j] = 'lf'
        
    for i in range(1, row_size):
        for j in range(1, col_size):
            substitution = DP_matrix[i-1][j-1] + df[tar[j-1]][ord(src[i-1])-97]
            deletion = DP_matrix[i-1][j] + 1
            insertion = DP_matrix[i][j-1] + 1
            DP_matrix[i][j] = min(insertion, deletion, substitution)
            choice = []
            # insertion => left
            if(DP_matrix[i][j] == insertion):
                choice.append('lf')
            # deletion => up
            if(DP_matrix[i][j] == deletion):
                choice.append('up')
            # substitution => up and left
            if(DP_matrix[i][j] == substitution):
                choice.append('ul')
            # random choose from all possible cells
            backtrace_matrix[i][j] = np.random.choice(choice)
            
    # start backtracking
    row = row_size-1
    col = col_size-1
    cost = DP_matrix[row][col]
    operation = ""
    source = ""
    target = ""
    # stop when [0][0]
    while(row != 0 or col != 0):
        # left => insertion
        if(backtrace_matrix[row][col] == 'lf'):
            operation += 'i '
            source += '* '
            target += tar[col-1] + ' '
            col -= 1
        # up => deletion
        elif(backtrace_matrix[row][col] == 'up'):
            operation += 'd '
            source += src[row-1] + ' '
            target += '* '
            row -= 1
        # up and left => substitution or null
        else:
            # null operation
            if(src[row-1] == tar[col-1]):
                operation += 'n '
            # substitution operation
            else:
                operation += 's '
            source += src[row-1] + ' '
            target += tar[col-1] + ' '
            row -= 1
            col -= 1
                
    return operation, source, target, cost

with open('input.txt') as file:
    input = file.readlines()
    
for line in input:
    line = line.split()
    target = line[0]
    source = line[1:len(line)]
    # print the result
    for src in source:
        operation, new_source, new_target, cost = min_edit_dist(src, target, L_df)
        print(new_source[::-1])
        print(' |' * (int(len(new_source)/2)))
        print(new_target[::-1])
        print(operation[::-1])
        print(" cost: "+str(float(cost)))
        print("\n")
        operation, new_source, new_target, cost = min_edit_dist(src, target, W_df)
        print(new_source[::-1])
        print(' |' * (int(len(new_source)/2)))
        print(new_target[::-1])
        print(operation[::-1])
        print(" cost: "+str(float(cost)))
        print('-'*25)