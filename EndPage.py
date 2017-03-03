import wx
import wx.richtext as rt
import os

class EndPage(wx.Frame):
    def __init__(self, parent, application, instructionFile):
        super(EndPage, self) \
            .__init__(parent, title="Instruction", size=(640, 480), style=wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX))
        self.application = application
        self.instructionFile = instructionFile

        self.Hide()
        self.Center()
        self.initUI()
        #self.Maximize(True)
        self.ShowFullScreen(True)
        self.Hide()

    def initUI(self):
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox2 = wx.BoxSizer(wx.VERTICAL)
        fontRichText = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler()) #add suppport to read xml for richtext
        wx.FileSystem.AddHandler(wx.MemoryFSHandler()) #add suppport to read xml for richtext
        richText = rt.RichTextCtrl(panel, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER);
        richText.SetFont(fontRichText)
        path = os.path.abspath(self.instructionFile)
        richText.LoadFile(path, rt.RICHTEXT_TYPE_XML)
        richText.SetEditable(False)
        richText.SetBackgroundColour(wx.Colour(240, 240, 240))
        hbox2.Add(richText, flag=wx.ALIGN_CENTER | wx.EXPAND, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM,
                 border=10, proportion=1)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        buttonNext = wx.Button(panel, label="CLOSE THE SCREEN")
        font = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD)
        buttonNext.SetFont(font)
        buttonNext.Bind(wx.EVT_BUTTON, self.OnButtonCloseClick)
        buttonNext.SetFocus()
        hbox3.Add(buttonNext, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=8)

        panel.SetSizer(vbox)

    def OnButtonCloseClick(self, event):
        self.application.Shutdown()

