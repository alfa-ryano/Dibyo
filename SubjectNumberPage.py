import wx
import ConfigParser
import requests
from WelcomePage import WelcomePage

class SubjectNumberPage(wx.Frame):
    def __init__(self, parent, application):
        super(SubjectNumberPage, self) \
            .__init__(parent, title="Subject Number", size=(640, 480), style=wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX))
        self.application = application
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

        font = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD)

        label = wx.StaticText(panel, label="SUBJECT NUMBER")
        label.SetFont(font)

        self.subjectNumberText = wx.TextCtrl(panel, size=(400, -1), style=wx.TE_CENTRE)
        self.subjectNumberText.SetFont(font)
        self.subjectNumberText.Bind(wx.EVT_TEXT, self.OnTextChanged)

        vbox1a = wx.BoxSizer(wx.VERTICAL)
        vbox1a.Add(label, flag=wx.ALIGN_CENTER)
        vbox1a.Add(self.subjectNumberText, flag=wx.ALIGN_CENTER | wx.TOP, border=10)
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

    def OnTextChanged(self, event):
        subjectNumber = self.subjectNumberText.GetValue()
        self.application.subjectNumber = subjectNumber.strip()

    def OnButtonSubmitClick(self, event):
        subjectNumber = self.application.subjectNumber
        chars = set('<>:"/\     |?*_')
        if len(subjectNumber) == 0:
            wx.MessageBox('Subject number cannot be empty!', 'Warning',
                          wx.OK | wx.ICON_WARNING)
            return

        if any((c in chars) for c in subjectNumber):
            wx.MessageBox('Subject number cannot contain these characters <>:"/\    |?*_', 'Warning',
                          wx.OK | wx.ICON_WARNING)
            return

        try:
            config = ConfigParser.ConfigParser()
            config.read("client.ini")
            server = config.get("Config", "Server")
            server += "/check"
            response = requests.get(server)
            if response.text.strip() == "1":
                wx.MessageBox('Server is still locked. Ask the experimenter to open it!', 'Warning',
                              wx.OK | wx.ICON_WARNING)
                return
        except:
            wx.MessageBox('Cannot connect to server. Please check your connection!', 'Warning',
                      wx.OK | wx.ICON_WARNING)
            return

        self.application.NextPage()