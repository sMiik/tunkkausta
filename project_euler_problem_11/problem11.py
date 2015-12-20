#!/usr/bin/python

import sys
import os
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

def calculate_maximum(numbers,product_count,d):
    if product_count > len(numbers) or product_count > len(numbers[0]):
        sys.exit('Given item count is too large for given grid!\n' \
                 'Grid size (%d, %d) is less than given product count %d' \
                 % (len(numbers),len(numbers[0]),product_count))
    # Construct grid for products
    if d == Direction.horizontal:
        rows = len(numbers)
        cols = (len(numbers[0])-product_count+1)
    elif d == Direction.vertical:
        rows = (len(numbers)-product_count+1)
        cols = len(numbers[0])
    else:
        rows = (len(numbers)-product_count+1)
        cols = (len(numbers[0])-product_count+1)

    # Calculate the products
    maximum = {
        'value': 0,
        'pos': {
            'row': -1,
            'col': -1
        }
    }
    for i in range(rows):
        for j in range(cols):
            val = 1
            for k in range(product_count):
                if d == Direction.horizontal:
                    # For horizontal, product is counted from left to right
                    val *= numbers[i][j+k]
                elif d == Direction.vertical:
                    # For vertical, product is counted from up to down
                    val *= numbers[i+k][j]
                elif d == Direction.diagonal:
                    # For diagonal, product is counted from top left to bottom right
                    val *= numbers[i+k][j+k]
                elif d == Direction.reverse_diagonal:
                    # For reverse diagonal, product is counted from bottom left to top right
                    val *= numbers[len(numbers)-i-k-1][j+k]
            if val > maximum['value']:
                maximum['value'] = val
                if d == Direction.reverse_diagonal:
                    maximum['pos']['row'] = (len(numbers) - i - 1)
                else:
                    maximum['pos']['row'] = i
                maximum['pos']['col'] = j

    if maximum['pos']['row'] < 0 or maximum['pos']['col'] < 0:
        sys.exit('Something went wrong and maximum value could not be found')
    return maximum

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
                         'Value cannot be more than either size of grid')
            if product_count <= 1:
                sys.exit('Too low item count!\n' \
                         'Value must be over 1')
        except ValueError:
            sys.exit('Invalid item count value: %s\n' \
                     'Insert integer smaller or equal to smaller grid dimension' % sys.argv[2])
    # Cast all values to integers in a 2D array
    numbers = [map(int, row) for row in numbers]

    # Calculate maximum values
    try:
        maxs = {
            Direction.horizontal: calculate_maximum(numbers, product_count, Direction.horizontal),
            Direction.vertical: calculate_maximum(numbers, product_count, Direction.vertical),
            Direction.diagonal: calculate_maximum(numbers, product_count, Direction.diagonal),
            Direction.reverse_diagonal: calculate_maximum(numbers, product_count, Direction.reverse_diagonal)
        }
    except:
        sys.exit('Something went wrong while trying to calculate maximums')
        
    # Get the indeces (row and column of grid) for maximums
    try:
        # Print the maximum values for each
        print('Maximal products of each direction:')
        print('Horizontally: %d starting from %d. rows %d.column towards right' % (maxs[Direction.horizontal]['value'], \
             (maxs[Direction.horizontal]['pos']['row']+1), (maxs[Direction.horizontal]['pos']['col']+1)))
        print('Vertically: %d starting from %d. rows %d. column towards down' % (maxs[Direction.vertical]['value'], \
             (maxs[Direction.vertical]['pos']['row']+1), (maxs[Direction.vertical]['pos']['col'])+1))
        print('Diagonally: %d starting from %d. rows %d. column towards bottom right' % (maxs[Direction.diagonal]['value'], \
             (maxs[Direction.diagonal]['pos']['row']+1), (maxs[Direction.diagonal]['pos']['col']+1)))
        print('Reverse diagonally: %d starting from %d. rows %d. column towards upper right' % (maxs[Direction.reverse_diagonal]['value'], \
             (maxs[Direction.reverse_diagonal]['pos']['row']+1), (maxs[Direction.reverse_diagonal]['pos']['col']+1)))
    except IndexError:
        sys.exit('Error finding maximum values!\n' \
                 'Try with smaller grid and/or item count')
    # Flip the objects to get the maximum (pure if stuff's kinda boring)
    flip = [(obj['value'], d) for (d, obj) in maxs.items()]
    [highest, direction] = max(flip)
    print('Maximum is: %d starting from %d. rows %d. column %s' % \
         (highest, (maxs[direction]['pos']['row']+1),(maxs[direction]['pos']['col']+1),str(direction)))

    # Print the original numbers grid visualizing the maximum values
    print_matrix(numbers, maxs[direction]['pos']['row'], maxs[direction]['pos']['col'], product_count, direction)

if __name__ == "__main__":
    main()

