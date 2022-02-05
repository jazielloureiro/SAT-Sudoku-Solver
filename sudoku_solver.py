#!/bin/python3

def read_grid(file):
    grid = []

    with open(file) as data:
        for line in data:
            grid += [[int(i) for i in line.split(' ')]]

    return grid

if __name__ == '__main__':
    print(read_grid('data/sudoku'))
