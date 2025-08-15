from pathlib import Path
from dataclasses import dataclass

@dataclass
class CountLen:
    words: str = ""

    def read_text(self):
        with open("3280709.txt", "r", encoding="utf-8") as fr:
            self.words = fr.read()


    def count_len(self):
        print(f"Total words: {len(self.words.split())}")


def main():
    data = CountLen()
    data.read_text()
    data.count_len()

if __name__ == "__main__":
    main()

    