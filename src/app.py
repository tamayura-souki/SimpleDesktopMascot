import sys
import os
import json
import glob
import random
import time

from PySide2 import QtCore, QtGui, QtWidgets

class ImageViewer(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setMouseTracking(True)

        self.drag = False
        self.offset = QtCore.QPoint(0,0)

    def setImage(self, image):
        pixel = QtGui.QPixmap.fromImage(image)
        scene = QtWidgets.QGraphicsScene(self)
        photo = QtWidgets.QGraphicsPixmapItem()
        photo.setPixmap(pixel)
        scene.addItem(photo)
        self.setScene(scene)
        self.setGeometry(self.x(), self.y(),image.width(), image.height())

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            return

        self.drag = True
        self.offset = event.pos()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            return

        self.drag = False
        return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.drag == True:
            diff = event.pos() - self.offset
            diff = self.parent.mapToParent(diff)
            self.parent.setGeometry(
                diff.x(), diff.y(),
                self.parent.width(), self.parent.height()
            )
        return super().mouseMoveEvent(event)

class PeriodicallyProcess(QtCore.QThread):
    thread = QtCore.Signal()
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

        self.mutex = QtCore.QMutex()
        self.stopped = False
        self.interval = 1

    def setInterval(self, interval:float):
        self.interval = interval

    def __del__(self):
        self.stop()
        self.wait()

    def stop(self):
        with QtCore.QMutexLocker(self.mutex):
            self.stopped = True

    def restart(self):
        with QtCore.QMutexLocker(self.mutex):
            self.stopped = False

    def run(self):
        while not self.stopped:
            self.thread.emit()
            time.sleep(self.interval)

class Main(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        config = json.load(open("config.json"))

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
        self.setWindowTitle(config["app_name"])
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context)

        self.viewer = ImageViewer(self)
        self.images  = []
        self.loadImage(config["image_folder"])
        self.image_process = PeriodicallyProcess()
        self.image_process.setInterval(config["image_change_interval"])
        self.image_process.thread.connect(self.changeImage)
        self.image_process.start()

    def changeImage(self):
        self.setImage(random.choice(self.images))

    def loadImage(self, path:str):
        files = glob.glob(f"{path}/*.png")
        files += glob.glob(f"{path}/*.jpg")
        self.images = [QtGui.QImage(f) for f in files]

    def setImage(self, image:QtGui.QImage):
        self.viewer.setImage(image)
        self.setGeometry(self.x(), self.y(), image.width(), image.height())

        mask = QtGui.QPixmap.fromImage(image.createAlphaMask())
        self.setMask(mask)

    def context(self, pos):
        menu = QtWidgets.QMenu(self)
        exit_action = menu.addAction("終了")
        exit_action.triggered.connect(self.close)
        menu.exec_(self.mapToGlobal(pos))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    a = Main()
    a.show()
    sys.exit(app.exec_())