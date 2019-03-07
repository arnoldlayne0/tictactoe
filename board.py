from copy import deepcopy
import random
#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns

class TakenFieldError(Exception):
    pass

class Board:
    def __init__(self, size):
        self.size = size
        self.board = [['_'] * self.size for i in range(self.size)]
        rows = [[(i, j) for j in range(self.size)] for i in range(self.size)]
        cols = [[(i, j) for i in range(self.size)] for j in range(self.size)]
        diag_one = [[(i, i) for i in range(self.size)]]
        diag_two = [[(i, self.size - 1 - i) for i in range(self.size)]]
        self._all_combs = rows + cols + diag_one + diag_two
        self.moves_history = []

    def print_board(self):
        for row in self.board:
            print(row)

    def board_to_string(self):
        rows = []
        for row in self.board:
            rows.append(''.join(row))
        return '\n'.join(rows)

    def __str__(self):
        return self.board_to_string()

    def get_board_list(self):
        return [i for sub in self.board for i in sub]

    def get_legal_moves(self):
        return [i + 1 for i, p in enumerate(self.get_board_list()) if p == "_"]

    def num_to_ind(self, num):
        num -= 1
        return divmod(num, self.size)

    def ind_to_num(self, ind):
        return ind[0] * self.size + ind[1] + 1

    # uzywaj tego
    def _make_move(self, num, sym):
        row, col = self.num_to_ind(num)
        if self.board[row][col] != '_':
            raise TakenFieldError
        try:
            self.board[row][col] = sym
            return self
        except (IndexError, ValueError):
            pass

    def make_player_move(self, sym):
        while True:
            move = raw_input()
            try:
                move = int(move)
                self._make_move(move, sym)
                self.moves_history.append(move)
                break
            #except (Exception, IndexError, ValueError):
            #    print('move outside of the board, on a taken field or not a number, please make a valid move')
            except ValueError:
                print('insert a number')
            except IndexError:
                print('make a move within the board')
            except TakenFieldError:
                print('make a move on a field that is not already taken')

    def make_random_legal_move(self, sym):
        move = random.choice(self.get_legal_moves())
        self._make_move(move, sym)
        self.moves_history.append(move)

    def get_winner(self):
        for comb in self._all_combs:
            vals = {self.board[i][j] for (i, j) in comb}
            if len(vals) == 1 and (vals != {'_'}):
                return vals.pop()

    def board_finished(self):
        if self.get_winner() != None or len(self.get_legal_moves()) == 0:
            return True
        return False

    def moves_to_boards(self):
        boards = [Board(self.size) for i in range(len(self.moves_history)+1)]
        for i in range(1, len(self.moves_history)+1):
            if i % 2 == 0:
                sym = 'o'
            else:
                sym = 'x'
            m = self.moves_history[i-1]
            boards[i] = deepcopy(boards[i-1])._make_move(m, sym)
        boards = [b.board for b in boards]
        return boards

    def play_one_random_game(self):
        i = 0
        boards = []
        while self.board_finished() == False:
            if i % 2 == 0:
                sym = 'x'
            else:
                sym = 'o'
            self.make_random_legal_move(sym)
            boards.append(deepcopy(self.board))
            i += 1
        winner = self.get_winner() or 'draw'
        return winner, self.moves_history, boards

    def play_two_players(self):
        i = 0
        while self.board_finished() == False:
            if i % 2 == 0:
                sym = 'x'
            else:
                sym = 'o'
            self.make_player_move(sym)
            print(self.board_to_string())
            i += 1
        winner = self.get_winner() or 'draw'
        return winner, self.moves_history