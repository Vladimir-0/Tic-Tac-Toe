from random import choice
from typing import Union

from .board import Board
from .statistic import Statistic, GameResult
from .turn import Turn


class Core:
    def __init__(self, first_turn: Turn = Turn.Cross) -> None:
        self._board: Board = Board()
        self._turn: Turn = first_turn if isinstance(first_turn, Turn) \
            else choice((Turn.Cross, Turn.Zero))
        self._is_game_end: bool = False
        self._winner: Union[Turn, None] = None
        self._stat_x = Statistic()
        self._stat_o = Statistic()

    @property
    def is_game_end(self) -> bool:
        return self._is_game_end

    @property
    def winner(self) -> Union[Turn, None]:
        return self._winner

    @property
    def turn(self) -> Turn:
        return self._turn

    def stats(self, turn: Turn) -> Statistic:
        if turn == Turn.Cross:
            return self._stat_x
        else:
            return self._stat_o

    @property
    def board(self) -> Board:
        return self._board

    def reset(self, first_turn: Turn = Turn.Cross) -> None:
        self._board.reset()
        self._turn: Turn = first_turn if isinstance(first_turn, Turn) \
            else choice((Turn.Cross, Turn.Zero))
        self._is_game_end = False
        self._winner = None
        self._stat_x.reset()
        self._stat_o.reset()

    def _change_turn(self) -> None:
        self._turn = Turn.Zero if self._turn == Turn.Cross else Turn.Cross

    def _end_game(self, *, winner: Union[Turn, None]) -> None:
        self._is_game_end = True
        self._winner = winner

        if winner == Turn.Cross:
            self._stat_x.add_result(GameResult.win)
            self._stat_o.add_result(GameResult.lose)
        elif winner == Turn.Zero:
            self._stat_x.add_result(GameResult.lose)
            self._stat_o.add_result(GameResult.win)
        else:
            self._stat_x.add_result(GameResult.draw)
            self._stat_o.add_result(GameResult.draw)

    def next(self, cell: int) -> None:
        self._board[cell] = self._turn
        self._change_turn()

        if self._board.is_full():
            self._end_game(winner=None)
        elif self._board.is_win(Turn.Cross):
            self._end_game(winner=Turn.Cross)
        elif self._board.is_win(Turn.Zero):
            self._end_game(winner=Turn.Zero)

