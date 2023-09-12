from typing import Union

from customtkinter import CTk, CTkFont, CTkFrame, CTkLabel, CTkEntry, CTkButton, DISABLED, NORMAL
from ..core import Core
from ..turn import Turn
from time import sleep


class MainFrame(CTkFrame):
    def __init__(self, master: CTk, elements_font: CTkFont = None) -> None:
        super().__init__(master, fg_color="transparent")
        self._core = Core()

        # Config
        self._elements_font = elements_font

        # Create elements
        self.board_frame = CTkFrame(master=self, fg_color=None)
        self._buttons = [CTkButton(self.board_frame,
                                   text=" ",
                                   command=lambda cell=i: self._update(cell),
                                   font=CTkFont("Roboto", 100)) for i in range(9)]

        self.end_game_label = CTkLabel(master=self, text="", font=self._elements_font)
        self.restart_btn = CTkButton(self, text="Restart", command=self._restart, font=self._elements_font)

        self._bind_elements()
        self._pack_elements()

    def _update(self, cell: int) -> None:
        self._buttons[cell].configure(text=self._core.turn.value, state=DISABLED)
        self._core.next(cell)

        if self._core.is_game_end:
            self._set_board_buttons_state(DISABLED)
            if self._core.winner:
                self.end_game_label.configure(text=f"Winner is {self._core.winner.value}")
            else:
                self.end_game_label.configure(text="Draw!")

    def _restart(self):
        self._core.reset()
        self._set_board_buttons_state(NORMAL)
        for b in self._buttons:
            b.configure(text=" ")

    def _set_board_buttons_state(self, state: str):
        for b in self._buttons:
            b.configure(state=state.lower())

    def _bind_elements(self) -> None:
        """
        Bind the keyboard keys to the elements.
        """
        #self._IO_entry.bind("<Return>", lambda event=None: None)

    def _pack_elements(self) -> None:
        """
        Display all frame elements.
        """
        self.board_frame.pack()
        b = self._buttons[::]
        for i in range(3):
            for j in range(3):
                b.pop(0).grid(column=j, row=i, padx=5, pady=5)

        self.end_game_label.pack(pady=5)
        self.restart_btn.pack(pady=5)
