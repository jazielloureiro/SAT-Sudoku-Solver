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

def add_clauses(grid_mapping):
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

    for i in range(1, 10):
        for j in range(1, 10):
            for k in range(1, 10):
                predicate = 'grid_{}_{}_{}'.format(k, i, j)

                for l in range(k + 1, 10):
                    sub_predicate = 'grid_{}_{}_{}'.format(l, i, j)
                    clause = [-grid_mapping[predicate], -grid_mapping[sub_predicate]]
                    sudoku_cnf.add_clause(clause)
    
    for i in 1, 4, 7:
        for j in 1, 4, 7:
            for k in range(i, i + 3):
                for l in range(j, j + 3):
                    for m in range(1, 10):
                        predicate = 'grid_{}_{}_{}'.format(k, l, m)

                        for n in range(i, i + 3):
                            for p in range(j, j + 3):
                                if k != n and l != p:
                                    sub_predicate = 'grid_{}_{}_{}'.format(n, p, m)
                                    clause = [-grid_mapping[predicate], -grid_mapping[sub_predicate]]
                                    sudoku_cnf.add_clause(clause)

    return sudoku_cnf

def print_grid(sudoku_solved):
    sudoku = [[0] * 9 for i in range(9)]

    for i in sudoku_solved:
        row, col, num = [int(i) for i in i[-5:].split('_')]
        sudoku[row-1][col-1] = num
    
    print('-------------------------------------')

    for i in range(9):
        for j in range(9):
            print('| {} '.format(sudoku[i][j]), end='')

        if i < 8:
            print('|\n|---+---+---+---+---+---+---+---+---|')

    print('|\n-------------------------------------')

if __name__ == '__main__':
    grid_mapping, inv_grid_mapping = get_grid_mapping()

    sudoku_cnf = add_clauses(grid_mapping)

    if sudoku_cnf.solve():
        sudoku_solved = [inv_grid_mapping[i] for i in sudoku_cnf.get_model() if i > 0]
        print_grid(sudoku_solved)
