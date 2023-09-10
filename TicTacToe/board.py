from typing import Iterator, List, Union

from .turn import Turn


class Board:
    def __init__(self) -> None:
        self._brd: List[Union[Turn, None]] = list()
        self.reset()

    def reset(self) -> None:
        self._brd = [None for _ in range(9)]

    def is_win(self, player: Turn) -> bool:
        win_coords = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Горизонтальные линии
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Вертикальные линии
            (0, 4, 8), (2, 4, 6)              # Диагональные линии
        )

        for coords in win_coords:
            if all(self._brd[i] == player for i in coords):
                return True
        return False

    def is_full(self) -> bool:
        return None not in self._brd

    def __getitem__(self, item: int) -> Union[Turn, None]:
        return self._brd[item]

    def __setitem__(self, key: int, value: Turn) -> None:
        if isinstance(value, Turn):
            if not self._brd[key]:
                self._brd[key] = value
            else:
                raise KeyError(f"This cell ({key}) is already occupied!")
        else:
            raise TypeError(f"Error value type {type(value)}")

    def __len__(self) -> int:
        return len(self._brd)

    def __iter__(self) -> Iterator[Union[Turn, None]]:
        return iter(self._brd)

    def __repr__(self) -> str:
        t = [i.value if isinstance(i, Turn) else " " for i in self._brd]
        return f'<Board: {str(t)}>'
