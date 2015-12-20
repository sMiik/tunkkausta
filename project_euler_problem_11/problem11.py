#!/usr/bin/python

import sys
import numpy as np
import os
from os.path import isfile
from enum import Enum

default_file_name = 'numbers.txt'

class Direction(Enum):
    horizontal = 0
    vertical = 1
    diagonal = 2
    reverse_diagonal = 3

# Prints the whole matrix with the numers used for maximal product covered with bracets
def print_matrix(numarray,row,col,prod_count,d):
    iter=0
    for i in range(len(numarray)):
        for j in range(len(numarray[i])):
            if d == Direction.vertical and col == j and row == i+iter and iter < prod_count:
                sys.stdout.write(('[%d]' % numarray[i][j]).zfill(2).center(6))
                iter = iter+1
            elif d == Direction.horizontal and row == i and col == j+iter and iter < prod_count:
                sys.stdout.write(('[%d]' % numarray[i][j]).zfill(2).center(6))
                iter = iter+1
            elif d == Direction.diagonal and row == i+iter and col == j+iter and iter < prod_count:
                sys.stdout.write(('[%d]' % numarray[i][j]).zfill(2).center(6))
                iter = iter+1
            elif d == Direction.reverse_diagonal and row == i+prod_count-1-iter and col == j-prod_count+1+iter and iter < prod_count:
                # For bottom left to top right, must be calculated a bit differently
                sys.stdout.write(('[%d]' % numarray[i][j]).zfill(2).center(6))
                iter = iter+1
            else:
                sys.stdout.write(('%d' % numarray[i][j]).zfill(2).center(6))
        print('')

def calculate_products(numbers,product_count,d):
    if product_count > len(numbers) or product_count > len(numbers[0]):
        sys.exit('Given item count is too large for given grid!\n' \
                 'Grid size (%d, %d) is less than given product count %d' \
                 % (len(numbers),len(numbers[0]),product_count))
    # Construct grid for products
    if len(numbers) == product_count and len(numbers[0]) == product_count:
        products = [[1]]
    elif len(numbers) == product_count:
        products = [[1 for col in range(len(numbers[0])-product_count)]]
    elif len(numbers[0]) == product_count:
        products = [[1] for row in range(len(numbers)-product_count)]
    if d == Direction.horizontal:
        products = [[1 for col in range(len(numbers[row])-product_count)] for row in range(len(numbers))]
    elif d == Direction.vertical:
        products = [[1 for col in range(len(numbers[row]))] for row in range(len(numbers)-product_count)]
    else:
        products = [[1 for col in range(len(numbers[row])-product_count)] for row in range(len(numbers)-product_count)]

    # Calculate the products
    for i in range(len(products)):
        for j in range(len(products[i])):
            for k in range(product_count):
                try:
                    if d == Direction.horizontal:
                        # For horizontal, product is counted from left to right
                        products[i][j]*=numbers[i][j+k]
                    elif d == Direction.vertical:
                        # For vertical, product is counted from up to down
                        products[i][j]*=numbers[i+k][j]
                    elif d == Direction.diagonal:
                        # For diagonal, product is counted from top left to bottom right
                        products[i][j]*=numbers[i+k][j+k]
                    elif d == Direction.reverse_diagonal:
                        # For reverse diagonal, product is counted from bottom left to top right
                        products[len(products)-i-1][j]*=numbers[len(products)-i-k-1][j+k]
                except IndexError:
                    if d == Direction.horizontal:
                        print('Invalid index for horizontal calculations (%d, %d)' % (i+k,j))
                    elif d == Direction.vertical:
                        print('Invalid index for vertical calculations (%d, %d)' % (i+k,j))
                    elif d == Direction.diagonal:
                        print('Invalid index for diagonal calculations (%d, %d)' % (i+k,j+k))
                    elif d == Direction.reverse_diagonal:
                        print('Invalid index for reverse diagonal calculations (%d, %d)' % (len(products)-i-k-1,j+k))
                    
    return products

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
    # Just to ensure the file's read correctly in this case
    #if len(numbers) == 0 or len(numbers) != 20 or len(numbers[0]) != 20:
    #    sys.exit('Invalid file format! Should be 20x20 grid')
    product_count = 4
    if len(sys.argv) > 2:
        try:
            product_count = int(sys.argv[2])
            if product_count > len(numbers) or product_count > len(numbers[0]):
                sys.exit('Too large item count!\n' \
                         'Value cannot be more than grid size!') 
        except ValueError:
            sys.exit('Invalid item count value: %s\n' \
                     'Insert integer smaller or equal to smaller grid dimension' % sys.argv[2])
    # Cast all values to integers in a 2D array
    numbers = [map(int, row) for row in numbers]

    # Construct grids for products
    horizontal = calculate_products(numbers, product_count, Direction.horizontal)
    vertical = calculate_products(numbers, product_count, Direction.vertical)
    diagonal = calculate_products(numbers, product_count, Direction.diagonal)
    reverse_diagonal = calculate_products(numbers, product_count, Direction.reverse_diagonal)

    # Store maximals from each direction to variable
    maxs = {
        Direction.horizontal:{
            'value':np.amax(horizontal)
        },
        Direction.vertical:{
            'value':np.amax(vertical)
        },
        Direction.diagonal:{
            'value':np.amax(diagonal)
        },
        Direction.reverse_diagonal:{
            'value':np.amax(reverse_diagonal)
        }
    }
    # Get the indeces (row and column of grid) for maximums
    maxs[Direction.horizontal]['index'] = np.where(horizontal == maxs[Direction.horizontal]['value'])
    maxs[Direction.vertical]['index'] = np.where(vertical == maxs[Direction.vertical]['value'])
    maxs[Direction.diagonal]['index'] = np.where(diagonal == maxs[Direction.diagonal]['value'])
    maxs[Direction.reverse_diagonal]['index'] = np.where(reverse_diagonal == maxs[Direction.reverse_diagonal]['value'])

    # Print the maximum values for each
    print('Maximal products of each direction:')
    print('Horizontally: %lf starting from (%s, %s) to right' % \
         (maxs[Direction.horizontal]['value'], maxs[Direction.horizontal]['index'][0], maxs[Direction.horizontal]['index'][1]))
    print('Vertically: %lf starting from (%s, %s) to down' % \
         (maxs[Direction.vertical]['value'], maxs[Direction.vertical]['index'][0], maxs[Direction.vertical]['index'][1]))
    print('Diagonally: %lf starting from (%s, %s) to bottom right' % \
         (maxs[Direction.diagonal]['value'], maxs[Direction.diagonal]['index'][0], maxs[Direction.diagonal]['index'][1]))
    print('Reverse diagonally: %lf starting from (%s, %s) to upper right' % \
         (maxs[Direction.reverse_diagonal]['value'], maxs[Direction.reverse_diagonal]['index'][0], maxs[Direction.reverse_diagonal]['index'][1]))
    # Flip the objects to get the maximum (pure if stuff's kinda boring)
    flip = [(obj['value'], d) for (d, obj) in maxs.items()]
    [highest,direction] = max(flip)
    print('Maximum is: %lf starting from (%s,%s) %s' % (highest,maxs[direction]['index'][0],maxs[direction]['index'][1],str(direction)))

    # Print the original numbers grid visualizing the maximum values
    print_matrix(numbers, maxs[direction]['index'][0], maxs[direction]['index'][1], product_count, direction)

if __name__ == "__main__":
    main()

