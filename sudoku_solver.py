#!/bin/python3

from pysat.solvers import Glucose4, Solver

def read_grid(file):
    grid = []

    with open(file) as data:
        for line in data:
            grid += [[int(i) for i in line.split(' ')]]

    return grid

def get_grid_mapping():
    grid_mapping = {}
    inv_grid_mapping = {}
    c = 1

    for i in range(1, 10):
        for j in range(1, 10):
            for k in range(1, 10):
                predicate = 'grid_{}_{}_{}'.format(i, j, k)
                grid_mapping[predicate] = c
                inv_grid_mapping[c] = predicate
                c += 1

    return grid_mapping, inv_grid_mapping

def add_clauses(grid_mapping, inv_grid_mapping):
    sudoku_cnf = Glucose4()

    for i in range(1, 10):
        for j in range(1, 10):
            clause = []

            for k in range(1, 10):
                predicate = 'grid_{}_{}_{}'.format(i, j, k)
                clause += [grid_mapping[predicate]]

                for l in range(k + 1, 10):
                    sub_predicate = 'grid_{}_{}_{}'.format(i, j, l)
                    sub_clause = [-grid_mapping[predicate], -grid_mapping[sub_predicate]]
                    sudoku_cnf.add_clause(sub_clause)

            sudoku_cnf.add_clause(clause)

    for i in range(1, 10):
        for j in range(1, 10):
            for k in range(1, 10):
                predicate = 'grid_{}_{}_{}'.format(i, k, j)

                for l in range(k + 1, 10):
                    sub_predicate = 'grid_{}_{}_{}'.format(i, l, j)
                    clause = [-grid_mapping[predicate], -grid_mapping[sub_predicate]]
                    sudoku_cnf.add_clause(clause)

    if sudoku_cnf.solve():
        sudoku = [i for i in sudoku_cnf.get_model() if i > 0]

        for i in sudoku:
            print(inv_grid_mapping[i])

if __name__ == '__main__':
    grid_mapping, inv_grid_mapping = get_grid_mapping()

    add_clauses(grid_mapping, inv_grid_mapping)
