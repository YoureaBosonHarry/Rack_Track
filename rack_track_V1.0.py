import cv2
import datetime
import imutils
import json
import os
import numpy as np
from imutils.video import VideoStream
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from pyzbar import pyzbar

def check_frame(frame):
    flag = False
    data = None
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        barcode_data = barcode.data.decode("utf-8")
        try:
            flag, data = validate_code(barcode_data)
        except (UnboundLocalError, TypeError):
            flag = False
    return flag, data

def validate_code(barcode_data):
    matrix, box = barcode_data.split(" ")
    with open(os.path.join(os.getcwd(), "racks.json"), 'r') as f:
        data = json.load(f)
    if matrix in data:
        return True, [matrix, box, data[matrix][box]]

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.showFullScreen()
        self.fps = 24
        self.font = self.font()
        self.font.setPointSize(14)
        self.main_ui()
        self.form_ui()
        self.stack.hide()
        for c1 in self.findChildren(QWidget):
            c1.setFont(self.font)

    def main_ui(self):
        self.main_gb = QGroupBox(self)
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_gb.setLayout(self.main_layout)
        self.layout.addWidget(self.main_gb)
        self.video_frame = QLabel(self)
        self.video_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.capture_button = QPushButton(self)
        self.capture_button.clicked.connect(self.cap)
        self.main_layout.addWidget(self.video_frame)
        self.main_layout.addWidget(self.capture_button)

    def form_ui(self):
        self.stack = QStackedWidget(self)
        self.layout.addWidget(self.stack)
        self.form_gb = QGroupBox(self)
        self.form_layout = QFormLayout()
        self.form_layout.setAlignment(Qt.AlignCenter)
        self.form_layout.setSpacing(12)
        self.form_gb.setLayout(self.form_layout)
        self.stack.addWidget(self.form_gb)
        self.location = QLabel(self)
        self.product = QLabel(self)
        self.size = QLabel(self)
        self.quantity = QLabel(self)
        self.item_no = QLabel(self)
        self.lot_no = QLabel(self)
        self.proto_no = QLabel(self)
        self.date_stored = QLabel(self)
        self.sent_to_storage = QLabel(self)
        self.proj_num = QLabel(self)
        self.q_spec = QLabel(self)
        self.contact = QLabel(self)
        self.form_layout.addRow(QLabel("Location:"), self.location)
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

    def fill_form(self, data):
        box = data[1].replace("_", " ").capitalize()
        keys = data[2].keys()
        self.stack.show()
        self.main_gb.hide()
        self.location.setText(f"{data[0]} {box}")
        self.product.setText(str(data[2]["Item_Group_1"][0]))
        self.size.setText(str(data[2]["Item_Group_1"][1]))
        self.quantity.setText(str(data[2]["Item_Group_1"][2]))
        self.item_no.setText(str(data[2]["Item_Group_1"][3]))
        self.lot_no.setText(str(data[2]["Item_Group_1"][4]))
        self.proto_no.setText(str(data[2]["Item_Group_1"][5]))
        self.date_stored.setText(str(data[2]["Item_Group_1"][6]))
        self.sent_to_storage.setText(str(data[2]["Item_Group_1"][7]))
        self.proj_num.setText(str(data[2]["Item_Group_1"][8]))
        self.q_spec.setText(str(data[2]["Item_Group_1"][11]))
        self.contact.setText(str(data[2]["Item_Group_1"][12]))

    def cap(self):
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)
        self.timer.start(1000./self.fps)

    def next_frame(self):
        flag = False
        ret, frame = self.cap.read()
        # OpenCV yields frames in BGR format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        width, height, channels = frame.shape
        img = QImage(frame, height, width, QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        scaled_width, scaled_height = self.video_frame.frameGeometry().width(), self.video_frame.frameGeometry().height()
        self.video_frame.setPixmap(pix.scaled(scaled_width, scaled_height))
        flag, data = check_frame(frame)
        if flag:
            self.stop(data)

    def stop(self, data):
        self.timer.stop()
        self.cap.release()
        cv2.destroyAllWindows()
        self.video_frame.hide()
        self.fill_form(data)


def main():
    import sys
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())


# Run main
if __name__ == "__main__":
    main()

