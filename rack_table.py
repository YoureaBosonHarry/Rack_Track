import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

class Dialog_Form(QWidget):
    def __init__(self):
        super().__init__()
        self.master_layout = QVBoxLayout()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setLayout(self.master_layout)
        self.current_item = 1

    def set_font(self, size=14):
        self.font = self.font()
        self.font.setPointSize(size)
        for c1 in self.findChildren(QWidget):
            c1.setFont(self.font)

    def form_data(self, data):
        self.data = data

    def form_ui(self):
        self.form_gb = QGroupBox(self)
        self.form_gb.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.form_layout = QFormLayout()
        self.form_layout.setAlignment(Qt.AlignCenter)
        self.form_layout.setSpacing(12)
        self.form_gb.setLayout(self.form_layout)
        self.master_layout.addWidget(self.form_gb)
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
        self.product = QLabel(self.data[2][f"Item_Group_{self.current_item}"][0], self)
        self.size = QLabel(self.data[2][f"Item_Group_{self.current_item}"][1], self)
        self.quantity = QLabel(self.data[2][f"Item_Group_{self.current_item}"][2], self)
        self.item_no = QLabel(self.data[2][f"Item_Group_{self.current_item}"][3], self)
        self.lot_no = QLabel(self.data[2][f"Item_Group_{self.current_item}"][4], self)
        self.proto_no = QLabel(self.data[2][f"Item_Group_{self.current_item}"][5], self)
        self.date_stored = QLabel(self.data[2][f"Item_Group_{self.current_item}"][6], self)
        self.sent_to_storage = QLabel(self.data[2][f"Item_Group_{self.current_item}"][7], self)
        self.proj_num = QLabel(self.data[2][f"Item_Group_{self.current_item}"][8], self)
        self.q_spec = QLabel(self.data[2][f"Item_Group_{self.current_item}"][9], self)
        self.contact = QLabel(self.data[2][f"Item_Group_{self.current_item}"][10], self)
        self.form_layout.addRow(QLabel("Location:"), container)
        self.form_layout.addRow(QLabel("Product:"), self.product)
        self.form_layout.addRow(QLabel("Size:"), self.size)
        self.form_layout.addRow(QLabel("Quantity:"), self.quantity)
        self.form_layout.addRow(QLabel("Item Number:"), self.item_no)
        self.form_layout.addRow(QLabel("Lot Number:"), self.lot_no)
        self.form_layout.addRow(QLabel("Prototype Number:"), self.proto_no)
        self.form_layout.addRow(QLabel("Date Stored:"), self.date_stored)
        self.form_layout.addRow(QLabel("Sent to LT Storage:"), self.sent_to_storage)
        self.form_layout.addRow(QLabel("Project Number:"), self.proj_num)
        self.form_layout.addRow(QLabel("QE/QA/QN:"), self.q_spec)
        self.form_layout.addRow(QLabel("Contact:"), self.contact)
        self.set_font()

