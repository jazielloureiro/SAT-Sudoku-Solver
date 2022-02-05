#!/bin/python3

def read_board(file):
    board = []

    with open(file) as data:
        for line in data:
            line = line.split(' ')
            board += [[int(i) for i in line]]

    return board

if __name__ == '__main__':
    print(read_board('data/sudoku'))
