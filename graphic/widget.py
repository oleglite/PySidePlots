#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils
from graphic import model, view
from PySide.QtCore import *


class GraphicWidget(view.GraphicView):
    def __init__(self, parent, model=model.GraphicModel(), look=view.GraphicLook()):
        super(GraphicWidget, self).__init__(parent, model, look)
        self.model.data_updated.connect(self.update)

    @Slot(utils.Point)
    def add_point(self, point):
        self.model.append_point(point)