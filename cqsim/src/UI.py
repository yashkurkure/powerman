"""
CQStream UI in urwid using MVC
"""

from __future__ import annotations
import os
import sys
import math
import time
import typing
import subprocess
import urwid
import asyncio
import random
import fcntl

async def redis_listener(pipe):
    while True:
        await asyncio.sleep(10)
        random_number = random.randint(1, 100)
        os.write(pipe, str(random_number).encode())


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
    
    # Handler for a sub process
    def on_update_widget_redis(self, data: bytes) -> bool:
        self.widget_qstat.set_text(data.decode("utf8"))
        return True
        

    def build_widget_hello_world(self):
        w = urwid.Text('Hello World\n')
        w = urwid.Filler(w, "top")
        return w

    def build_widget_subprocess(self):
        txt = urwid.Text('')
        return txt


    def main_window(self):
        self.widget_qstat = self.build_widget_subprocess()
        self.widget_redis = self.build_widget_subprocess()
        w = urwid.Columns(
            [
                (
                    urwid.WEIGHT, 
                    1, 
                    urwid.Pile(
                    [
                        (urwid.WEIGHT, 1, urwid.LineBox(urwid.Filler(self.widget_qstat), "qstat -a")),
                        (urwid.WEIGHT, 1, urwid.LineBox(urwid.Filler(self.widget_redis), "redis-hook")),
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
        write_fd2 = self.loop.watch_pipe(self.view.on_update_widget_redis)
        with subprocess.Popen(
            ["python3", "-u", run_me],  # noqa: S603,S607  # Example can be insecure
            stdout=write_fd,
            close_fds=True,
        ) as proc:
            # Start the asyncio task
            asyncio_loop = asyncio.get_event_loop()
            asyncio_loop.create_task(redis_listener(write_fd2))
            self.loop.run()

def main():
    RootController().main()


if __name__ == "__main__":
    main()