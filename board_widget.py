import json
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
from PyQt5.QtGui import QPainter, QColor
from board import Board


class BoardWidget(QWidget):
    board = None

    def __init__(self, board):
        super().__init__()

        self.board = board

        self.initUI()

    def initUI(self):
        gridLayout = QGridLayout()

        # Add grid with crossword:
        for row in range(self.board.side):
            for col in range(self.board.side):
                if self.board.matrix[row][col] != '#':
                    letter_frame = QLineEdit()
                    letter_frame.setStyleSheet("""
                                        QLineEdit {
                                            border: 2px solid black;
                                            font-weight: bold;
                                            padding: 0px;
                                            margin: 0px;
                                            height: 40px;
                                            width: 40px;
                                        }
                                    """)
                    gridLayout.addWidget(letter_frame, row + 1, col)

        # Add board assignment:
        board_assignment = QLabel(self.board.get_words_description_text())
        gridLayout.addWidget(
            board_assignment,
            1,
            self.board.side,
            self.board.side,
            2
        )

        self.setLayout(gridLayout)

