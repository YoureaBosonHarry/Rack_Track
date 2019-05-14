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
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QTreeWidgetItem
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
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)
        #self.showFullScreen()
        self.fps = 24
        self.font = self.font()
        self.font.setPointSize(14)
        self.main_ui()
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

    def cap(self):
        self.video_frame.show()
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
        self.video_frame.clear()
        self.display_capture(data)

    def display_capture(self, data):
        import rack_table
        self.dialog = rack_table.Dialog_Form(data)
        self.dialog.create_stack(len(data[2]))
        self.dialog.show()

def main():
    import sys
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())


# Run main
if __name__ == "__main__":
    main()

