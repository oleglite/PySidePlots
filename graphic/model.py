#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore
import utils


class GraphicModel(QtCore.QObject):
    data_updated = QtCore.Signal()

    def __init__(self):
        super(GraphicModel, self).__init__()

        self.__points = []
        self.__bound = None

    @property
    def points(self):
        return self.__points

    @property
    def bounding_rect(self):
        return self.__bound

    def append_point(self, point):
        self.__points.append(point)
        self.__update_limits()
        self.data_updated.emit()

    @points.setter
    def points(self, value):
        self.__points = value
        self.__update_limits()
        self.data_updated.emit()

    def __update_limits(self):
        if len(self.points) > 1:
            self.__bound = utils.bound_points(self.points)