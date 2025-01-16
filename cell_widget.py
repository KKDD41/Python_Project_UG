from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QVBoxLayout
)
from PyQt5.QtGui import QPainter, QColor


class CellWidget(QLineEdit):
    def __init__(self, task_number = None):
        super().__init__()

        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid black;
                font-weight: bold;
                padding: 2px;
                margin: 0px;
                height: 40px;
                width: 40px;
                text-align: center;
                font-size: 16pt;
            }
        """)
        self.setFixedSize(40, 40)

        if task_number:
            task_label = QLabel(str(task_number))
            task_label.setParent(self)

            task_label.setIndent(3)

