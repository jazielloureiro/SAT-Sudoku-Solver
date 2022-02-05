#!/bin/python3

def read_grid(file):
    grid = []

    with open(file) as data:
        for line in data:
            grid += [[int(i) for i in line.split(' ')]]

    return grid

def add_clauses():
    grid_mapping = {}
    inv_grid_mapping = {}
    c = 0

    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                for l in range(1, 4):
                    for m in range(1, 10):
                        predicate = 'grid_{}_{}_{}_{}_{}'.format(i, j, k, l, m)
                        grid_mapping[predicate] = c
                        inv_grid_mapping[c] = predicate
                        c += 1

    for i, j in grid_mapping.items():
        print(i, j)

if __name__ == '__main__':
    # print(read_grid('data/sudoku'))
    add_clauses()
