watchmagic
==========
``watchmagic`` adds ``%%watch`` magic to IPython. When added to a cell, it
watches a given directory for file changes. Once a file is changed, the cell is
re-evaluated.

``watchmagic``'s real power lies in combining it with ``%autoreload`` which
allows to edit code in an external editor while watching the changes in a
notebook in real-time on every save.

License
-------
Copyright 2020 Gunnar Voet

``watchmagic`` is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or any later version.

``watchmagic`` is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License along
with ``watchmagic``.  If not, see <http://www.gnu.org/licenses/>.

Installation
------------
Install via [pip](https://pypi.org/project/pip/):

.. code-block:: shell

    pip install watchmagic

Usage
-----
In the notebook run

.. code-block:: python

    %load_ext watchmagic

Now you can use the magic by simply putting `%%watch` on the first line of the
cell you are working on. This will watch the current directory and its
subdirectories for file changes. For example:

.. code-block:: python

    %%watch
    print('hello world')

will watch the current directory and run the print statement on any file
changes. Interrupt the kernel to quit watching for file changes.

To make the magic available by default, add ``watchmagic`` to your
``ipython_config.py``:

.. code-block:: python

    c.InteractiveShellApp.extensions = ['watchmagic']

Note that this is not the jupyter config file, but it will work in jupyter
notebooks.

The real power of the ``%%watch`` magic lies in combining it with IPython's
``%autoreload`` magic. It allows to develop code in an external editor while
watching the results in real time on every file save. For example, if working
on the new function ``overview_plot()`` in the package ``science_plots``, runnig
the following in a jupyter notebook will provide a real time view of the
results:

.. code-block:: python

    import science_plots
    %load_ext autoreload
    %autoreload 2  # reload all packages
    %load_ext watchmagic

.. code-block:: python

    %%watch --ignore *.ipynb
    science_plots.overview_plot()

Note that here we are watching the current directory by default, so
``science_plots`` must be either in the local directory or one of its
subdirectories. ``%%watch`` will also ignore changes in jupyter notebook files
such that the ``overview_plot()`` is not run when the notebook is saved (and no
changes have ocurred in the source code).

Options
-------
Several command line options exist. Run ``%%watch?`` to display the following
help screen::

    %watch [-p PATH] [-r] [-nr]
                [--patterns [PATTERNS [PATTERNS ...]]]
                [--ignore [IGNORE_PATTERNS [IGNORE_PATTERNS ...]]]

    Watch for file changes and re-evaluate current cell.

    optional arguments:
    -p PATH, --path PATH  provides the PATH to watch for file changes. If
                            not provided, the current directory will be
                            watched.
    -r, --recursive       include subdirectories recursively when
                            watching for file changes. This is the default
                            behaviour.
    -nr, --non-recursive  do not include subdirectories when watching for
                            file changes.
    --patterns <[PATTERNS [PATTERNS ...]]>
                            look for files with these PATTERNS.
    --ignore <[IGNORE_PATTERNS [IGNORE_PATTERNS ...]]>
                            ignore files containing IGNORE_PATTERNS when
                            watching for file changes.


Config
------
The following default settings can be changed in ``ipython_config.py``::

    #---------------------------------------------------------------
    # WatchMagics configuration
    #---------------------------------------------------------------
    c.WatchMagics.default_patterns = ['*.py']
    c.WatchMagics.default_ignore_patterns = ['*.ipynb']
    c.WatchMagics.default_case_sensitive = False
    c.WatchMagics.default_ignore_directories = True

Command line options (if provided) will override the default settings.
