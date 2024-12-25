import sys
import os
import json

from board import Board


class GameTasksLoader:
    boards = dict()
    themes = None

    def __init__(self):
        self.themes = ['animals', 'city', 'nature', 'sport']

        for theme in self.themes:
            self.boards[theme] = [
                Board(f"./boards/{theme}/{filename}") for filename in os.listdir(f"./boards/{theme}/")
            ]


