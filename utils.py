#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections


Point = collections.namedtuple('Point', 'x y')
__Rect_namedtuple = collections.namedtuple('Rect', 'left bottom right top')

def Rect(*args, **kwargs):
    if len(args) == 1:
        qrect = args[0]
        return __Rect_namedtuple(left=qrect.left(),
                                 bottom=qrect.bottom(),
                                 right=qrect.right(),
                                 top=qrect.top())
    else:
        return __Rect_namedtuple(*args, **kwargs)


def pairs(values):
    """
    >>> list(pairs([]))
    []
    >>> list(pairs([0]))
    []
    >>> list(pairs([0, 1]))
    [(0, 1)]
    >>> list(pairs([0, 1, 2]))
    [(0, 1), (1, 2)]
    >>> list(pairs([0, 1, 2, 3]))
    [(0, 1), (1, 2), (2, 3)]

    >>> list(pairs(i for i in range(4)))
    [(0, 1), (1, 2), (2, 3)]
    """
    prev_value = None
    for value in values:
        if prev_value is not None:
            yield (prev_value, value)
        prev_value = value


def bound_points(points):
    """
    >>> bound_points([Point(1, 1), Point(1, 2), Point(2, 1), Point(2, 2), Point(0, 3)])
    Rect(left=0, bottom=1, right=2, top=3)
    """
    max_x = max(x for x, y in points)
    max_y = max(y for x, y in points)
    min_x = min(x for x, y in points)
    min_y = min(y for x, y in points)

    assert min_x < max_x
    assert min_y < max_y

    return Rect(left=min_x, bottom=min_y, right=max_x, top=max_y)


def update_bounding(rect, point):
    pass


def stroke_generator(min_value, max_value, value_interval, min_stroke, max_stroke, round_digits=6):
    """
    >>> list(stroke_generator(1, 11, 1, 100, 200))
    [(100, 1), (110, 2), (120, 3), (130, 4), (140, 5), (150, 6), (160, 7), (170, 8), (180, 9), (190, 10), (200, 11)]
    >>> list(stroke_generator(1, 11, 4, 100, 200))
    [(100, 1), (140, 5), (180, 9), (220, 13)]

    >>> list(stroke_generator(1.0, 2.1, 0.2, 10, 120))
    [(10, 1.0), (30, 1.2), (50, 1.4), (70, 1.6), (90, 1.8), (110, 2.0), (130, 2.2)]
    """
    if max_value != min_value and value_interval:
        coeff = float(max_stroke - min_stroke) / (max_value - min_value)  # multiply by 1000, because 110 / 1.1 < 100
        coeff = round(coeff, round_digits)

        stroke_value = float(min_value) if type(value_interval) is float else min_value
        while stroke_value <= max_value:
            stroke = round(min_stroke + (stroke_value - min_value) * coeff, round_digits)
            if type(stroke_value) is float:
                yield (int(stroke), round(stroke_value, round_digits))
            else:
                yield (int(stroke), stroke_value)
            stroke_value += value_interval


class QtPointsAdjuster:
    """
    >>> pa = QtPointsAdjuster(QRect(10, 10, 100, 50), (11, 11), (1, 1))
    >>> pa.adjust((1, 1))
    PySide.QtCore.QPoint(10, 60)
    >>> pa.adjust((2, 1))
    PySide.QtCore.QPoint(20, 60)
    >>> pa.adjust((1, 2))
    PySide.QtCore.QPoint(10, 55)
    >>> pa.adjust((2, 2))
    PySide.QtCore.QPoint(20, 55)
    >>> pa.adjust((3, 3))
    PySide.QtCore.QPoint(30, 50)
    >>> pa.adjust((11, 11))
    PySide.QtCore.QPoint(110, 10)
    """

    def __init__(self, bound_qrect, bound_rect):
        self.left = bound_qrect.left()
        self.top = bound_qrect.top()
        self.width = bound_qrect.width()
        self.height = bound_qrect.height()

        self.limit_points = bound_rect
        self.point_width = self.limit_points.right - self.limit_points.left
        self.point_height = self.limit_points.top - self.limit_points.bottom

        assert self.point_width != 0
        assert self.point_height != 0

    def adjust(self, point):
        point_x, point_y = point
        x = self.left + (point_x - self.limit_points.left) * self.width / self.point_width
        y = self.top + self.height - (point_y - self.limit_points.bottom) * self.height / self.point_height
        return Point(x, y)


class Direction:
    x_direction = 'x'
    y_direction = 'y'

    def __init__(self, direction):
        self.direction = direction

    def point(self, direction_pos, other_pos):
        if self.is_x():
            return Point(direction_pos, other_pos)
        elif self.is_y():
            return Point(other_pos, direction_pos)

    def rect_right(self, rect):
        if self.is_x():
            return rect.right
        elif self.is_y():
            return rect.bottom

    def is_x(self):
        return self.direction is self.x_direction

    def is_y(self):
        return self.direction is self.y_direction

Direction.X = Direction(Direction.x_direction)
Direction.Y = Direction(Direction.y_direction)