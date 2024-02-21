#!/usr/bin/env python
#
# Urwid graphics example program
#    Copyright (C) 2004-2011  Ian Ward
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Urwid web site: https://urwid.org/

"""
Urwid example demonstrating use of the BarGraph widget and creating a
floating-window appearance.  Also shows use of alarms to create timed
animation.
"""

from __future__ import annotations

import math
import time
import typing

import urwid

UPDATE_INTERVAL = 0.2


def sin100(x):
    """
    A sin function that returns values between 0 and 100 and repeats
    after x == 100.
    """
    return 50 + 50 * math.sin(x * math.pi / 50)


class RootModel:
    """
    A class responsible for storing the data that will be displayed
    on the graph, and keeping track of which mode is enabled.
    """

    data_max_value = 100

    def __init__(self):
        data = [
            ("Saw", list(range(0, 100, 2)) * 2),
            ("Square", [0] * 30 + [100] * 30),
            ("Sine 1", [sin100(x) for x in range(100)]),
            ("Sine 2", [(sin100(x) + sin100(x * 2)) / 2 for x in range(100)]),
            ("Sine 3", [(sin100(x) + sin100(x * 3)) / 2 for x in range(100)]),
        ]
        self.modes = []
        self.data = {}
        for m, d in data:
            self.modes.append(m)
            self.data[m] = d

    def get_modes(self):
        return self.modes

    def set_mode(self, m) -> None:
        self.current_mode = m

    def get_data(self, offset, r):
        """
        Return the data in [offset:offset+r], the maximum value
        for items returned, and the offset at which the data
        repeats.
        """
        lines = []
        d = self.data[self.current_mode]
        while r:
            offset %= len(d)
            segment = d[offset : offset + r]
            r -= len(segment)
            offset += len(segment)
            lines += segment
        return lines, self.data_max_value, len(d)


class RootView(urwid.WidgetWrap):
    """
    A class responsible for providing the application's interface and
    root display.
    """

    palette = [
        ("body", "black", "light gray", "standout"),
        ("header", "white", "dark red", "bold"),
        ("screen edge", "light blue", "dark cyan"),
        ("main shadow", "dark gray", "black"),
        ("line", "black", "light gray", "standout"),
        ("bg background", "light gray", "black"),
        ("bg 1", "black", "dark blue", "standout"),
        ("bg 1 smooth", "dark blue", "black"),
        ("bg 2", "black", "dark cyan", "standout"),
        ("bg 2 smooth", "dark cyan", "black"),
        ("button normal", "light gray", "dark blue", "standout"),
        ("button select", "white", "dark green"),
        ("line", "black", "light gray", "standout"),
        ("pg normal", "white", "black", "standout"),
        ("pg complete", "white", "dark magenta"),
        ("pg smooth", "dark magenta", "black"),
    ]

    def __init__(self, controller):
        self.controller = controller
        self.started = True
        self.start_time = None
        self.offset = 0
        self.last_offset = None
        super().__init__(self.main_window())

    def hello_world(self):
        return urwid.Text('Hello World')

    def main_window(self):
        self.hw1 = self.hello_world()
        self.hw2 = self.hello_world()
        self.hww1 = urwid.WidgetWrap(self.hw1)
        self.hww2 = urwid.WidgetWrap(self.hw2)
        vline = urwid.AttrMap(urwid.SolidFill("\u2502"), "line")

        w = urwid.Columns(
            [
                (urwid.WEIGHT, 2, self.hww1), 
                (1, vline), 
                (urwid.WEIGHT, 2, self.hww2)
            ],
            dividechars=1, 
            focus_column=2
        )


        w = urwid.Padding(w, ("fixed left", 1), ("fixed right", 0))
        w = urwid.AttrMap(w, "body")
        w = urwid.LineBox(w)
        w = urwid.AttrMap(w, "line")
        return w


class RootController:
    """
    A class responsible for setting up the model and view and running
    the application.
    """

    def __init__(self):
        self.animate_alarm = None
        self.model = RootModel()
        self.view = RootView(self)


    def main(self):
        self.loop = urwid.MainLoop(self.view, self.view.palette)
        self.loop.run()


def main():
    RootController().main()


if __name__ == "__main__":
    main()