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
import os
import sys
import math
import time
import typing
import subprocess
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
        self.sub_process_output = ''



class RootView(urwid.WidgetWrap):
    """
    A class responsible for providing the application's interface and
    root display.
    """

    palette = [
    ]

    def __init__(self, controller):
        self.controller = controller
        self.started = True
        self.start_time = None
        self.offset = 0
        self.last_offset = None
        super().__init__(self.main_window())


    # Handler for a sub process
    def on_update_widget_qstat(self, data: bytes) -> bool:
        self.widget_qstat.set_text(data.decode("utf8"))
        return True
        

    def build_widget_hello_world(self):
        w = urwid.Text('Hello World\n')
        w = urwid.Filler(w, "top")
        return w

    def build_widget_subprocess(self):
        txt = urwid.Text('')
        return txt
    
    def pile(self):
        w = urwid.Pile(
            [
                (urwid.WEIGHT, 1, urwid.LineBox(self.hello_world())),
                (urwid.WEIGHT, 1, urwid.LineBox(self.hello_world())),
            ]
        )
        return w

    def main_window(self):
        self.widget_qstat = self.build_widget_subprocess()
        w = urwid.Columns(
            [
                (
                    urwid.WEIGHT, 
                    1, 
                    urwid.Pile(
                    [
                        (urwid.WEIGHT, 1, urwid.LineBox(urwid.Filler(self.widget_qstat), "qstat -a")),
                        (urwid.WEIGHT, 1, urwid.LineBox(self.build_widget_hello_world())),
                    ])
                ), 
                (
                    urwid.WEIGHT, 
                    1, 
                    urwid.Pile(
                    [
                        (urwid.WEIGHT, 1, urwid.LineBox(self.build_widget_hello_world())),
                        (urwid.WEIGHT, 1, urwid.LineBox(self.build_widget_hello_world())),
                    ])
                )
            ]
        )
        w = urwid.LineBox(w)
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
    
    def exit_on_enter(key: str | tuple[str, int, int, int]) -> None:
        if key == "enter":
            raise urwid.ExitMainLoop()


    def main(self):
        
        self.loop = urwid.MainLoop(self.view, self.view.palette)
        run_me = os.path.join(os.path.dirname(sys.argv[0]), "qstat_proxy.py")
        write_fd = self.loop.watch_pipe(self.view.on_update_widget_qstat)
        with subprocess.Popen(
            ["python3", "-u", run_me],  # noqa: S603,S607  # Example can be insecure
            stdout=write_fd,
            close_fds=True,
        ) as proc:
            self.loop.run()


def main():
    RootController().main()


if __name__ == "__main__":
    main()