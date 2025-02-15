import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QStackedWidget,
    QMessageBox,
    QDialog,
    QVBoxLayout
)
from PyQt5.QtCore import QRect
from PyQt5 import QtGui
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

        self.puzzle_counter = QLabel(f"1 / {len(self.board_widgets[self.current_theme])}")

        self.previous_button = QPushButton("<<")
        self.next_button = QPushButton(">>")

        self.previous_button.clicked.connect(self.switch_to_previous_board)
        self.next_button.clicked.connect(self.switch_to_next_board)

        self.complete_button = QPushButton("Complete")
        self.complete_button.clicked.connect(self.on_complete)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.on_exit)

        self.initUI()

    def get_current_board_widget(self):
        return self.board_widgets[self.current_theme][self.current_board_widget_index]

    def initUI(self):
        self.setFixedHeight(500)
        self.setWindowIcon(QtGui.QIcon("./icons/crossword_icon.png"))

        # Add control elements:
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                text-align: right;
                font-size: 8pt;
                align: right;
                margin-left: 50px;
            }
        """)

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
        puzzle_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                text-align: right;
                font-size: 8pt;
                align: right;
                margin-left: 50px;
            }
        """)

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

        self.gridLayout.addWidget(
            self.previous_button,
            0,
            4
        )
        self.gridLayout.addWidget(
            self.next_button,
            0,
            5
        )

        self.gridLayout.addWidget(
            self.complete_button,
            0,
            6
        )
        self.gridLayout.addWidget(
            self.exit_button,
            0,
            7
        )

        # adding current board widget
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

    def set_current_board(self, new_index, new_theme):
        self.gridLayout.replaceWidget(
            self.get_current_board_widget(),
            self.board_widgets[new_theme][new_index]
        )
        self.get_current_board_widget().setParent(None)

        self.current_theme = new_theme
        self.current_board_widget_index = new_index

        self.puzzle_counter.setText(f"{new_index + 1} / {len(self.board_widgets[new_theme])}")

    def switch_theme(self):
        self.set_current_board(
            0,
            self.theme_dropdown.currentText()
        )

    def switch_to_next_board(self):
        if self.current_board_widget_index + 1 >= len(self.board_widgets[self.current_theme]):
            index_to_set = 0
        else:
            index_to_set = self.current_board_widget_index + 1

        self.set_current_board(
            index_to_set,
            self.current_theme
        )

    def switch_to_previous_board(self):
        if self.current_board_widget_index - 1 <= -1:
            index_to_set = len(self.board_widgets[self.current_theme]) - 1
        else:
            index_to_set = self.current_board_widget_index - 1

        self.set_current_board(
            index_to_set,
            self.current_theme
        )

    def on_complete(self):
        crossword_correctly_completed = self.get_current_board_widget().board.is_complete()

        dialog = QDialog(self)

        dialog.setFixedHeight(100)
        dialog.setFixedWidth(400)

        dialog.setWindowTitle("Crossword Completion")

        if crossword_correctly_completed:
            label = QLabel("Congratulations! Answers are correct.")
            dialog.setWindowIcon(QtGui.QIcon("./icons/tick.png"))
        else:
            label = QLabel("Answers are incorrect. Try once again.")
            dialog.setWindowIcon(QtGui.QIcon("./icons/cross.png"))

        label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                padding: 2px;
                margin: 10px;
                text-align: center;
                font-size: 10pt;
            }
        """)

        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(label)

        dialog.setLayout(dialog_layout)
        dialog.exec_()


    def on_exit(self):
        self.close()
