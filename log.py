from __future__ import annotations
import sys
from typing import TextIO

class Log:
    ofile:TextIO = sys.stderr
    flags:set[str] = set()

    _flag:str

    def __init__(self, flag:str) -> None:
        self._flag = flag
    
    def __call__(self, *args) -> None:
        if self._flag in self.flags:
            print(f"{self._flag}: ", *args, file=self.ofile)

        