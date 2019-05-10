
import os
import re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

class Dialog_Form(QWidget):
    def __init__(self, data):
        super().__init__()
        self.master_layout = QVBoxLayout()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setLayout(self.master_layout)
        self.toolbar = QToolBar(self)
        self.combobox = QComboBox(self)
        self.toolbar.addWidget(self.combobox)
        self.master_layout.addWidget(self.toolbar)
        self.combobox.currentTextChanged.connect(self.switch_page)
        self.data = data
        self.current_item = 1

    def set_font(self, size=14):
        self.font = self.font()
        self.font.setPointSize(size)
        for c1 in self.findChildren(QWidget):
            c1.setFont(self.font)

    def add_pages(self, num):
        for i in range(num):
            self.combobox.addItem(f"Item Group {i+1}")

    def switch_page(self):
        page = re.findall(r"\d{1,}", self.combobox.currentText())
        page = int(page[0]) - 1
        try:
            self.stack.setCurrentIndex(page)
        except AttributeError:
            pass

    def create_stack(self, stack_num):
        self.add_pages(stack_num)
        self.stack_dict = {i: QWidget(self) for i in range(stack_num)}
        self.form_dict = {i: QFormLayout() for i in range(stack_num)}
        self.stack = QStackedWidget(self)
        self.master_layout.addWidget(self.stack)
        for i in self.stack_dict:
            self.stack.addWidget(self.stack_dict[i])
            self.form_ui(i)

    def form_ui(self, stack_num):
        self.form_dict[stack_num].setAlignment(Qt.AlignCenter)
        self.form_dict[stack_num].setSpacing(12)
        self.stack_dict[stack_num].setLayout(self.form_dict[stack_num])
        array, box = self.data[0], self.data[1].replace("_", " ").capitalize()
        container = QWidget(self)
        container_layout = QHBoxLayout()
        container_layout.setAlignment(Qt.AlignLeft)
        container.setLayout(container_layout)
        container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.location = QLabel(f"{array}, {box}", self)
        add_button = QToolButton(self)
        add_button.setIcon(QIcon(os.path.join(os.getcwd(), "images", "add.png")))
        edit_button = QToolButton(self)
        edit_button.setIcon(QIcon(os.path.join(os.getcwd(), "images", "edit.png")))
        trash_button = QToolButton(self)
        trash_button.setIcon(QIcon(os.path.join(os.getcwd(), "images", "remove.png")))
        container_layout.addWidget(self.location)
        container_layout.addWidget(add_button)
        container_layout.addWidget(edit_button)
        container_layout.addWidget(trash_button)
        self.product = QLabel(self.data[2][f"Item_Group_{stack_num + 1}"][0], self)
        self.size = QLabel(self.data[2][f"Item_Group_{stack_num + 1}"][1], self)
        self.quantity = QLabel(self.data[2][f"Item_Group_{stack_num + 1}"][2], self)
        self.item_no = QLabel(self.data[2][f"Item_Group_{stack_num + 1}"][3], self)
        self.lot_no = QLabel(self.data[2][f"Item_Group_{stack_num + 1}"][4], self)
        self.proto_no = QLabel(self.data[2][f"Item_Group_{stack_num + 1}"][5], self)
        self.date_stored = QLabel(self.data[2][f"Item_Group_{stack_num + 1}"][6], self)
        self.sent_to_storage = QLabel(self.data[2][f"Item_Group_{stack_num + 1}"][7], self)
        self.proj_num = QLabel(self.data[2][f"Item_Group_{stack_num + 1}"][8], self)
        self.q_spec = QLabel(self.data[2][f"Item_Group_{stack_num + 1}"][9], self)
        self.contact = QLabel(self.data[2][f"Item_Group_{stack_num + 1}"][10], self)
        self.form_dict[stack_num].addRow(QLabel("Location:"), container)
        self.form_dict[stack_num].addRow(QLabel("Product:"), self.product)
        self.form_dict[stack_num].addRow(QLabel("Size:"), self.size)
        self.form_dict[stack_num].addRow(QLabel("Quantity:"), self.quantity)
        self.form_dict[stack_num].addRow(QLabel("Item Number:"), self.item_no)
        self.form_dict[stack_num].addRow(QLabel("Lot Number:"), self.lot_no)
        self.form_dict[stack_num].addRow(QLabel("Prototype Number:"), self.proto_no)
        self.form_dict[stack_num].addRow(QLabel("Date Stored:"), self.date_stored)
        self.form_dict[stack_num].addRow(QLabel("Sent to LT Storage:"), self.sent_to_storage)
        self.form_dict[stack_num].addRow(QLabel("Project Number:"), self.proj_num)
        self.form_dict[stack_num].addRow(QLabel("QE/QA/QN:"), self.q_spec)
        self.form_dict[stack_num].addRow(QLabel("Contact:"), self.contact)
        #self.set_font()

