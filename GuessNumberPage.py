import wx
from random import randrange


class GuessNumberPage(wx.Frame):
    def __init__(self, parent, application):
        super(GuessNumberPage, self) \
            .__init__(parent, title="Guess Number", size=(640, 480), style=wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX))

        self.a = randrange(10)
        self.b = randrange(10)
        self.c = randrange(10)

        self.question = str(self.a) + " + " + str(self.b) + " x " + str(self.c) + " = ?"
        self.answer = self.a + self.b * self.c
        self.guess = None

        self.application = application
        self.Hide()
        self.Center()
        self.initUI()
        # self.Maximize(True)
        self.ShowFullScreen(True)
        self.Hide()

    def initUI(self):
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        font = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD)

        label = wx.StaticText(panel, label=self.question)
        label.SetFont(font)

        self.guessText = wx.TextCtrl(panel, size=(400, -1), style=wx.TE_CENTRE)
        self.guessText.SetFont(font)

        vbox1a = wx.BoxSizer(wx.VERTICAL)
        vbox1a.Add(label, flag=wx.ALIGN_CENTER)
        vbox1a.Add(self.guessText, flag=wx.ALIGN_CENTER | wx.TOP, border=10)
        hbox1.Add(vbox1a, flag=wx.ALIGN_CENTER_VERTICAL, proportion=1)

        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM,
                 border=10, proportion=1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        button = wx.Button(panel, label="SUBMIT")
        button.SetFont(font)
        button.Bind(wx.EVT_BUTTON, self.OnButtonSubmitClick)
        hbox2.Add(button, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=8)

        panel.SetSizer(vbox)

    def OnButtonSubmitClick(self, event):
        guessText = self.guessText.GetValue().strip()
        isNumber = self.is_number(guessText)
        if isNumber:
            self.guess = int(guessText)
        else:
            self.guess = -1
            wx.MessageBox("Your answer is not correct!", "Warning",
                          wx.OK | wx.ICON_WARNING)
            return

        if self.guess != self.answer:
            wx.MessageBox("Your answer is not correct!", "Warning",
                          wx.OK | wx.ICON_WARNING)
            return

        self.application.NextPage()

    def is_number(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False
