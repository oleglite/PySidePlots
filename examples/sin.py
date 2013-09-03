# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *
import sys, math
import utils, graphic


class DataThread(QThread):
    new_point = Signal(utils.Point)

    def __init__(self):
        super(DataThread, self).__init__()
        self.__is_alive = False

    def run(self):
        self.__is_alive = True
        for point in [utils.Point(i, math.sin(i / 10.0)) for i in xrange(-100, 101)]:
            if not self.__is_alive:
                return
            self.new_point.emit(point)
            self.msleep(100)

    def stop(self):
        assert self.__is_alive
        self.__is_alive = False


class ThreadController(QObject):
    def __init__(self, thread):
        super(ThreadController, self).__init__()

        self.__thread = thread

    def stop(self):
        self.__thread.stop()
        self.__thread.wait()


def main():
    app = QApplication(sys.argv)

    graphic_widget = graphic.Widget(None)
    graphic_widget.resize(QSize(800, 600))
    graphic_widget.show()

    data_thread = DataThread()
    data_thread.new_point.connect(graphic_widget.add_point)

    data_thread_controller = ThreadController(data_thread)
    graphic_widget.destroyed.connect(data_thread_controller.stop)

    data_thread.start()

    app.exec_()
    sys.exit()


if __name__ == "__main__":
    main()
