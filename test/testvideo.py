import wx
from wx.media import MediaCtrl
import os


class StaticText(wx.StaticText):
    """
    A StaticText that only updates the label if it has changed, to
    help reduce potential flicker since these controls would be
    updated very frequently otherwise.
    """

    def SetLabel(self, label):
        if label <> self.GetLabel():
            wx.StaticText.SetLabel(self, label)


class MainForm(wx.Frame):
    def __init__(self):
        super(MainForm, self). \
            __init__(None, title="Subject Number", size=(640, 480), style=wx.DEFAULT_FRAME_STYLE)
        self.Center()
        self.initUI()

    def initUI(self):
        panel = wx.Panel(self)

        # Create some controls
        try:
            self.mc = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)

        except NotImplementedError:
            self.Destroy()
            raise

        self.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded)

        btn1 = wx.Button(self, -1, "Load File")
        self.Bind(wx.EVT_BUTTON, self.OnLoadFile, btn1)

        btn2 = wx.Button(self, -1, "Play")
        self.Bind(wx.EVT_BUTTON, self.OnPlay, btn2)
        self.playBtn = btn2

        btn3 = wx.Button(self, -1, "Pause")
        self.Bind(wx.EVT_BUTTON, self.OnPause, btn3)

        btn4 = wx.Button(self, -1, "Stop")
        self.Bind(wx.EVT_BUTTON, self.OnStop, btn4)

        slider = wx.Slider(self, -1, 0, 0, 10)
        self.slider = slider
        slider.SetMinSize((150, -1))
        self.Bind(wx.EVT_SLIDER, self.OnSeek, slider)

        self.st_size = StaticText(self, -1, size=(100, -1))
        self.st_len = StaticText(self, -1, size=(100, -1))
        self.st_pos = StaticText(self, -1, size=(100, -1))

        # setup the layout
        sizer = wx.GridBagSizer(5, 5)
        sizer.Add(self.mc, (1, 1), span=(5, 1))  # , flag=wx.EXPAND)
        sizer.Add(btn1, (1, 3))
        sizer.Add(btn2, (2, 3))
        sizer.Add(btn3, (3, 3))
        sizer.Add(btn4, (4, 3))
        sizer.Add(slider, (6, 1), flag=wx.EXPAND)
        sizer.Add(self.st_size, (1, 5))
        sizer.Add(self.st_len, (2, 5))
        sizer.Add(self.st_pos, (3, 5))
        self.SetSizer(sizer)

        wx.CallAfter(self.DoLoadFile, os.path.abspath("D:\degea.mp4"))

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(100)

    def OnLoadFile(self, evt):

        dlg = wx.FileDialog(self, message="Choose a media file",
                            defaultDir=os.getcwd(), defaultFile="",
                            style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.DoLoadFile(path)

        dlg.Destroy()

    def DoLoadFile(self, path):

        # self.playBtn.Disable()

        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mc.SetInitialSize()
            self.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())

    def OnMediaLoaded(self, evt):

        self.playBtn.Enable()

    def OnPlay(self, evt):

        if not self.mc.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mc.SetInitialSize()
            self.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())

    def OnPause(self, evt):

        self.mc.Pause()

    def OnStop(self, evt):

        self.mc.Stop()

    def OnSeek(self, evt):

        offset = self.slider.GetValue()
        self.mc.Seek(offset)

    def OnTimer(self, evt):

        offset = self.mc.Tell()
        self.slider.SetValue(offset)
        self.st_size.SetLabel('size: %s' % self.mc.GetBestSize())
        self.st_len.SetLabel('length: %d seconds' % (self.mc.Length() / 1000))
        self.st_pos.SetLabel('position: %d' % offset)

    def ShutdownDemo(self):

        self.timer.Stop()
        del self.timer


app = wx.App(False)
mainForm = MainForm()
mainForm.Show()
app.MainLoop()
