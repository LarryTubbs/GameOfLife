#!/usr/bin/env python

from os import curdir
from sys import flags
import wx
from wx.core import BoxSizer, FileDialogNameStr, PropagateOnce, RadioBoxNameStr, Size

class MainFrame(wx.Frame):

    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(600,600))

        self.InitUI()
        self.Centre()

    def InitUI(self):

        self.panel = wx.Panel(self)

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)

        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        # square size
        st1 = wx.StaticText(self.panel, label='Square Size')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        self.tcself.boxSize = wx.TextCtrl(self.panel)
        self.tcself.boxSize.Value = "20"
        hbox1.Add(self.tcself.boxSize, flag=wx.RIGHT, proportion=0, border=8)

        # reset button
        resetButton = wx.Button(self.panel, label="Reset")
        hbox1.Add(resetButton, flag=wx.RIGHT, proportion=0, border=8 )

        # start button
        startButton = wx.Button(self.panel, label=">>")
        hbox1.Add(startButton, flag=wx.RIGHT, proportion=0, border=8 )

        # pause button
        pauseButton = wx.Button(self.panel, label="||")
        hbox1.Add(pauseButton, flag=wx.RIGHT, proportion=0, border=8 )
    
        # step button
        stepButton = wx.Button(self.panel, label=">")
        hbox1.Add(stepButton, flag=wx.RIGHT, proportion=0, border=8 )
    
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        vbox.Add((-1, 10))

        self.ca = ClientArea(parent=self.panel, size=(100,100))
        vbox.Add(self.ca, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.sb = wx.StatusBar(self.panel)
        self.sb.SetStatusText("Ready")
        
        vbox.Add(self.sb, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=0)

        self.panel.Bind(wx.EVT_TEXT, self.onChangeself.boxSize, self.tcself.boxSize)
        self.panel.Bind(wx.EVT_LEFT_UP, self.onSquareClick, self.ca)
        self.panel.Bind(wx.EVT_BUTTON, self.onPauseClick, pauseButton)
        self.panel.Bind(wx.EVT_BUTTON, self.onResetClick, resetButton)
        
        self.panel.SetSizer(vbox)

    

    def onSquareClick(self, e):
        self.sb.SetStatusText('Left button clicked at' + str(e.GetLogicalPosition(wx.ClientDC(self.panel))))

    def onPauseClick(self, e):
        self.sb.SetStatusText('Pause Button Clicked')

    def onResetClick(self, e):
        self.sb.SetStatusText('Ready')

    def onChangeself.boxSize(self, e):
        try:
            self.ca.SetBoxSize(int(self.tcself.boxSize.Value))
        except ValueError:
            pass

class ClientArea(wx.Panel):
    def __init__(self,*args,**kwargs):
        wx.Panel.__init__(self,*args,**kwargs)
        self.panel = wx.Panel(self)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_UP, self.onSquareClick)
        self.boxSize = 20
        self.initialized = False
        
        
    def initData(self, dc, preserve=False):
        self.currentGrid = [[]]
        self.nextGrid = [[]]
        clientSize = dc.GetSize()
        rows = int(clientSize.y / self.boxSize)
        cols = int(clientSize.x / self.boxSize)
        for y in range(0, rows - 1):
            self.currentGrid.insert(y, [])
            self.nextGrid.insert(y, [])
            for x in range(0, cols - 1):
                self.currentGrid[y].insert(x,False)
                self.nextGrid[y].insert(x, False)
        print('Data table is ' + str(len(self.currentGrid)) + ' rows, and ' + str(len(self.currentGrid[0])) + ' columns.')
        #todo: add support for preserve

    def onSquareClick(self, e):
        dc = wx.ClientDC(self.panel)
        pos = e.GetLogicalPosition(dc)
        print('Left button clicked at' + str(pos))
        # find root position of box contining click
        rootPos = wx.Point(0, 0)
        x = 0
        y = 0

        for i in range(0, len(self.currentGrid[0])):
            if pos.x >= (i * self.boxSize) and pos.x <= ((i+1) * self.boxSize):
                rootPos.x = i * self.boxSize
                x = i
        for i in range(0, len(self.currentGrid)):
            if pos.y >= (i * self.boxSize) and pos.y <= ((i+1) * self.boxSize):
                rootPos.y = i * self.boxSize
                y = i

        # if the current array contains a box already
        if self.currentGrid[x][y] == True:
            # clear it
            self.currentGrid[x][y] = False    
        # else
            # set that array element to true
            self.currentGrid[x][y] = True

        print('Array indexes are (' + str(x) + ', ' + str(y) + ')')
        print('Root position is ' + str(rootPos))

    def onPaint(self, e):

        dc = wx.PaintDC(self)
        self.DrawGrid(dc)
        if not self.initialized:
            self.initData(dc)

    def DrawGrid(self, dc):
        # determine dimentions of client area
        clientSize = dc.GetSize()

        # draw grid of squares maintaining aspect ratio
        width = self.boxSize
        height = self.boxSize
        
        dc.DrawLine(0, 0, clientSize.x, 0)

        for x in range(1, int(clientSize.x / self.boxSize) + 1):
            # draw vertical lines
            dc.DrawLine(width * x, 0, width * x, clientSize.y + 1)

        for y in range (1, int(clientSize.y / self.boxSize) + 1):
            # draw horizontal lines
            dc.DrawLine(0, height * y, clientSize.x, height * y)

    def DrawSquares(self, dc):
        # walk the array drawing a filled square at every "true" position
        # todo implement this!

    def SetBoxSize(self, size):
        self.boxSize = size
        self.Refresh()
        
def main():

    app = wx.App()
    ex = MainFrame(None, title='Game of Life')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()