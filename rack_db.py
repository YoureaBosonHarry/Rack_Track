import json
import os
import re
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex
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
        columns_menu.addAction(self.col_action("Location", 1))
        columns_menu.addAction(self.col_action("Item No.", 5))
        columns_menu.addAction(self.col_action("Lot No.", 6))
        columns_menu.addAction(self.col_action("Prototype No.", 7))
        columns_menu.addAction(self.col_action("Storage", 9))
        columns_menu.addAction(self.col_action("Project No.", 10))
        toolbar.addWidget(columns_button)
        toolbar.addSeparator()
        self.empty_boxes = QCheckBox("Show Empty Boxes", self)
        self.empty_rows = []
        self.hidden_rows = []
        self.edit_flag = False
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
        self.table.setColumnCount(13)
        self.table.setRowCount(len([j for i in data for j in data[i] for k in data[i][j]]))
        self.table.setHorizontalHeaderLabels(["Actions", "Location", "Product Description",
                                              "Size", "Quanitity", "Item No.", "Lot No.",
                                              "Prototype No.", "Date Stored", "Sent to Storage",
                                              "Project No.","QE/QN/QA", "Contact"])
        self.master_layout.addWidget(self.table)
        self.table.setColumnHidden(0, True)
        self.table.setColumnHidden(1, True)
        self.table.setColumnHidden(5, True)
        self.table.setColumnHidden(6, True)
        self.table.setColumnHidden(7, True)
        self.table.setColumnHidden(9, True)
        self.table.setColumnHidden(10, True)
        self.table.setShowGrid(False)
        self.table.setWordWrap(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.cellClicked.connect(self.open_editor)
        self.populate_table()

    def populate_table(self):
        data = open_racksdb()
        self.row_ids = {}
        d = 0
        for i in data:
            for j in data[i]:
                for n, k in enumerate(data[i][j]):
                    self.row_ids[d] = [i, j, k]
                    loc = QTableWidgetItem()
                    loc.setData(Qt.DisplayRole, f'{i}, {j.replace("_", " ").capitalize()}')
                    loc.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(d, 1, loc)
                    for l, m in enumerate(self.get_box(i, j, k)):
                        item = QTableWidgetItem()
                        item.setData(Qt.DisplayRole, str(m))
                        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.table.setItem(d, l+2, item)
                    if data[i][j][k][0]:
                        pass
                    else:
                        self.hidden_rows.append(d)
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
        self.empty_boxes.setChecked(False)
        items = self.table.findItems(event, Qt.MatchContains)
        visible_rows = [item.row() for item in items]
        for i in range(self.table.rowCount()):
            if i not in visible_rows:
                self.table.setRowHidden(i, True)
            else:
                if i not in self.hidden_rows:
                    self.table.setRowHidden(i, False)

    def show_empty(self):
        if self.empty_boxes.isChecked():
            for i in range(self.table.rowCount()):
                if self.table.isRowHidden(i):
                    self.empty_rows.append(i)
                self.table.setRowHidden(i, False)
        else:
            for i in self.empty_rows:
                self.table.setRowHidden(i, True)
            self.empty_rows = []

    def column_change(self, column):
        if self.table.isColumnHidden(column):
            self.table.setColumnHidden(column, False)
        else:
            self.table.setColumnHidden(column, True)

    def scan_signal(self, data):
        item_string = f'{data[0]}, {data[1].replace("_", " ").capitalize()}'
        f_i = self.table.findItems(item_string, Qt.MatchExactly)
        for i in f_i:
            self.table.scrollToItem(self.table.item(i.row(), i.column()))
            self.table.selectRow(i.row())

    def open_editor(self, i, j):
        if self.edit_flag is False:
            self.table.setColumnHidden(0, False)
            btn = QPushButton(self.table)
            menu = QMenu(self)
            btn.setMenu(menu)
            add = QAction("Add", self)
            edit = QAction("Edit", self)
            remove = QAction("Remove", self)
            menu.addAction(add)
            menu.addAction(edit)
            menu.addAction(remove)
            self.table.setCellWidget(i, 0, btn)
            add.triggered.connect(lambda: self.add_row(i+1))
            edit.triggered.connect(lambda: self.edit_row(i))

    def add_row(self, row):
        self.table.insertRow(row)

    def edit_row(self, row):
        self.edit_flag = True
        btn = QPushButton(self.table)
        btn.setIcon(QIcon(os.path.join(os.getcwd(), "images", "check.png")))
        btn.clicked.connect(lambda: self.complete_edit(row))
        self.table.setCellWidget(row, 0, btn)
        for i in range(1, self.table.columnCount()):
            self.table.item(row, i).setFlags((self.table.item(row, i).flags() ^ Qt.ItemIsEditable))

    def complete_edit(self, row):
        print(self.row_ids[row])
        new = [self.table.item(row, i).text() for i in range(2, self.table.columnCount())]
        
