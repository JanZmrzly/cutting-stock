import sys

from PyQt5 import QtCore, QtGui, QtWidgets

class UiWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("Cutting Stock")
        
        table = MyTable()
        table1 = MyTable()

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(table1)
        left_layout.addWidget(QtWidgets.QPushButton("Fuck"))

        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addWidget(table)
      

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        
        self.setLayout(main_layout)

class MyTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.add_button = QtWidgets.QPushButton("+")
        self.add_button.clicked.connect(self.add_row)
        self.clear_all_button = QtWidgets.QPushButton("Clear All")
        self.clear_all_button.clicked.connect(self.clear_all)
        self.calculate_button = QtWidgets.QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Length", "Quantity", ""])
        self.add_row()

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        
        self.product_length = QtWidgets.QLineEdit()
        self.product_length.setText("Product lenght")
        
        menu_layout = QtWidgets.QHBoxLayout()
        menu_layout.addWidget(self.product_length)
        menu_layout.addWidget(self.add_button)
        menu_layout.addWidget(self.clear_all_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(menu_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.calculate_button)

        self.setLayout(main_layout)
        
    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.add_remove_button(row_position)

    def add_remove_button(self, row_position):
        remove_button = QtWidgets.QPushButton("Remove Row")
        remove_button.clicked.connect(lambda: self.remove_row(remove_button))
        self.table.setCellWidget(row_position, 2, remove_button)
    
    @QtCore.pyqtSlot()
    def remove_row(self, remove_button):
        row = self.table.indexAt(remove_button.pos()).row()
        self.table.removeRow(row)
        print(row)

    def clear_all(self):
        self.table.setRowCount(0)

    def calculate(self):
        print(self.product_length.text())

        nrows = self.table.rowCount()
        group = []

        for row in range(0, nrows):
            item = self.table.item(row,1)
            item_text = item.text() # TODO: no text
            print(item_text)
            group.append(item)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UiWindow()
    window.show()
    sys.exit(app.exec_())