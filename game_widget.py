import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox
)
from PyQt5.QtCore import QRect

from board import Board
from board_widget import BoardWidget
from game_tasks_loader import GameTasksLoader


class GameWidget(QWidget):
    board_widgets = dict()
    game_tasks_loader = None

    def __init__(self):
        super().__init__()

        self.game_tasks_loader = GameTasksLoader()

        for theme in self.game_tasks_loader.themes:
            self.board_widgets[theme] = [BoardWidget(board) for board in self.game_tasks_loader.boards[theme]]

        self.initUI()

    def initUI(self):
        gridLayout = QGridLayout()

        # Add control elements:
        theme_label = QLabel("Theme:")
        theme_dropdown = QComboBox()
        theme_dropdown.addItems(self.game_tasks_loader.themes)

        gridLayout.addWidget(
            theme_label,
            0,
            0
        )
        gridLayout.addWidget(
            theme_dropdown,
            0,
            1
        )

        puzzle_label = QLabel("Puzzle:")
        puzzle_counter = QLabel("1 / 10")

        gridLayout.addWidget(
            puzzle_label,
            0,
            2
        )
        gridLayout.addWidget(
            puzzle_counter,
            0,
            3
        )

        previous_button = QPushButton("<<")
        next_button = QPushButton(">>")
        gridLayout.addWidget(
            previous_button,
            0,
            4
        )
        gridLayout.addWidget(
            next_button,
            0,
            5
        )

        complete_button = QPushButton("Complete")
        exit_button = QPushButton("Exit")
        gridLayout.addWidget(
            complete_button,
            0,
            6
        )
        gridLayout.addWidget(
            exit_button,
            0,
            7
        )

        gridLayout.addWidget(self.board_widgets[theme_dropdown.currentText()][0], 1, 0, 8, 8)

        self.setLayout(gridLayout)

        self.setWindowTitle('Crossword Puzzle')
        self.setGeometry(200, 200, 1000, 700)
        self.show()