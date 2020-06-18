#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Register %%watch as ipython magic."""

import time

from IPython.core.magic import Magics, cell_magic, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import clear_output
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


@magics_class
class WatchMagics(Magics):
    @magic_arguments()
    @argument(
        "-p",
        "--path",
        dest="path",
        type=str,
        default="./",
        help="""
        provides the PATH to watch for file changes. If not provided, the
        current directory will be watched.
        """,
    )
    @argument(
        "-r",
        "--recursive",
        dest="recursive",
        action="store_true",
        default=True,
        help="""
        include subdirectories recursively when watching for file changes. This
        is the default behaviour.
        """,
    )
    @argument(
        "-nr",
        "--non-recursive",
        dest="recursive",
        action="store_false",
        help="""
        do not include subdirectories when watching for file changes.
        """,
    )
    @argument(
        "--patterns",
        dest="patterns",
        type=str,
        nargs='*',
        help="""
        look for files with these PATTERNS.
        """,
    )
    @argument(
        "--ignore",
        dest="ignore_patterns",
        type=str,
        nargs='*',
        help="""
        ignore files containing IGNORE_PATTERNS when watching for file changes.
        """,
    )
    @cell_magic
    def watch(self, line, cell):
        """watch for file changes and re-evaluate current cell."""
        args = parse_argstring(self.watch, line)
        if args.path:
            path = args.path
        recursive = args.recursive
        patterns = args.patterns
        ignore_patterns = args.ignore_patterns
        ignore_directories = True
        case_sensitive = True
        my_event_handler = PatternMatchingEventHandler(
            patterns, ignore_patterns, ignore_directories, case_sensitive
        )

        def run_again():
            ip = get_ipython()
            ip.run_cell(cell)

        def on_modified(event):
            clear_output()
            print(f"watch: {event.src_path} has been modified")
            # print("Interrupt kernel to stop (i-i in notebook, ctrl-c in console).")
            run_again()

        my_event_handler.on_modified = on_modified
        my_observer = Observer()
        my_observer.schedule(my_event_handler, path, recursive=recursive)

        # message
        if path == "." or path == "./":
            watchdir = "current directory"
        else:
            watchdir = path
        if recursive:
            rstr = "recursively"
        else:
            rstr = "non-recursively"

        print(f"Watching {watchdir} {rstr} for file changes.")
        print("Interrupt kernel to stop (i-i in notebook, ctrl-c in console).")
        # initialize by running the cell once
        ip = get_ipython()
        ip.run_cell(cell)
        # start watchdog
        my_observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()
        my_observer.join()
