import wx

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)
        self.panel = wx.Panel(self)
        self.panel.BackgroundColour = wx.RED
        self.panel.Bind(wx.EVT_LEFT_UP, self.onClick)

    def onClick(self, event):
        if self.panel.BackgroundColour == wx.RED:
            self.panel.BackgroundColour = wx.GREEN
        else:
            self.panel.BackgroundColour = wx.RED

            
def main():

    app = wx.App()
    ex = MyFrame()
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()