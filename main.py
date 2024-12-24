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
from board import BoardWidget


def main():
    app = QApplication(sys.argv)
    ex = BoardWidget("./boards/animals/sample_1.json")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()