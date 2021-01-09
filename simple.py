#!/usr/bin/env python
 
# simple.py

import wx
from wx.core import Height, Width

app = wx.App()

frame = wx.Frame(None, title='Simple application')
frame.SetSize(width=1000, height=1000)
frame.Show()

app.MainLoop()