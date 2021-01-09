#!/usr/bin/python

"""
ZetCode wxPython tutorial

This is a wx.MoveEvent event demostration.

author: Jan Bodnar
website: www.zetcode.com
last modified: April 2018
"""

import wx

class Example(wx.Frame):

    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)

        self.InitUI()


    def InitUI(self):

        wx.StaticText(self, label='x:', pos=(10,10))
        wx.StaticText(self, label='y:', pos=(10,30))
        wx.StaticText(self, label='q:', pos=(10,50))

        self.st1 = wx.StaticText(self, label='', pos=(30, 10))
        self.st2 = wx.StaticText(self, label='', pos=(30, 30))
        self.st3 = wx.StaticText(self, label='', pos=(30, 50))

        self.Bind(wx.EVT_MOVE, self.OnMove)

        self.SetSize((350, 250))
        self.SetTitle('Move event')
        self.Centre()

    def OnMove(self, e):

        x, y = e.GetPosition()
        self.st1.SetLabel(str(x))
        self.st2.SetLabel(str(y))
        # determine quadrant of the screen
        sys = wx.SystemSettings()
        scr_x = sys.GetMetric(wx.SYS_SCREEN_X)
        scr_y = sys.GetMetric(wx.SYS_SCREEN_Y)
        if x < (scr_x / 2):
            # left side of the screen
            if y < (scr_y / 2):
                #upper left
                self.st3.SetLabel('Upper Left')
            else:
                self.st3.SetLabel('Lower Left')
        else:
            #right side of the screen
            if y < (scr_y / 2):
                #upper right
                self.st3.SetLabel('Upper Right')
            else:
                self.st3.SetLabel('Lower Right')

def main():

    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
