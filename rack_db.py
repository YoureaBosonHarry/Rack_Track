import json
import os
import re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


def open_racksdb():
    with open(os.path.join(os.getcwd(), "racks.json"), 'r') as f:
        data = json.load(f)
    return data


class Table_Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.master_layout = QVBoxLayout()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setLayout(self.master_layout)
        toolbar = QToolBar(self)
        spacer=QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.addWidget(spacer)
        search_bar = QLineEdit(self)
        search_bar.setClearButtonEnabled(True)
        search_bar.setPlaceholderText("Search...")
        search_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        search_bar.textEdited.connect(self.search_table)
        toolbar.addWidget(search_bar)
        self.master_layout.addWidget(toolbar)
        self.init_table()
        self.set_font()

    def init_table(self):
        data = open_racksdb()
        self.table = QTableWidget(self)
        self.table.cellClicked.connect(self.cell_clicked)
        self.table.setColumnCount(11)
        self.table.setRowCount(len([j for i in data for j in data[i] for k in data[i][j] if data[i][j][k][0]]))
        self.table.setHorizontalHeaderLabels(["Product Description", "Size", "Quanitity",
                                              "Item No.", "Lot No.", "Prototype No.",
                                              "Date Stored", "Sent to Storage", "Project No.",
                                              "QE/QN/QA", "Contact"])
        self.master_layout.addWidget(self.table)
        self.table.setColumnHidden(3, True)
        self.table.setColumnHidden(4, True)
        self.table.setColumnHidden(5, True)
        self.table.setColumnHidden(7, True)
        self.table.setColumnHidden(8, True)
        self.table.setShowGrid(False)
        self.table.setWordWrap(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.populate_table()

    def populate_table(self):
        data = open_racksdb()
        self.row_ids = {}
        d = 0
        for i in data:
            for j in data[i]:
                for n, k in enumerate(data[i][j]):
                    if data[i][j][k][0]:
                        self.row_ids[d] = [i, j]
                        for l, m in enumerate(self.get_box(i, j, k)):
                            item = QTableWidgetItem()
                            item.setData(Qt.DisplayRole, str(m))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.table.setItem(d, l, item)
                        d += 1

    def get_box(self, i, j, k):
        data = open_racksdb()
        return data[i][j][k]

    def set_font(self, size=14):
        self.class_font = self.font()
        self.class_font.setPointSize(size)
        for c1 in self.findChildren(QWidget):
            c1.setFont(self.class_font)

    def search_table(self, event):
        items = self.table.findItems(event, Qt.MatchContains)
        visible_rows = [item.row() for item in items]
        for i in range(self.table.rowCount()):
            if i not in visible_rows:
                self.table.setRowHidden(i, True)
            else:
                self.table.setRowHidden(i, False)

    def cell_clicked(self, row, col):
        a = self.row_ids[row]
        qb = QMessageBox(self)
        qb.setWindowTitle("Location")
        qb.setText(f"Items Located in {a[0]}, {a[1]}")
        qb.exec_()
