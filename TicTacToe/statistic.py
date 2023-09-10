from enum import Enum


class GameResult(Enum):
    win = 0
    lose = 1
    draw = 2


class Statistic:
    def __init__(self) -> None:
        self._win_rate = 0
        self._lose_rate = 0
        self._draw_rate = 0

    def add_result(self, game_result: GameResult) -> None:
        if isinstance(game_result, GameResult):
            if game_result == GameResult.win:
                self._win_rate += 1
            elif game_result == GameResult.lose:
                self._lose_rate += 1
            else:
                self._draw_rate += 1
        else:
            ValueError("Invalid game result!")

    def reset(self) -> None:
        self._win_rate = 0
        self._lose_rate = 0
        self._draw_rate = 0

    @property
    def win_rate(self) -> int:
        return self._win_rate

    @property
    def lose_rate(self) -> int:
        return self._lose_rate

    @property
    def draw_rate(self) -> int:
        return self._draw_rate

    @property
    def total_games(self) -> int:
        return self._win_rate + self._lose_rate + self._draw_rate

    @property
    def win_lose(self) -> float:
        return self._win_rate / self._lose_rate if self._lose_rate else float("inf")

    def percent(self, game_result: GameResult) -> float:
        if isinstance(game_result, GameResult):
            if game_result == GameResult.win:
                t = self._win_rate
            elif game_result == GameResult.lose:
                t = self._lose_rate
            else:
                t = self._draw_rate
            return t / self.total_games if self.total_games else float("inf")
        else:
            raise ValueError("Invalid ")
