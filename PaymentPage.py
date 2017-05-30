import wx
import wx.richtext as rt
import os
from PreferencePage5columns import PreferencePage

class PaymentPage(wx.Frame):
    WITHOUT_PREV_BUTTON = 0
    WITH_PREV_BUTTON = 1

    def __init__(self, parent, application, instructionFile, type=WITH_PREV_BUTTON):
        super(PaymentPage, self).__init__(parent, title="Payment", size=(640, 480),
                                              style=wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX))
        self.application = application
        self.type = type
        self.instructionFile = instructionFile

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
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD)
        labelTitle = wx.StaticText(panel, label="YOUR PAYMENT")
        labelTitle.SetFont(font)
        hbox1.Add(labelTitle, flag=wx.ALIGN_CENTRE, proportion=1)
        vbox.Add(hbox1, flag=wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=8)
        
        hbox2 = wx.BoxSizer(wx.VERTICAL)
        fontRichText = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())  # add suppport to read xml for richtext
        wx.FileSystem.AddHandler(wx.MemoryFSHandler())  # add suppport to read xml for richtext
        richText = rt.RichTextCtrl(panel, style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER);
        richText.SetFont(fontRichText)
        path = os.path.abspath(self.instructionFile)
        richText.LoadFile(path, rt.RICHTEXT_TYPE_XML)
        richText.SetEditable(False)
        # richText.SetBackgroundColour(wx.Colour(240, 240, 240))
        hbox2.Add(richText, flag=wx.ALIGN_CENTER | wx.EXPAND, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM,
                 border=10, proportion=1)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        boxNext = wx.BoxSizer(wx.VERTICAL)
        buttonNext = wx.Button(panel, label="GO TO THE EXPERIMENT")
        buttonNext.SetFont(font)
        buttonNext.Bind(wx.EVT_BUTTON, self.OnButtonNextClick)
        boxNext.Add(buttonNext, flag=wx.ALIGN_RIGHT)

        boxPrev = wx.BoxSizer(wx.VERTICAL)
        buttonPrev = wx.Button(panel, label="PREV")
        buttonPrev.SetFont(font)
        buttonPrev.Bind(wx.EVT_BUTTON, self.OnButtonPrevClick)
        boxPrev.Add(buttonPrev, flag=wx.ALIGN_LEFT)

        hbox3.Add(boxPrev, flag=wx.ALIGN_LEFT, proportion=1)
        hbox3.Add(boxNext, flag=wx.ALIGN_RIGHT, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=8)

        panel.SetSizer(vbox)
        
    def OnButtonPrevClick(self, event):
        self.application.PrevPage()

    def OnButtonNextClick(self, event):
        self.application.NextPage()
        