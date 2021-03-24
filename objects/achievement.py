# -*- coding: utf-8 -*-

from typing import Callable

__all__ = ('Achievement',)

class Achievement:
    """A class to represent a single osu! achievement."""
    __slots__ = ('id', 'file', 'name',
                 'desc', 'cond', 'mode')

    def __init__(self, id: int, file: str, name: str,
                 desc: str, cond: Callable, mode: int) -> None:
        self.id = id
        self.file = file
        self.name = name
        self.desc = desc

        self.cond = cond
        self.mode = mode

    def __repr__(self) -> str:
        return f'{self.file}+{self.name}+{self.desc}'
