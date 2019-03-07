from copy import deepcopy
import random
# import numpy as np
# import pandas as pd
from functools import reduce
import board


class TakenFieldError(Exception):
    pass


class LocalBoardFinishedError(Exception):
    pass


class NotPositiveIntegerError(Exception):
    pass


class BigBoard:
    def __init__(self, size):
        self.size = size
        self.subboards = [reduce((lambda x, y: x + y),
                                 ([board.Board(size)] for _ in range(self.size)))
                          for _ in range(self.size)]
        self.moves_history = []
        self.metaboard = board.Board(size)

    def big_board_to_string(self):
        big_rows = []
        for br in range(self.size):
            small_rows = []
            for sr in range(self.size):
                board_list = []
                for col in range(self.size):
                    row = ''.join(self.subboards[br][col].board[sr])
                    board_list.append(row)
                    res1 = '|'.join(board_list)
                small_rows.append(res1)
                res2 = '\n'.join(small_rows)
            big_rows.append(res2)
            div_list = ['/' * 3] * 3
            div_str = '\n' + '|'.join(div_list) + '\n'
            res3 = div_str.join(big_rows) + '\n'
        return res3

    def __str__(self):
        return self.big_board_to_string()

    def num_to_ind(self, num):
        if num < 1:
            raise NotPositiveIntegerError
        num -= 1
        return divmod(num, self.size)

    def get_subboard_list(self):
        return [i for sub in self.subboards for i in sub]

    def get_legal_subboards(self):
        subboard_list = self.get_subboard_list()
        return [i + 1 for i, p in enumerate(subboard_list) if p.board_finished() == False]

    def is_restricted(self):
        if len(self.moves_history) == 0:
            return False
        board_row, board_col = self.num_to_ind(self.moves_history[-1]['field'])
        if self.subboards[board_row][board_col].board_finished():
            return False
        return True

    def _make_move(self, board_num, field_num, sym):
        if board_num not in self.get_legal_subboards():
            raise LocalBoardFinishedError
        board_row, board_col = self.num_to_ind(board_num)
        field_row, field_col = self.num_to_ind(field_num)
        curr_local_board = self.subboards[board_row][board_col]
        if curr_local_board.board[field_row][field_col] != '_':
            raise TakenFieldError
        try:
            # nie lap bledu tutaj jesli chcesz lapac pozniej
            curr_local_board.board[field_row][field_col] = sym
            return self
        except (IndexError, ValueError):
            pass

    def make_player_move(self, sym):
        while True:
            if self.is_restricted():
                board_num = self.moves_history[-1]['field']
            else:
                board_num = input('input board number')
            field_num = input('input field number')
            try:
                board_num = int(board_num)
                field_num = int(field_num)
                self._make_move(board_num, field_num, sym)
                # self._last_move = field_num
                # append moves history in _make_move()
                self.moves_history.append({'number': len(self.moves_history), 'board': board_num, 'field': field_num})
                break
            except (NotPositiveIntegerError, ValueError):
                print('input a positive integer')
            except IndexError:
                print('make a valid move within the board')
            except LocalBoardFinishedError:
                print('make a move on a valid board')
            except TakenFieldError:
                print('field taken')

    def make_random_legal_move(self, sym):
        if self.is_restricted():
            board_num = self.moves_history[-1]['field']
        else:
            board_num = random.choice(self.get_legal_subboards())
        board_row, board_col = self.num_to_ind(board_num)
        field_num = random.choice(self.subboards[board_row][board_col].get_legal_moves())
        self._make_move(board_num, field_num, sym)
        self.moves_history.append({'number': len(self.moves_history), 'board': board_num, 'field': field_num})

    def get_local_winner(self):
        return [b.get_winner() or 'draw' if b.board_finished() else '_' for b in self.get_subboard_list()]

    def update_metaboard(self):
        self.metaboard = board.Board(self.size)
        for ind, sym in enumerate(self.get_local_winner()):
            self.metaboard._make_move(ind + 1, sym)

    def get_global_winner(self):
        if self.metaboard.board_finished():
            return self.metaboard.get_winner() or 'draw'
        else:
            return 'nobody yet'

    def play_one_random_game(self):
        i = 0
        while self.metaboard.board_finished() == False:
            if i % 2 == 0:
                sym = 'x'
            else:
                sym = 'o'
            self.make_random_legal_move(sym)
            i += 1
            self.update_metaboard()
        winner = self.get_global_winner()
        return winner

    def play_two_players(self):
        i = 0
        while self.metaboard.board_finished() == False:
            if i % 2 == 0:
                sym = 'x'
            else:
                sym = 'o'
            self.make_player_move(sym)
            print(self)
            i += 1
            self.update_metaboard()
        winner = self.get_get_winner() or 'draw'
        return winner

    # te dwie funkcje moga byc jedna
    def _human_or_machine_move(self, who, sym):
        if who == 'h':
            self.make_player_move(sym)
        elif who == 'm':
            self.make_random_legal_move(sym)
        else:
            raise Exception

    def play_against_the_machine(self):
        goes_first = None
        while goes_first not in 'hm':
            goes_first = input('choose who goes first (input h for human or m for machine)')
        i = 0
        if goes_first == 'h':
            sym_play_dict = {'x': 'h', 'o': 'm'}
        elif goes_first == 'm':
            sym_play_dict = {'x': 'm', 'o': 'h'}
        while self.metaboard.board_finished() == False:
            if i % 2 == 0:
                sym = 'x'
            else:
                sym = 'o'
            self._human_or_machine_move(sym_play_dict[sym], sym)
            print(self)
            i += 1
            self.update_metaboard()
        winner = self.get_get_winner() or 'draw'
        return winner
