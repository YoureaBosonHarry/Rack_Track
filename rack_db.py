import json
import os
import re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMenu
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
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setLayout(self.master_layout)
        toolbar = QToolBar(self)
        spacer=QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.addWidget(spacer)
        columns_button = QToolButton(self)
        columns_button.setIcon(QIcon(os.path.join(os.getcwd(), "images", "options.png")))
        columns_button.setPopupMode(QToolButton.InstantPopup)
        columns_menu = QMenu(self)
        columns_button.setMenu(columns_menu)
        columns_menu.addAction(self.col_action("Location", 0))
        columns_menu.addAction(self.col_action("Item No.", 4))
        columns_menu.addAction(self.col_action("Lot No.", 5))
        columns_menu.addAction(self.col_action("Prototype No.", 6))
        columns_menu.addAction(self.col_action("Storage", 8))
        columns_menu.addAction(self.col_action("Project No.", 9))
        toolbar.addWidget(columns_button)
        toolbar.addSeparator()
        self.empty_boxes = QCheckBox("Show Empty Boxes", self)
        self.empty_rows = []
        self.empty_boxes.stateChanged.connect(self.show_empty)
        toolbar.addWidget(self.empty_boxes)
        search_bar = QLineEdit(self)
        search_bar.setClearButtonEnabled(True)
        search_bar.setPlaceholderText("Search...")
        search_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        search_bar.textEdited.connect(self.search_table)
        toolbar.addWidget(search_bar)
        self.master_layout.addWidget(toolbar)
        self.init_table()
        self.set_font()

    def col_action(self, title, col):
        action = QAction(title, self)
        action.setCheckable(True)
        action.changed.connect(lambda: self.column_change(col))
        return action

    def init_table(self):
        data = open_racksdb()
        self.table = QTableWidget(self)
        self.table.cellClicked.connect(self.cell_clicked)
        self.table.setColumnCount(12)
        self.table.setRowCount(len([j for i in data for j in data[i] for k in data[i][j]]))
        self.table.setHorizontalHeaderLabels(["Location", "Product Description", "Size", "Quanitity",
                                              "Item No.", "Lot No.", "Prototype No.",
                                              "Date Stored", "Sent to Storage", "Project No.",
                                              "QE/QN/QA", "Contact"])
        self.master_layout.addWidget(self.table)
        self.table.setColumnHidden(0, True)
        self.table.setColumnHidden(4, True)
        self.table.setColumnHidden(5, True)
        self.table.setColumnHidden(6, True)
        self.table.setColumnHidden(8, True)
        self.table.setColumnHidden(9, True)
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
                    self.row_ids[d] = [i, j]
                    loc = QTableWidgetItem()
                    loc.setData(Qt.DisplayRole, f'{i}, {j.replace("_", " ").capitalize()}')
                    loc.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(d, 0, loc)
                    for l, m in enumerate(self.get_box(i, j, k)):
                        item = QTableWidgetItem()
                        item.setData(Qt.DisplayRole, str(m))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.table.setItem(d, l+1, item)
                    if data[i][j][k][0]:
                        pass
                    else:
                        self.table.setRowHidden(d, True)
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

    def show_empty(self):
        if self.empty_boxes.isChecked():
            for i in range(self.table.rowCount()):
                if self.table.isRowHidden(i):
                    self.empty_rows.append(i)
                self.table.setRowHidden(i, False)
        else:
            print(self.empty_rows)
            for i in self.empty_rows:
                self.table.setRowHidden(i, True)
            self.empty_rows = []

    def column_change(self, column):
        if self.table.isColumnHidden(column):
            self.table.setColumnHidden(column, False)
        else:
            self.table.setColumnHidden(column, True)
