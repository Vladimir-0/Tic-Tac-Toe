from enum import Enum
from typing import Union, Any

from TicTacToe import Bot, Core, Turn


class Member(Enum):
    player = 0
    bot = 1


class ConsoleGame:
    def __init__(self, member_1: Member, member_2: Member, *,
                 core: Core = Core(), bot: Bot = Bot(), board_template: str = None) -> None:
        self._core = core
        self._bot = bot

        if board_template:
            self._board_template = board_template
        else:
            self._board_template = ("[ {} | {} | {} ]\n"
                                    "[ {} | {} | {} ]\n"
                                    "[ {} | {} | {} ]\n")

        self._member_1 = member_1
        self._member_2 = member_2

        self._play = False
        self._current_member = member_1

    def _change_member(self) -> None:
        self._current_member = self._member_1 if self._current_member is self._member_2 else self._member_2

    def _player_get_cell(self) -> Union[None, int]:
        while True:
            inp = input("Введите номер клетки от 1 до 9: ").lower()
            if inp.isnumeric():
                inp = int(inp) - 1
                if 0 <= inp < len(self._core.board):
                    if self._core.board[inp] is None:
                        return inp
                    else:
                        print("Эта клетка уже занята!")
                else:
                    print("Число должно быть от 1 до 9!")
            elif inp in ("q", "quit", "e", "exit"):
                return None
            else:
                print("Ошибка! Введите число.")

    @staticmethod
    def _convert_turn(turn: Turn, none: Any = " ") -> str:
        if turn == Turn.Cross:
            return "X"
        elif turn == Turn.Zero:
            return "O"
        else:
            return none

    def _show_board(self) -> str:
        board = [self._convert_turn(item) for item in self._core.board]
        return self._board_template.format(*board)

    def _get_cell(self) -> int:
        if self._current_member == Member.player:
            return self._player_get_cell()
        else:
            return self._bot.get_cell(self._core.board, self._core.turn)

    def reset(self, first_turn: Turn = Turn.Cross) -> None:
        self._core.reset(first_turn)
        self._current_member = self._member_1

    def _ask_end_game(self) -> None:
        inp = input("Перезапустить игру - r\n"
                    "Статистика - s\n"
                    "Выход - e\n").lower()

        if inp in "r resrart р рестарт".split(" "):
            self.reset()
            return
        elif inp in "s stat statistic с статистика".split(" "):
            self._show_stats()
            self._ask_end_game()
        self.reset()
        self._play = False

    def _show_stats(self):
        stat_x = self._core.stats(Turn.Cross)
        stat_o = self._core.stats(Turn.Zero)

        for stat, turn in zip((stat_x, stat_o), "X O".split(" ")):
            print(f"Statistic for {turn}:\n"
                  f"total = {stat.total_games}\n"
                  f"win = {stat.win_rate}\n"
                  f"lose = {stat.lose_rate}\n"
                  f"draw = {stat.draw_rate}\n")
        input("Press Enter...")

    def _check_game_end(self) -> None:
        if self._core.is_game_end:
            print(self._show_board())
            if self._core.winner:
                print(f"{self._convert_turn(self._core.winner)} is win!")
            else:
                print("Game end.")
            self._ask_end_game()

    def main_loop(self) -> None:
        self.reset()
        self._play = True

        while self._play:
            if self._current_member == Member.player:
                print(self._show_board())
            try:
                self._core.next(self._get_cell())
            except Exception as e:
                print(e)
                self.reset()
            self._change_member()
            self._check_game_end()


if __name__ == '__main__':
    g = ConsoleGame(Member.player, Member.bot)
    g.main_loop()
