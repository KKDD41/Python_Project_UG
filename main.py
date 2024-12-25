import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit
)
from PyQt5.QtCore import QRect
from board_widget import BoardWidget
from game_widget import GameWidget


def main():
    app = QApplication(sys.argv)
    ex = GameWidget()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()