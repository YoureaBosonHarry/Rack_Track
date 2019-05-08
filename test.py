from PyQt5 import QtGui
import cv2
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import time

class QtCapture(QtWidgets.QWidget):
    def __init__(self, *args):
        super(QtWidgets.QWidget, self).__init__()

        self.fps = 24
        self.cap = cv2.VideoCapture(0)

        self.video_frame = QtWidgets.QLabel()
        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(self.video_frame)
        self.setLayout(lay)
        self.start()

    def setFPS(self, fps):
        self.fps = fps

    def nextFrameSlot(self):
        ret, frame = self.cap.read()
        # OpenCV yields frames in BGR format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channels = frame.shape
        img = QtGui.QImage(frame, width, height, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)

    def start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000./self.fps)

    def stop(self):
        self.timer.stop()

    def deleteLater(self):
        self.cap.release()
        super(QtGui.QWidget, self).deleteLater()

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = QtCapture()
    ex.show()
    sys.exit(app.exec_())


# Run main
if __name__ == "__main__":
    main()
