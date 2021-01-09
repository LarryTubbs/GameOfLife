#!/usr/bin/python

"""
ZetCode wxPython tutorial

This program draws a line in
a paint event.

author: Jan Bodnar
website: zetcode.com
last edited: May 2018
"""

import wx

class Example(wx.Frame):

    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.SetTitle("Grid")
        self.Centre()

    def OnPaint(self, e):

        dc = wx.PaintDC(self)
        self.DrawGrid(dc, 20)

    def DrawGrid(self, dc, squareSize):
        # determine dimentions of client area
        clientSize = dc.GetSize()

        # draw grid of squares maintaining aspect ratio
        width = 20
        height = 20

        for x in range(1, int(clientSize.x / squareSize) + 1):
            # draw vertical lines
            dc.DrawLine(width * x, 0, width * x, clientSize.y)

        for y in range (1, int(clientSize.y / squareSize) + 1):
            # draw horizontal lines
            dc.DrawLine(0, height * y, clientSize.x, height * y)


def main():

    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
