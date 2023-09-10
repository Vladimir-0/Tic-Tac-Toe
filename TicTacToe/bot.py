from random import choice

from .board import Board
from .turn import Turn


class Bot:
    @staticmethod
    def get_cell(board: Board, bot_turn: Turn) -> int:
        """Bot logic"""
        player_turn = Turn.Cross if bot_turn == Turn.Zero else Turn.Zero

        win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                     (0, 3, 6), (1, 4, 7), (2, 5, 8),
                     (0, 4, 8), (2, 4, 6))
        sides = (1, 3, 5, 7)
        corners = (2, 6, 8, 0)
        alg = ((0, 5, 7, 2, 6), (2, 3, 7, 0, 8), (6, 1, 5, 0, 8), (8, 1, 3, 2, 6))

        """If the next bot move leads to a victory
           return this move (highest priority)"""
        for win in win_coord:
            if board[win[0]] == board[win[1]] == bot_turn and board[win[2]] is None:
                return win[2]
            elif board[win[1]] == board[win[2]] == bot_turn and board[win[0]] is None:
                return win[0]
            elif board[win[0]] == board[win[2]] == bot_turn and board[win[1]] is None:
                return win[1]

        """If the next player move leads to a victory
           return the move that prevents it (high priority)"""
        for win in win_coord:
            if board[win[0]] == board[win[1]] == player_turn and board[win[2]] is None:
                return win[2]
            elif board[win[1]] == board[win[2]] == player_turn and board[win[0]] is None:
                return win[0]
            elif board[win[0]] == board[win[2]] == player_turn and board[win[1]] is None:
                return win[1]

        """Ставит в центр, если это первый ход бота"""
        if bot_turn not in board and board[4] is None:
            return 4

        """Ставит в пустую сторону, если игрок поставил в противоположные углы
        Обычно бот к этому моменту ставит в центр, что позволяет забрать инициативу"""
        if board[0] == board[8] == player_turn or board[2] == board[6] == player_turn:
            return choice([side for side in sides if board[side] is None])

        """
        (0, 5, 7, 2, 6)
        [ p |   | b ]
        [   |   | p ]
        [ b | p |   ]
        """
        for corner in alg:
            if board[corner[0]] == player_turn:

                if board[corner[1]] == player_turn and board[corner[3]] is None:
                    return corner[3]

                elif board[corner[2]] == player_turn and board[corner[4]] is None:
                    return corner[4]

        """Checks all corners and returns any free (low priority)"""
        free_corners = [corner for corner in corners if board[corner] is None]  # free corners list
        return choice(free_corners) if len(free_corners) > 0 else list(board).index(
            None)  # board.index(None) is placeholder
