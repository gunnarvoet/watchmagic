#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Register %%watch as ipython magic."""

import time

from IPython.display import clear_output
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def watch(line, cell):
    path=line
    recursive=True
    patterns="*.py"
    ignore_patterns=""
    func=None
    parameters=None
    ignore_directories = True
    case_sensitive = True

    my_event_handler = PatternMatchingEventHandler(
        patterns, ignore_patterns, ignore_directories, case_sensitive
    )

    def run_function():
        ip = get_ipython()
        ip.run_cell(cell)

    def on_modified(event):
        clear_output()
        print(f"watch: {event.src_path} has been modified")
        run_function()

    my_event_handler.on_modified = on_modified

    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=recursive)

    # initialize by running the cell once
    ip = get_ipython()
    ip.run_cell(cell)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
    my_observer.join()


# def load_ipython_extension(ipython):
#     """This function is called when the extension is
#     loaded. It accepts an IPython InteractiveShell
#     instance. We can register the magic with the
#     `register_magic_function` method of the shell
#     instance."""
#     ipython.register_magic_function(watch, 'cell')

