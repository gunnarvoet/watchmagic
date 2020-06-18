# Copyright 2020 Gunnar Voet
#
# This file is part of watchmagic.
#
# watchmagic is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or any later version.
#
# watchmagic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with watchmagic.  If not, see <http://www.gnu.org/licenses/>.

"""`watchmagic` adds `%%watch` magic to IPython. When added to a cell, it watches
a given directory for file changes. Once a file is changed, the cell is
re-evaluated.

`watchmagic`'s real power lies in combining it with `%autoreload` which allows
to edit code in an external editor while watching the changes in a notebook in
real-time on every save.

## License

Copyright 2020 Gunnar Voet

`watchmagic` is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or any later version.

`watchmagic` is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with `watchmagic`.  If not, see <http://www.gnu.org/licenses/>.

## Installation

Clone the package from https://github.com/gunnarvoet/watchmagic. Then install
`watchmagic` by changing into the root directory and running

```shell
python setup.py install
```

or using [pip](https://pypi.org/project/pip/)

```shell
pip install .
```

## Usage

In the notebook run
```python
%load_ext watchmagic
```
Now you can use the magic by simply putting `%%watch` on the first line of the
cell you are working on. This will watch the current directory and its
subdirectories for file changes. For example:
```python
%%watch
print('hello world')
```
will watch the current directory and run the print statement on any file
changes. Interrupt the kernel to quit watching for file changes.

To make the magic available by default, add `watchmagic` to your
`ipython_config.py`:
```python
c.InteractiveShellApp.extensions = ['watchmagic']
```
Note that this is not the jupyter config file, but it will work in jupyter
notebooks.

The real power of the `%%watch` magic lies in combining it with IPython's
`%autoreload` magic. It allows to develop code in an external editor while
watching the results in real time on every file save. For example, if working
on the new function `overview_plot()` in the package `science_plots`, runnig
the following in a jupyter notebook will provide a real time view of the
results:
```python
import science_plots
%load_ext autoreload
%autoreload 2  # reload all packages
%load_ext watchmagic
```
```python
%%watch --ignore *.ipynb
science_plots.overview_plot()
```
Note that here we are watching the current directory by default, so
`science_plots` must be either in the local directory or one of its
subdirectories. `%%watch` will also ignore changes in jupyter notebook files
such that the `overview_plot()` is not run when the notebook is saved (and no
changes have ocurred in the source code).

## Config
The following default settings can be changed in `ipython_config.py`:
```
#------------------------------------------------------------------------------
# WatchMagics configuration
#------------------------------------------------------------------------------
c.WatchMagics.default_patterns = ['*.py']
c.WatchMagics.default_ignore_patterns = ['*.ipynb']
c.WatchMagics.default_case_sensitive = False
c.WatchMagics.default_ignore_directories = True
```
Command line options (if provided) will override the default settings.
"""

__author__ = "Gunnar Voet"
__email__ = "gvoet@ucsd.edu"
__version__ = "0.1.0"

from watchmagic.watch import WatchMagics


def load_ipython_extension(ipython):
    ipython.register_magics(WatchMagics)
