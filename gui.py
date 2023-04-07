import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from prettytable import PrettyTable

from column_generation import column_eneration

class NumericDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super(NumericDelegate, self).createEditor(parent, option, index)
        if isinstance(editor, QtWidgets.QLineEdit):
            reg_ex = QtCore.QRegExp("[0-9]+")
            validator = QtGui.QRegExpValidator(reg_ex, editor)
            editor.setValidator(validator)
        return editor
    
class MyTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.items_length = []
        self.items_demand = []
        self.items_count = 0
        self.product_length_int = 0

        self.add_button = QtWidgets.QPushButton("+")
        self.add_button.clicked.connect(self.add_row)
        self.clear_all_button = QtWidgets.QPushButton("Clear All")
        self.clear_all_button.clicked.connect(self.clear_all)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Length", "Quantity", ""])
        delegate = NumericDelegate(self.table)
        self.table.setItemDelegate(delegate)

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        self.product_length = QtWidgets.QLineEdit()
        self.product_length_validator = QtGui.QIntValidator()
        self.product_length_validator.setRange(0, 99999)
        self.product_length.setValidator(self.product_length_validator)
        self.product_length.setText("15")
        
        menu_layout = QtWidgets.QHBoxLayout()
        menu_layout.addWidget(self.product_length)
        menu_layout.addWidget(self.add_button)
        menu_layout.addWidget(self.clear_all_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(menu_layout)
        main_layout.addWidget(self.table)

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

    def clear_all(self):
        self.table.setRowCount(0)

    def save_data(self):
        self.product_length_int = int(self.product_length.text())
        
        rows = self.table.rowCount()
        items_length = []
        items_demand = []
        for row in range(0, rows):
            item_length = self.table.item(row,0)
            item_demand = self.table.item(row,1)
            if item_length is not None and  item_demand is not None:
                items_demand.append(int(item_demand.text()))
                items_length.append(int(item_length.text()))
      
        self.items_length = items_length
        self.items_demand = items_demand
        self.items_count = len(items_length)

class Plot(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.figure = plt.figure(figsize=(5,2))
        self.canvas = FigureCanvas(self.figure)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    
    def plot_data(self, results, items_length):
        items_length = np.array(items_length)
        
        results = [result[1] for result in results]
        result_matrix = np.array(results)*np.array(items_length)
        results = result_matrix.T

        names = list(range(results.shape[1]))
        width = 0.5
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        left = np.zeros(results.shape[1])
        for pattern in results:
            ax.barh(names, pattern, width, left=left)
            left += pattern
        
        ax.set_ylabel('Patterns')
        ax.set_xlabel('Length')
        ax.set_title("Patterns")
        self.canvas.draw()

    def update_graph(self):
        self.plot_data()

class Results(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.result_box = QtWidgets.QTextEdit(self)
        self.result_box.setMinimumSize(500,270)
        self.result_box.setReadOnly(True)
        self.result_box.setPlainText("The results will be displayed here")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.result_box)
        self.setLayout(layout)

    def print_start(self):
        self.result_box.setPlainText("Looking for the best solution...")
    
    def print_results(self, semiproduct_count, results, items_length):
        self.result_box.clear()
        self.result_box.insertPlainText("Best solution found\n\n")
        self.result_box.insertPlainText(f"""{semiproduct_count} pieces of the default length will be needed for production\n\n""")
        self.print_table(results, items_length)

    def print_table(self, results, items_length):
        # Console output
        table = PrettyTable()
        field_names = ["Pattern"]
        [field_names.append(str(item_len)) for item_len in items_length]
        table.field_names = field_names
        results = [result[1] for result in results]
        
        for i, result in enumerate(results):
            row = [str(i)]
            for j in range(len(items_length)):
                row.append(str(result[j]))
            table.add_row(row)

        print(table)
    
        # Gui Output
        [self.result_box.insertPlainText(f"{name}\t") for name in field_names]
        self.result_box.insertPlainText("\n")
        for j, result in enumerate(results):
            self.result_box.insertPlainText(f"{j}\t")
            for i in range(len(result)):
                self.result_box.insertPlainText(f"{result[i]}\t")
            self.result_box.insertPlainText("\n")

class UiWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("Cutting Stock")
        
        self.table = MyTable()
        self.table.setMinimumWidth(350)
        self.plot = Plot()
        self.results = Results()
        self.calculate_button = QtWidgets.QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.table)
        left_layout.addWidget(self.calculate_button)

        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addWidget(self.plot)
        right_layout.addWidget(self.results)
      
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        
        self.setLayout(main_layout)

    def calculate(self):
        self.results.print_start()
        self.table.save_data()
        semiproduct_count, cg_results = column_eneration(self.table.product_length_int, 
                                                            self.table.items_length, self.table.items_demand,
                                                            self.table.items_count)
            
        for i, (num, arr) in enumerate(cg_results):
            cg_results[i] = (num, arr.tolist())

        self.results.print_results(semiproduct_count, cg_results, self.table.items_length)
        self.plot.plot_data(cg_results, self.table.items_length)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UiWindow()
    window.show()
    sys.exit(app.exec_())