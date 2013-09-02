# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *
import sys
import utils
from graphic import model, view
import math


class DataThread(QThread):
    new_point = Signal(utils.Point)

    def run(self):
        for point in [utils.Point(i, math.sin(i/10.0)) for i in xrange(-100, 101)]:
            self.new_point.emit(point)
            self.msleep(100)


class MyMainWindow(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)

        self.resize(QSize(800, 600))

        self.model = model.GraphicModel()
        look = view.GraphicLook()
        self.view = view.GraphicView(self, self.model, look)
        self.model.data_updated.connect(self.view.update)
        self.setCentralWidget(self.view)

    @Slot(utils.Point)
    def add_point(self, point):
        self.model.append_point(point)


def main():
    app = QApplication(sys.argv)

    window = MyMainWindow(None)
    window.show()

    data_thread = DataThread()
    data_thread.new_point.connect(window.add_point)
    data_thread.start()

    app.exec_()
    sys.exit()


if __name__ == "__main__":
    main()