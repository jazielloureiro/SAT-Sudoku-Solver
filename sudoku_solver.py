#!/bin/python3

from pysat.solvers import Glucose4
import argparse

def main(args):
    grid = read_grid(args.filepath)

    grid_mapping, inv_grid_mapping = get_grid_mapping()

    sudoku_cnf = add_clauses(grid, grid_mapping)

    if sudoku_cnf.solve():
        sudoku_solved = [inv_grid_mapping[i-1] for i in sudoku_cnf.get_model() if i > 0]
        print_grid(sudoku_solved, args.simple_out)

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

    add_row_clauses(sudoku_cnf, grid_mapping)

    add_column_clauses(sudoku_cnf, grid_mapping)
    
    add_box_clauses(sudoku_cnf, grid_mapping)

    add_grid_clauses(sudoku_cnf, grid, grid_mapping)

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

def add_row_clauses(sudoku_cnf, grid_mapping):
    for i in range(9):
        for j in range(9):
            for k in range(9):
                for l in range(k + 1, 9):
                    sudoku_cnf.add_clause([-grid_mapping[i][k][j], -grid_mapping[i][l][j]])

def add_column_clauses(sudoku_cnf, grid_mapping):
    for i in range(9):
        for j in range(9):
            for k in range(9):
                for l in range(k + 1, 9):
                    sudoku_cnf.add_clause([-grid_mapping[k][i][j], -grid_mapping[l][i][j]])

def add_box_clauses(sudoku_cnf, grid_mapping):
    for i in 0, 3, 6:
        for j in 0, 3, 6:
            for k in range(i, i + 3):
                for l in range(j, j + 3):
                    for m in range(9):
                        for n in range(i, i + 3):
                            for p in range(j, j + 3):
                                if k != n and l != p:
                                    sudoku_cnf.add_clause([-grid_mapping[k][l][m], -grid_mapping[n][p][m]])

def add_grid_clauses(sudoku_cnf, grid, grid_mapping):
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                sudoku_cnf.add_clause([grid_mapping[i][j][grid[i][j] - 1]])

def print_grid(sudoku_solved, simple_out):
    sudoku = [[0] * 9 for i in range(9)]

    for i in sudoku_solved:
        row, col, num = i
        sudoku[row][col] = num + 1
    
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
