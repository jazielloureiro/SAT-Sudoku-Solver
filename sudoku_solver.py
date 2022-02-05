#!/bin/python3

def read_grid(file):
    grid = []

    with open(file) as data:
        for line in data:
            grid += [[int(i) for i in line.split(' ')]]

    return grid

def get_grid_mapping():
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

    return grid_mapping, inv_grid_mapping

if __name__ == '__main__':
    # print(read_grid('data/sudoku'))
    grid_mapping, inv_grid_mapping = get_grid_mapping()

    for i, j in grid_mapping.items():
        print(i, j)

    for i, j in inv_grid_mapping.items():
        print(i, j)
