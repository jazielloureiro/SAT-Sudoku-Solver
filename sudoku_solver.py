#!/bin/python3

from pysat.solvers import Glucose4
import argparse

def main(args):
    grid = read_grid(args.filepath)

    grid_mapping, inv_grid_mapping = get_grid_mapping()

    sudoku_cnf = add_clauses(grid, grid_mapping)

    # if sudoku_cnf.solve():
        # sudoku_solved = [inv_grid_mapping[i] for i in sudoku_cnf.get_model() if i > 0]
        # print_grid(sudoku_solved, args.simple_out)

def read_grid(file):
    grid = []

    with open(file) as data:
        for line in data:
            grid += [[int(i) for i in line.split(' ')]]

    return grid

def get_grid_mapping():
    grid_mapping = [[[0 for _ in range(9)] for _ in range(9)] for _ in range(9)]
    inv_grid_mapping = []
    c = 1

    for i in range(9):
        for j in range(9):
            for k in range(9):
                grid_mapping[i][j][k] = c
                inv_grid_mapping.append([i, j, k])
                c += 1

    return grid_mapping, inv_grid_mapping

def add_clauses(grid, grid_mapping):
    sudoku_cnf = Glucose4()

    add_square_clauses(sudoku_cnf, grid_mapping)

    for i in range(9):
        for j in range(9):
            for k in range(9):
                predicate = 'grid_{}_{}_{}'.format(i, k, j)

                for l in range(k + 1, 10):
                    sub_predicate = 'grid_{}_{}_{}'.format(i, l, j)
                    clause = [-grid_mapping[predicate], -grid_mapping[sub_predicate]]
                    sudoku_cnf.add_clause(clause)

    for i in range(9):
        for j in range(9):
            for k in range(9):
                predicate = 'grid_{}_{}_{}'.format(k, i, j)

                for l in range(k + 1, 10):
                    sub_predicate = 'grid_{}_{}_{}'.format(l, i, j)
                    clause = [-grid_mapping[predicate], -grid_mapping[sub_predicate]]
                    sudoku_cnf.add_clause(clause)
    
    for i in 1, 4, 7:
        for j in 1, 4, 7:
            for k in range(i, i + 3):
                for l in range(j, j + 3):
                    for m in range(9):
                        predicate = 'grid_{}_{}_{}'.format(k, l, m)

                        for n in range(i, i + 3):
                            for p in range(j, j + 3):
                                if k != n and l != p:
                                    sub_predicate = 'grid_{}_{}_{}'.format(n, p, m)
                                    clause = [-grid_mapping[predicate], -grid_mapping[sub_predicate]]
                                    sudoku_cnf.add_clause(clause)

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                predicate = 'grid_{}_{}_{}'.format(i + 1, j + 1, grid[i][j])
                sudoku_cnf.add_clause([grid_mapping[predicate]])

    return sudoku_cnf

def add_square_clauses(sudoku_cnf, grid_mapping):
    for i in range(9):
        for j in range(9):
            sqr_clause = []

            for k in range(9):
                sqr_clause += [grid_mapping[i][j][k]]

                for l in range(k + 1, 9):
                    sudoku_cnf.add_clause([-grid_mapping[i][j][k], -grid_mapping[i][j][l]])

            sudoku_cnf.add_clause(sqr_clause)

def print_grid(sudoku_solved, simple_out):
    sudoku = [[0] * 9 for i in range(9)]

    for i in sudoku_solved:
        row, col, num = [int(i) for i in i[-5:].split('_')]
        sudoku[row-1][col-1] = num
    
    if simple_out:
        for i in sudoku:
            for j in i:
                print(j, end=' ')
            print()
    else:
        print('-------------------------------------')

        for i in range(9):
            for j in range(9):
                print('| {} '.format(sudoku[i][j]), end='')

            if i < 8:
                print('|\n|---+---+---+---+---+---+---+---+---|')

        print('|\n-------------------------------------')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('filepath')
    parser.add_argument('-s', '--simple-out',
                        action='store_true',
                        help='show a simplified output')

    args = parser.parse_args()

    main(args)
