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




class Board:
    # General board parameters:
    side = None
    words_with_descriptions = None
    matrix = None
    matrix_current_fill = None
    matrix_words_coordinates = None

    # Board quality parameters:
    current_number_of_intersections = None
    samples_covered = None

    # Words location metadata:
    words_coordinates = None

    def __init__(self, board_filepath):
        with open(board_filepath, 'r') as f:
            board_data = json.load(f)

        self.side = board_data['board_size']
        self.words_with_descriptions = board_data['words_with_descriptions']
        self.words_coordinates = board_data['words_coordinates']

        self.matrix = [list(row) for row in board_data['board'].split('\n')]
        self.matrix_current_fill = [['#'] * self.side for _ in range(self.side)]

    def is_complete(self):
        for i in range(self.side):
            for j in range(self.side):
                if self.matrix[i][j] != self.matrix_current_fill[i][j]:
                    return False
        return True

    def get_words_description_text(self):
        board_assignment_text = ""

        for index, word_with_coordinates in enumerate(self.words_coordinates.items()):
            word = word_with_coordinates[0]
            coordinates = word_with_coordinates[1]

            board_assignment_text += f"""
            {index + 1} ({coordinates[2]}). {self.words_with_descriptions[word]} 
            """

        return board_assignment_text


class BoardWidget(QWidget):
    board = None

    def __init__(self, board_filepath):
        super().__init__()

        self.board = Board(board_filepath)
        self.initUI()

    def initUI(self):
        gridLayout = QGridLayout()


        # Add control elements:
        theme_label = QLabel("Theme:")
        theme_dropdown = QComboBox()
        theme_dropdown.addItems(["Animals", "City", "Nature", "Sport"])

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
                                            height: 40px;  # Adjust the size to make it square
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

        self.setWindowTitle('Crossword Puzzle')
        self.setGeometry(200, 200, 1000, 700)
        self.show()
