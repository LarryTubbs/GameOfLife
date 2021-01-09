#!/usr/bin/env python

# moving.py

import wx


class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,
            size=(300, 200))

        # self.Move((0, 0))
        self.Center()


def  main():

    app = wx.App()
    ex = Example(None, title='Moving')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()