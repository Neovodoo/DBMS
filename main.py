from PyQt5 import QtWidgets
from windows import AppWindow


if __name__ == '__main__':
    database = QtWidgets.QApplication([])
    window = AppWindow()
    window.show()
    database.exec()