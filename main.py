from sys import argv, exit
from PyQt5.QtWidgets import QApplication
from calculator import Calculator

if __name__ == '__main__':
    app = QApplication(argv)
    widget = Calculator()
    widget.show()
    exit(app.exec_())