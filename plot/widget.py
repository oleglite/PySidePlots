#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils
from plot import model, view
from PySide.QtCore import *


class PlotWidget(view.PlotView):
    def __init__(self, parent, model=model.PlotModel(), look=view.PlotLook()):
        super(PlotWidget, self).__init__(parent, model, look)
        self.model.data_updated.connect(self.update)

    @Slot(utils.Point)
    def add_point(self, point):
        self.model.append_point(point)