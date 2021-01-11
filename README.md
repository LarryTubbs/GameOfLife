# John Conway's Game of Life

## Introduction

This program is a basic implementation of John Conway's Game of Life written in Python.  It requires wx.Python for its GUI.  For help with installation, see the [wxPython Downloads](https://wxpython.org/pages/downloads/) page for more information on installed wxPython for your platform.

## Usage

To run the program, pass the life.py file to your python3 interpreter on the command line for your operating system.

```
$ python3 life.py
```

Once loaded, size the window to the size you want, select the size of square you'd prefer (default is 20 pixels), click a pattern of squares into the grid, and select either > to step through life one generation at a time, or click >> to advance through life one gernation per second.  Pressing "||" will pause progression through life.  And clicking "Reset" will blank the grid and start over.