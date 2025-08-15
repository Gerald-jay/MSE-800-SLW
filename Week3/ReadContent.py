from ast import List
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class ReadContent:
    content: str = ""
    lines: Optional[list[str]] = None

    def read_text(self):
        with open("3280709.txt", "r", encoding="utf-8") as fr:
            self.lines = fr.readlines()
        for line in self.lines:
            print(line.rstrip("\n"))

    def write_text(self, lines):
        with open("new_dome.txt", "w", encoding="utf-8") as fw:
            for line in lines:
                fw.write(line)
        print("Done")


def main():
    data = ReadContent()
    data.read_text()
    data.write_text(data.lines)

if __name__ == "__main__":
    main()

    