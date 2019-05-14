import json
import os
import re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
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
        self.new_form = False

    def set_font(self, size=14):
        self.tab_font = self.font()
        self.tab_font.setPointSize(size)
        for c1 in self.findChildren(QWidget):
            c1.setFont(self.tab_font)

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
        print(self.data)
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
        add_button.clicked.connect(self.is_form_open)
        edit_button = QToolButton(self)
        edit_button.setIcon(QIcon(os.path.join(os.getcwd(), "images", "edit.png")))
        edit_button.clicked.connect(self.edit_item)
        trash_button = QToolButton(self)
        trash_button.setIcon(QIcon(os.path.join(os.getcwd(), "images", "remove.png")))
        container_layout.addWidget(self.location)
        container_layout.addWidget(add_button)
        container_layout.addWidget(edit_button)
        container_layout.addWidget(trash_button)
        self.product = QLabel(self.data[2][f"Item_Group_{stack_num + 1}"][0], self)
        self.size = QLabel(str(self.data[2][f"Item_Group_{stack_num + 1}"][1]), self)
        self.quantity = QLabel(str(self.data[2][f"Item_Group_{stack_num + 1}"][2]), self)
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
        self.set_font()

    def is_form_open(self):
        if self.new_form:
            pass
        else:
            self.new_form = True
            self.add_item()

    def new_item(self, stack_num):
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
        add_button.setIcon(QIcon(os.path.join(os.getcwd(), "images", "check.png")))
        add_button.clicked.connect(lambda: self.write_item(self.stack.count(), "Item Group Added"))
        container_layout.addWidget(self.location)
        container_layout.addWidget(add_button)
        product = QLineEdit(self)
        product.setPlaceholderText("Product")
        size = QLineEdit(self)
        size.setPlaceholderText("Size")
        quantity = QLineEdit(self)
        quantity.setPlaceholderText("Quantity")
        item_no = QLineEdit(self)
        item_no.setPlaceholderText("Item Number")
        lot_no = QLineEdit(self)
        lot_no.setPlaceholderText("Lot Number")
        proto_no = QLineEdit(self)
        proto_no.setPlaceholderText("Prototype Number")
        date_stored = QLineEdit(self)
        date_stored.setPlaceholderText("Date Stored")
        sent_to_storage = QLineEdit(self)
        sent_to_storage.setPlaceholderText("Date Sent to Storage")
        proj_num = QLineEdit(self)
        proj_num.setPlaceholderText("Project Number")
        q_spec = QLineEdit(self)
        q_spec.setPlaceholderText("QE/QN/QA")
        contact = QLineEdit(self)
        contact.setPlaceholderText("Contact")
        for i in self.findChildren(QLineEdit):
            i.setClearButtonEnabled(True)
            i.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.form_dict[stack_num].addRow(QLabel("Location:"), container)
        self.form_dict[stack_num].addRow(QLabel("Product:"), product)
        self.form_dict[stack_num].addRow(QLabel("Size:"), size)
        self.form_dict[stack_num].addRow(QLabel("Quantity:"), quantity)
        self.form_dict[stack_num].addRow(QLabel("Item Number:"), item_no)
        self.form_dict[stack_num].addRow(QLabel("Lot Number:"), lot_no)
        self.form_dict[stack_num].addRow(QLabel("Prototype Number:"), proto_no)
        self.form_dict[stack_num].addRow(QLabel("Date Stored:"), date_stored)
        self.form_dict[stack_num].addRow(QLabel("Sent to LT Storage:"), sent_to_storage)
        self.form_dict[stack_num].addRow(QLabel("Project Number:"), proj_num)
        self.form_dict[stack_num].addRow(QLabel("QE/QA/QN:"), q_spec)
        self.form_dict[stack_num].addRow(QLabel("Contact:"), contact)
        self.set_font()

    def add_item(self):
        count = self.stack.count()
        self.combobox.addItem(f"Item Group {count+1}")
        self.stack_dict[count] = QWidget(self)
        self.form_dict[count] = QFormLayout()
        self.stack.addWidget(self.stack_dict[count])
        self.new_item(count)
        self.combobox.setCurrentIndex(count)

    def edit_item(self):
        for i in range(self.form_dict[self.stack.currentIndex()].rowCount()):
            self.form_dict[self.stack.currentIndex()].removeRow(0)
        array, box = self.data[0], self.data[1].replace("_", " ").capitalize()
        new_container = QWidget(self)
        new_container_layout = QHBoxLayout()
        location = QLabel(f"{array}, {box}")
        new_container_layout.setAlignment(Qt.AlignLeft)
        new_container.setLayout(new_container_layout)
        new_container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        add_button = QToolButton(self)
        add_button.setIcon(QIcon(os.path.join(os.getcwd(), "images", "check.png")))
        add_button.clicked.connect(lambda: self.write_item())
        new_container_layout.addWidget(location)
        new_container_layout.addWidget(add_button)
        self.form_dict[self.stack.currentIndex()].addRow(QLabel("Location:"), new_container)
        self.form_dict[self.stack.currentIndex()].addRow(QLabel("Product:"), QLineEdit(self))
        self.form_dict[self.stack.currentIndex()].addRow(QLabel("Size:"), QLineEdit(self))
        self.form_dict[self.stack.currentIndex()].addRow(QLabel("Quantity:"), QLineEdit(self))
        self.form_dict[self.stack.currentIndex()].addRow(QLabel("Item Number:"), QLineEdit(self))
        self.form_dict[self.stack.currentIndex()].addRow(QLabel("Lot Number:"), QLineEdit(self))
        self.form_dict[self.stack.currentIndex()].addRow(QLabel("Prototype Number:"), QLineEdit(self))
        self.form_dict[self.stack.currentIndex()].addRow(QLabel("Date Stored:"), QLineEdit(self))
        self.form_dict[self.stack.currentIndex()].addRow(QLabel("Sent to LT Storage:"), QLineEdit(self))
        self.form_dict[self.stack.currentIndex()].addRow(QLabel("Project Number:"), QLineEdit(self))
        self.form_dict[self.stack.currentIndex()].addRow(QLabel("QE/QA/QN:"), QLineEdit(self))
        self.form_dict[self.stack.currentIndex()].addRow(QLabel("Contact:"), QLineEdit(self))

    def write_item(self, write_stack, msg_str):
        with open(os.path.join(os.getcwd(), "racks.json"), 'r') as f:
            items = json.load(f)
        ss = self.stack_dict[self.stack.currentIndex()]
        items[self.data[0]][self.data[1]][f"Item_Group_{write_stack}"] = [i.text().upper() for i in ss.findChildren(QLineEdit)]
        #with open(os.path.join(os.getcwd(), "racks.json"), 'w') as fw:
            #json.dump(items, fw, indent=4)
        self.new_form = False
        self.info_message("Success", f"{msg_str}")
        self.data[2][f"Item_Group_{write_stack}"] = items[self.data[0]][self.data[1]][f"Item_Group_{write_stack}"]
        for i in reversed(range(self.form_dict[self.stack.count()-1].count())):
            self.form_dict[self.stack.count()-1].itemAt(i).widget().deleteLater()
        self.form_ui(self.stack.count()-1)

    def info_message(self, t, m):
        qb = QMessageBox(self)
        qb.setWindowTitle(t)
        qb.setText(m)
        qb.setFont(self.tab_font)
        ret = qb.exec_()
