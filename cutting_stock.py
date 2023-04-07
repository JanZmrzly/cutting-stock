import sys
from PyQt5 import QtWidgets

from gui import UiWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = UiWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()