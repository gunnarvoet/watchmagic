#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Register %%watch as ipython magic."""

import time

from IPython.core.magic import Magics, cell_magic, magics_class
from IPython.core.magic_arguments import (argument, magic_arguments,
                                          parse_argstring)
from IPython.display import clear_output
from traitlets import Bool, List
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


@magics_class
class WatchMagics(Magics):

    # allow for setting default values in ipython_config.py:
    default_patterns = List([], config=True)
    default_ignore_patterns = List([], config=True)
    default_case_sensitive=Bool(False, config=True)
    default_ignore_directories=Bool(True, config=True)

    @magic_arguments()
    @argument(
        "-p",
        "--path",
        dest="path",
        type=str,
        default="./",
        help="""
        provides the PATH to watch for file changes. If not provided, the\n
        current directory will be watched.
        """,
    )
    @argument(
        "-r",
        "--recursive",
        dest="recursive",
        default=True,
        action="store_true",
        help="""
        include subdirectories recursively when watching for file changes.\n
        This is the default behaviour.
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
        nargs="*",
        help="""
        look for files with these PATTERNS.
        """,
    )
    @argument(
        "--ignore",
        dest="ignore_patterns",
        type=str,
        nargs="*",
        help="""
        ignore files containing IGNORE_PATTERNS when watching for file changes.
        """,
    )
    @cell_magic
    def watch(self, line, cell):
        """Watch directory and re-evaluate current cell on file changes."""
        args = parse_argstring(self.watch, line)
        path = args.path
        patterns = self.parse_defaults(args.patterns, self.default_patterns)
        ignore_patterns = self.parse_defaults(
            args.ignore_patterns, self.default_ignore_patterns
        )
        recursive = args.recursive
        ignore_directories = self.default_ignore_directories
        case_sensitive = self.default_case_sensitive
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

    def parse_defaults(self, argin, default):
        """Decide which parameters to use."""
        if argin:
            return argin
        else:
            if default:
                return default
            else:
                return None
