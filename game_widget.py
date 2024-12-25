import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QStackedWidget
)
from PyQt5.QtCore import QRect

from board import Board
from board_widget import BoardWidget
from game_tasks_loader import GameTasksLoader


class GameWidget(QWidget):
    board_widgets = dict()
    game_tasks_loader = None
    current_theme = None
    current_board_widget_index = None

    def __init__(self):
        super().__init__()

        # Initialize board widgets:
        self.current_theme = "animals"
        self.game_tasks_loader = GameTasksLoader()

        for theme in self.game_tasks_loader.themes:
            self.board_widgets[theme] = [BoardWidget(board) for board in self.game_tasks_loader.boards[theme]]

        self.current_board_widget_index = 0


        # Initialize main UI controls:
        self.gridLayout = QGridLayout()

        self.theme_dropdown = QComboBox()
        self.theme_dropdown.addItems(self.game_tasks_loader.themes)
        self.theme_dropdown.currentTextChanged.connect(self.switch_theme)

        self.puzzle_counter = QLabel(f"0 / {len(self.board_widgets[self.current_theme])}")

        self.initUI()

    def get_current_board_widget(self):
        return self.board_widgets[self.current_theme][self.current_board_widget_index]

    def initUI(self):

        # Add control elements:
        theme_label = QLabel("Theme:")

        self.gridLayout.addWidget(
            theme_label,
            0,
            0
        )
        self.gridLayout.addWidget(
            self.theme_dropdown,
            0,
            1
        )

        puzzle_label = QLabel("Puzzle:")

        self.gridLayout.addWidget(
            puzzle_label,
            0,
            2
        )
        self.gridLayout.addWidget(
            self.puzzle_counter,
            0,
            3
        )

        previous_button = QPushButton("<<")
        next_button = QPushButton(">>")
        self.gridLayout.addWidget(
            previous_button,
            0,
            4
        )
        self.gridLayout.addWidget(
            next_button,
            0,
            5
        )

        complete_button = QPushButton("Complete")
        exit_button = QPushButton("Exit")
        self.gridLayout.addWidget(
            complete_button,
            0,
            6
        )
        self.gridLayout.addWidget(
            exit_button,
            0,
            7
        )

        self.gridLayout.addWidget(
            self.get_current_board_widget(),
            1,
            0,
            8,
            8
        )

        self.setLayout(self.gridLayout)

        self.setWindowTitle('Crossword Puzzle')
        self.setGeometry(200, 200, 1000, 700)

    def switch_theme(self):
        self.gridLayout.replaceWidget(
            self.get_current_board_widget(),
            self.board_widgets[self.theme_dropdown.currentText()][0]
        )
        self.get_current_board_widget().setParent(None)

        self.current_theme = self.theme_dropdown.currentText()
        self.current_board_widget_index = 0

        self.puzzle_counter.setText(f"1 / {len(self.board_widgets[self.current_theme])}")
