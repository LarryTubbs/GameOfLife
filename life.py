#!/usr/bin/env python

from os import curdir
from sys import flags
from copy import deepcopy
import time, threading

import wx
from wx.core import BoxSizer, CONTROL_CURRENT, FileDialogNameStr, PropagateOnce, RadioBoxNameStr, Size


class MainFrame(wx.Frame):

    ID_TIMER = 1

    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(600,600))

        self.InitUI()
        self.Centre()

    def InitUI(self):

        self.panel = wx.Panel(self)

        self.timer = wx.Timer(self, MainFrame.ID_TIMER)

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)

        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        # square size
        st1 = wx.StaticText(self.panel, label='Square Size')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        self.tcBoxSize = wx.TextCtrl(self.panel)
        self.tcBoxSize.Value = "20"
        hbox1.Add(self.tcBoxSize, flag=wx.RIGHT, proportion=0, border=8)

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

        self.generation = 0
        self.speed = 1000

        self.panel.Bind(wx.EVT_TEXT, self.onChangeBoxSize, self.tcBoxSize)
        self.panel.Bind(wx.EVT_LEFT_UP, self.onSquareClick, self.ca)
        self.panel.Bind(wx.EVT_BUTTON, self.onStartClick, startButton)
        self.panel.Bind(wx.EVT_BUTTON, self.onPauseClick, pauseButton)
        self.panel.Bind(wx.EVT_BUTTON, self.onResetClick, resetButton)
        self.panel.Bind(wx.EVT_BUTTON, self.onStepClick, stepButton)
        self.Bind(wx.EVT_TIMER, self.onTimer, id=MainFrame.ID_TIMER)

        self.panel.SetSizer(vbox)

    def onTimer(self, e):
        self.advanceGeneration()

    def onStartClick(self, e):
        self.timer.Start(self.speed)

    def advanceGeneration(self):
        self.ca.GenerateLife()
        self.generation += 1
        self.sb.SetStatusText(f"Generation {self.generation}")

    def onStepClick(self, e):
        self.advanceGeneration()

    def onSquareClick(self, e):
        self.sb.SetStatusText('Left button clicked at' + str(e.GetLogicalPosition(wx.ClientDC(self.panel))))

    def onPauseClick(self, e):
        self.timer.Stop()

    def onResetClick(self, e):
        self.timer.Stop()
        self.ca.Reset()
        self.generation = 0
        self.sb.SetStatusText('Ready')

    def onChangeBoxSize(self, e):
        try:
            self.ca.SetBoxSize(int(self.tcBoxSize.Value))
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

    def onSize(self):
        pass       
        
    def initData(self, preserve=False):
        if preserve == False:
            self.currentGrid = [[]]
            self.nextGrid = [[]]
        else:
            return    
        dc = wx.ScreenDC()
        screenSize = dc.GetSize()
        rows = int(screenSize.y / self.boxSize)
        cols = int(screenSize.x / self.boxSize)
        for y in range(0, rows):
            self.currentGrid.insert(y, [])
            self.nextGrid.insert(y, [])
            for x in range(0, cols):
                self.currentGrid[y].insert(x,False)
                self.nextGrid[y].insert(x, False)
        print('Data table is ' + str(len(self.currentGrid)) + ' rows, and ' + str(len(self.currentGrid[0])) + ' columns.')
        

    def onSquareClick(self, e):
        dc = wx.ClientDC(self.panel)
        pos = e.GetLogicalPosition(dc)
        print('Left button clicked at' + str(pos))
        x = 0
        y = 0

        x = int(pos.x / self.boxSize)
        y = int(pos.y / self.boxSize)
        
        print('x = ' + str(x) + ', y = ' + str(y))

        if self.currentGrid[y][x] == True:
            self.currentGrid[y][x] = False    
        else:
            self.currentGrid[y][x] = True

        print('Array indexes are (' + str(x) + ', ' + str(y) + ')')
        self.Refresh()
        
    def onPaint(self, e):

        dc = wx.PaintDC(self)
        self.DrawGrid(dc)
        if not self.initialized:
            self.initData()
            self.initialized = True
        else:
            self.initData(preserve=True)
        self.DrawLife(dc)

    def Reset(self):
        self.initData()
        self.Refresh()

    def DrawLife(self, dc):
        for y in range(0, len(self.currentGrid)):
            for x in range(0, len(self.currentGrid[y])):
                if self.currentGrid[y][x] == True:
                    # draw rectange in this position
                    dc.SetBrush(wx.Brush('#ffffff'))
                    dc.DrawRectangle(x * self.boxSize, y * self.boxSize, self.boxSize, self.boxSize)

    def GenerateLife(self):
        for y in range(0, len(self.currentGrid)):
            for x in range(0, len(self.currentGrid[y])):
                self.nextGrid[y][x] = False
                n = self.CountNeighbors(y, x)
                if self.currentGrid[y][x] == False:
                    if n == 3:
                        self.nextGrid[y][x] = True
                    else:
                        self.nextGrid[y][x] = False
                else:
                    if n < 2 or n > 3:
                        self.nextGrid[y][x] = False
                    else:
                        self.nextGrid[y][x] = True
        self.currentGrid = deepcopy(self.nextGrid)
        self.Refresh()


    def CountNeighbors(self, y, x):
        c = 0
        try:
            #upper left
            if self.currentGrid[y-1][x-1] == True:
                c += 1
        except IndexError:
            pass

        try:
            #upper middle
            if self.currentGrid[y-1][x] == True:
                c += 1  
        except IndexError:
            pass

        try:
            #upper right
            if self.currentGrid[y-1][x+1] == True:
                c += 1 
        except IndexError:
            pass

        try:   
            #left
            if self.currentGrid[y][x-1] == True:
                c += 1
        except IndexError:
            pass

        try:    
            #right
            if self.currentGrid[y][x+1] == True:
                c += 1 
        except IndexError:
            pass

        try:   
            #lower left
            if self.currentGrid[y+1][x-1] == True:
                c += 1
        except IndexError:
            pass

        try:    
            #lower middle
            if self.currentGrid[y+1][x] == True:
                c += 1
        except IndexError:
            pass

        try:    
            #lower right
            if self.currentGrid[y+1][x+1] == True:
                c += 1
        except IndexError:
            pass

        return c

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
        print('placeholder')

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