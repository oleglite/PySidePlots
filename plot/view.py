#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *
import utils


class PlotLook:
    # Plot spacing
    hspace = 60
    vspace = 40

    # Background
    background_brush = QBrush(Qt.white)

    # Data
    data_pen = QPen(Qt.green)
    data_pen.setWidth(2)
    data_pen.setCapStyle(Qt.RoundCap)

    # Arrows and strokes
    arrows_pen = QPen(Qt.black)
    stroke_size = 3
    x_stroke_shift_qpoint = QPoint(-2, 20)
    x_value_interval = 10
    y_stroke_shift_qpoint = QPoint(-8, -14)
    y_value_interval = 0.1

    # Grid
    draw_grid = True
    grid_pen = QPen(Qt.gray)
    grid_pen.setStyle(Qt.DashLine)

    # Border
    draw_border = True
    border_pen = QPen(Qt.black)


class PlotView(QWidget):
    def __init__(self, parent, model, look):
        QWidget.__init__(self, parent)

        self.__model = model
        self.__look = look
        self.__drawing_area_rect = None

        self.setMinimumSize(QSize(self.__look.hspace, self.__look.vspace) * 2)

    @property
    def model(self):
        return self.__model

    def paintEvent(self, event):
        QWidget.paintEvent(self, event)

        painter = QPainter(self)
        self.__draw_background(painter)

        if len(self.__model.points) > 1:
            self.__draw_data(painter)
            self.__draw_arrows(painter)

        self.__draw_border(painter)

    def resizeEvent(self, event):
        rect = self.rect()
        self.__drawing_area_rect = QRect(rect.left() + self.__look.hspace,
                                         rect.top() + self.__look.vspace,
                                         rect.width() - 2 * self.__look.hspace,
                                         rect.height() - 2 * self.__look.vspace)

    def __draw_background(self, painter):
        painter.fillRect(self.rect(), self.__look.background_brush)

    def __draw_border(self, painter):
        if self.__look.draw_border:
            painter.setPen(self.__look.border_pen)
            painter.drawRect(self.__drawing_area_rect.adjusted(0, -1, -1, -1))

    def __draw_data(self, painter):
        painter.setPen(self.__look.data_pen)

        points_adjuster = utils.QtPointsAdjuster(self.__drawing_area_rect, self.__model.bounding_rect)
        qpoints = (QPoint(*points_adjuster.adjust(point)) for point in self.__model.points)
        for qpoint1, qpoint2 in utils.pairs(qpoints):
            painter.drawLine(qpoint1, qpoint2)

    def __draw_arrows(self, painter):
        x_strokes = utils.stroke_generator(self.__model.bounding_rect.left,
                                           self.__model.bounding_rect.right,
                                           self.__look.x_value_interval,
                                           self.__drawing_area_rect.left(),
                                           self.__drawing_area_rect.right())

        self.__draw_strokes(painter, utils.Direction.X, x_strokes,
                            self.__drawing_area_rect.bottom(),
                            self.__drawing_area_rect.top(),
                            self.__look.x_stroke_shift_qpoint)

        y_strokes = utils.stroke_generator(self.__model.bounding_rect.bottom,
                                           self.__model.bounding_rect.top,
                                           self.__look.y_value_interval,
                                           self.__drawing_area_rect.bottom(),
                                           self.__drawing_area_rect.top())

        self.__draw_strokes(painter, utils.Direction.Y, y_strokes,
                            self.__drawing_area_rect.left(),
                            self.__drawing_area_rect.right(),
                            self.__look.y_stroke_shift_qpoint)

    def __draw_strokes(self, painter, direction, strokes, strokes_line_pos, strokes_opposite_line_pos, shift_qpoint):
        for pos, value in strokes:
            self.__draw_grid_line(painter, direction, pos, strokes_line_pos, strokes_opposite_line_pos)
            self.__draw_stroke(painter, direction, pos, strokes_line_pos)
            self.__draw_stroke_text(painter, direction, value, pos, strokes_line_pos, shift_qpoint)

    def __draw_stroke(self, painter, direction, pos, strokes_line_pos):
        painter.setPen(self.__look.arrows_pen)
        painter.drawLine(QPoint(*direction.point(pos, strokes_line_pos + self.__look.stroke_size)),
                         QPoint(*direction.point(pos, strokes_line_pos - self.__look.stroke_size)))

    def __draw_stroke_text(self, painter, direction, value, pos, strokes_line_pos, shift_qpoint):
        painter.setPen(self.__look.arrows_pen)
        stroke_text = str(round(value, 3))
        if direction.is_x():
            painter.drawText(QPoint(*direction.point(pos, strokes_line_pos)) + shift_qpoint, stroke_text)
        elif direction.is_y():
            flags = Qt.AlignRight | Qt.AlignTop
            rect = painter.boundingRect(self.rect().left() + shift_qpoint.x(), pos + shift_qpoint.y(),
                                        strokes_line_pos, self.__drawing_area_rect.height(),
                                        flags, stroke_text)
            painter.drawText(rect, flags, stroke_text)

    def __draw_grid_line(self, painter, direction, pos, strokes_line_pos, strokes_opposite_line_pos):
        painter.setPen(self.__look.grid_pen)
        if self.__look.draw_grid:
            if not self.__look.draw_border or pos != direction.rect_right(utils.Rect(self.__drawing_area_rect)):
                painter.drawLine(QPoint(*direction.point(pos, strokes_line_pos)),
                                 QPoint(*direction.point(pos, strokes_opposite_line_pos)))