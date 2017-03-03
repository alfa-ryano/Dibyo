import wx
from InstructionPage import InstructionPage

class WelcomePage(wx.Frame):
    def __init__(self, parent, application):
        super(WelcomePage, self).__init__(parent, title="Welcome To This Experiment", size=(640, 480), style=wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX))
        self.application = application#
        self.Hide()
        self.Center()
        self.initUI()
        #self.Maximize(True)
        self.ShowFullScreen(True)
        self.Hide()

    def initUI(self):
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        fontWelcome = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD)

        labelWelcome = wx.StaticText(panel, label="Welcome to this experiment")
        labelWelcome.SetFont(fontWelcome)

        logo = wx.StaticBitmap(panel, -1, wx.Bitmap("images/exec.png", wx.BITMAP_TYPE_ANY))

        fontContinue = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD)

        labelContinue = wx.StaticText(panel, label="Click 'CONTINUE' to go to the next page")
        labelContinue.SetFont(fontContinue)

        vbox1a = wx.BoxSizer(wx.VERTICAL)
        vbox1a.Add(labelWelcome, flag=wx.ALIGN_CENTER)
        vbox1a.Add(logo, flag=wx.ALIGN_CENTER | wx.TOP, border=50)
        vbox1a.Add(labelContinue, flag=wx.ALIGN_CENTER | wx.TOP, border=100)
        hbox1.Add(vbox1a, flag=wx.ALIGN_CENTER_VERTICAL, proportion=1)

        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM,
                 border=10, proportion=1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        fontButton = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD)
        button = wx.Button(panel, label="CONTINUE")
        button.SetFont(fontButton)
        button.Bind(wx.EVT_BUTTON, self.OnButtonContinueClick)
        hbox2.Add(button, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=8)

        panel.SetSizer(vbox)

    def OnButtonContinueClick(self, event):
        self.application.NextPage()
