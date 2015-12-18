#!/usr/bin/python

import sys
import numpy as np
from os.path import isfile

default_file_name = 'numbers.txt'
prod_count = 4

# Prints the whole matrix with the numers used for maximal product covered with '|'
def print_matrix(numarray,row,col,direction):
    iter=0
    for i in range(len(numarray)):
        for j in range(len(numarray[i])):
            if direction == 'ver' and col == j and row == i+iter and iter < prod_count:
                sys.stdout.write(('|%d|' % numarray[i][j]).center(6))
                iter = iter+1
            elif direction == 'hor' and row == i and col == j+iter and iter < prod_count:
                sys.stdout.write(('|%d|' % numarray[i][j]).center(6))
                iter = iter+1
            elif direction == 'diag' and row == i+iter and col == j+iter and iter < prod_count:
                sys.stdout.write(('|%d|' % numarray[i][j]).center(6))
                iter = iter+1
            elif direction == 'diagrev' and row == i+prod_count-1-iter and col == j-prod_count+1+iter and iter < prod_count:
                sys.stdout.write(('|%d|' % numarray[i][j]).center(6))
                iter = iter+1
            else:
                sys.stdout.write(('%d' % numarray[i][j]).center(6))
        print('')

# Everything that really matters in single main function while that's the way drunk people do it
def main():
    # Get numbers from file or show error
    if len(sys.argv) > 1 and not os.path.isfile(sys.argv[1]):
        sys.exit('Given file not found!')
    elif len(sys.argv) > 1:
        numbers = [line.split() for line in open(sys.argv[1])]
    else:
        print('No filename given, using default: %s' % default_file_name)
        numbers = [line.split() for line in open(default_file_name)]
    if len(numbers) == 0 or len(numbers) != 20 or len(numbers[0]) != 20:
        sys.exit('Invalid file format! Should be 20x20 array')
    # Cast all values to integers in a 2D array
    numbers = [map(int, row) for row in numbers]

    # Calculate results in arrays for each method
    res_hor = [[1 for col in range(len(numbers[0])-prod_count)] for row in range(len(numbers))]
    res_ver = [[1 for col in range(len(numbers[0]))] for row in range(len(numbers)-prod_count)]
    res_diag = [[1 for col in range(len(numbers[0])-prod_count)] for row in range(len(numbers)-prod_count)]
    res_diagrev = [[1 for col in range(len(numbers[0])-prod_count)] for row in range(len(numbers)-prod_count)]

    for i in range(len(res_hor)):
        for j in range(len(res_hor[0])):
            for k in range(prod_count):
                res_hor[i][j]*=numbers[i][j+k]

    for i in range(len(res_ver)):
        for j in range(len(res_ver[0])):
            for k in range(prod_count):
                res_ver[i][j]*=numbers[i+k][j]

    for i in range(len(res_diag)):
        for j in range(len(res_diag[0])):
            for k in range(prod_count):
                res_diag[i][j]*=numbers[i+k][j+k]

    for i in range(len(res_diagrev)):
        for j in range(len(res_diagrev[0])):
            for k in range(prod_count):
                res_diagrev[len(res_diagrev)-i-1][j]*=numbers[len(res_diagrev)-i-k-1][j+k]

    # Large amount of variables, prints of eachs maximum etc.
    maxi = {'hor':np.amax(res_hor),'ver':np.amax(res_ver),'diag':np.amax(res_diag),'diagrev':np.amax(res_diagrev)}
    idx = {'hor':np.where(res_hor==maxi['hor']),'ver':np.where(res_ver==maxi['ver']),'diag':np.where(res_diag==maxi['diag']),'diagrev':np.where(res_diagrev==maxi['diagrev'])}
    print('%d (%d, %d)' % (maxi['hor'], idx['hor'][0], idx['hor'][1]))
    print('%d (%d, %d)' % (maxi['ver'], idx['ver'][0], idx['ver'][1]))
    print('%d (%d, %d)' % (maxi['diag'], idx['diag'][0], idx['diag'][1]))
    print('%d (%d, %d)' % (maxi['diagrev'], idx['diagrev'][0], idx['diagrev'][1]))
    flip = [(value, key) for (key, value) in maxi.items()]
    print(max(flip))

    (k,v)=max(flip)
    print_matrix(numbers,idx[v][0],idx[v][1],v)

main()

