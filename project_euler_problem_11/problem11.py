#!/usr/bin/python

import sys
import os
import numpy as np
import re
import urllib2
from enum import Enum

default_file = 'https://dl.dropboxusercontent.com/u/4443923/gofore/rekry/numbers.txt'

class Direction(Enum):
    horizontal = 0
    vertical = 1
    diagonal = 2
    reverse_diagonal = 3

# Prints the whole matrix with the numers used for maximal product covered with brackets
def print_matrix(numarray,row,col,prod_count,d):
    it=0
    for i in range(len(numarray)):
        for j in range(len(numarray[i])):
            if d == Direction.vertical and col == j and row+it == i and it < prod_count:
                sys.stdout.write(('[%d]' % numarray[i][j]).zfill(2).center(6))
                it = it+1
            elif d == Direction.horizontal and row == i and col+it == j and it < prod_count:
                sys.stdout.write(('[%d]' % numarray[i][j]).zfill(2).center(6))
                it = it+1
            elif d == Direction.diagonal and row+it == i and col+it == j and it < prod_count:
                sys.stdout.write(('[%d]' % numarray[i][j]).zfill(2).center(6))
                it = it+1
            elif d == Direction.reverse_diagonal and row-prod_count+1+it == i and col+prod_count-it-1 == j and it < prod_count:
                # For bottom left to top right, must be calculated a bit differently
                sys.stdout.write(('[%d]' % numarray[i][j]).zfill(2).center(6))
                it = it+1
            else:
                sys.stdout.write(('%d' % numarray[i][j]).zfill(2).center(6))
        print('')

def calculate_products(numbers,product_count,d):
    if product_count > len(numbers) or product_count > len(numbers[0]):
        sys.exit('Given item count is too large for given grid!\n' \
                 'Grid size (%d, %d) is less than given product count %d' \
                 % (len(numbers),len(numbers[0]),product_count))
    # Construct grid for products
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

def validate_url(url):
    return re.compile(r'^https?:\/\/([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$',re.I).match(url) is not None

# Everything that really matters in single main function while that's the way drunk people do it
def main():
    # Get numbers from file or show error
    if len(sys.argv) > 1 and not os.path.isfile(sys.argv[1]):
        if validate_url(sys.argv[1]):
            try:
                req = urllib2.Request(sys.argv[1])
                numbers = [line.split() for line in urllib2.urlopen(req)]
            except urllib2.HTTPError:
                sys.exit('Error reading grid from given url: %s' % sys.argv[1])
        else:
            sys.exit('Given file not found or unreachable: %s' % sys.argv[1])
    elif len(sys.argv) > 1:
        numbers = [line.split() for line in open(sys.argv[1])]
    else:
        print('No filename given, using default: %s' % default_file)
        if validate_url(default_file):
            try:
                req = urllib2.Request(default_file)
                numbers = [line.split() for line in urllib2.urlopen(req)]
            except urllib2.HTTPError:
                sys.exit('Error reading grid from default url: %s' % default_file)
        else:
            try:
                numbers = [line.split() for line in open(default_file)]
            except ValueError:
                sys.exit('Error reading grid from default file: %s' % default_file)

    # Just to ensure the file's read correctly in this case
    #if len(numbers) == 0 or len(numbers) != 20 or len(numbers[0]) != 20:
    #    sys.exit('Invalid file format! Should be 20x20 grid')
    product_count = 4
    if len(sys.argv) > 2:
        try:
            product_count = int(sys.argv[2])
            if product_count > len(numbers) or product_count > len(numbers[0]):
                sys.exit('Too large item count!\n' \
                         'Value cannot be more than grid size')
            if product_count <= 1:
                sys.exit('Too low item count!\n' \
                         'Value must be over 1')
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
    try:
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
    except ValueError: # product_count = len(numbers)
        maxs = {
            Direction.horizontal:{
                'value':horizontal
            },
            Direction.vertical:{
                'value':vertical
            },
            Direction.diagonal:{
                'value':diagonal
            },
            Direction.reverse_diagonal:{
                'value':reverse_diagonal
            }
        }
    # Get the indeces (row and column of grid) for maximums
    try:
        maxs[Direction.horizontal]['index'] = np.where(horizontal == maxs[Direction.horizontal]['value'])
        if len(maxs[Direction.horizontal]['index'][0]) > 1:
            maxs[Direction.horizontal]['index'] = {
                0: maxs[Direction.horizontal]['index'][0][0],
                1: maxs[Direction.horizontal]['index'][1][0]
            }
        maxs[Direction.vertical]['index'] = np.where(vertical == maxs[Direction.vertical]['value'])
        if len(maxs[Direction.vertical]['index'][0]) > 1:
            maxs[Direction.vertical]['index'] = {
                0: maxs[Direction.vertical]['index'][0][0],
                1: maxs[Direction.vertical]['index'][1][0]
            }
        maxs[Direction.diagonal]['index'] = np.where(diagonal == maxs[Direction.diagonal]['value'])
        if len(maxs[Direction.diagonal]['index'][0]) > 1:
            maxs[Direction.diagonal]['index'] = {
                0: maxs[Direction.diagonal]['index'][0][0],
                1: maxs[Direction.diagonal]['index'][1][0]
            }
        maxs[Direction.reverse_diagonal]['index'] = np.where(reverse_diagonal == maxs[Direction.reverse_diagonal]['value'])
        if len(maxs[Direction.reverse_diagonal]['index'][0]) > 1:
            maxs[Direction.reverse_diagonal]['index'] = {
                0: maxs[Direction.reverse_diagonal]['index'][0][0],
                1: maxs[Direction.reverse_diagonal]['index'][1][0]
            }
        # Print the maximum values for each
        print('Maximal products of each direction:')
        print('Horizontally: %d starting from (%d, %d) towards right' % \
             (maxs[Direction.horizontal]['value'], maxs[Direction.horizontal]['index'][0], maxs[Direction.horizontal]['index'][1]))
        print('Vertically: %d starting from (%d, %d) towards down' % \
             (maxs[Direction.vertical]['value'], maxs[Direction.vertical]['index'][0], maxs[Direction.vertical]['index'][1]))
        print('Diagonally: %d starting from (%d, %d) towards bottom right' % \
             (maxs[Direction.diagonal]['value'], maxs[Direction.diagonal]['index'][0], maxs[Direction.diagonal]['index'][1]))
        print('Reverse diagonally: %d starting from (%d, %d) towards upper right' % \
             (maxs[Direction.reverse_diagonal]['value'], maxs[Direction.reverse_diagonal]['index'][0], maxs[Direction.reverse_diagonal]['index'][1]))
    except IndexError:
        sys.exit('Error finding maximum values!\n' \
                 'Try with smaller grid and/or item count')
    # Flip the objects to get the maximum (pure if stuff's kinda boring)
    flip = [(obj['value'], d) for (d, obj) in maxs.items()]
    [highest,direction] = max(flip)
    print('Maximum is: %d starting from (%d,%d) %s' % (highest,maxs[direction]['index'][0],maxs[direction]['index'][1],str(direction)))

    # Print the original numbers grid visualizing the maximum values
    print_matrix(numbers, maxs[direction]['index'][0], maxs[direction]['index'][1], product_count, direction)

if __name__ == "__main__":
    main()

