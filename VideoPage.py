import cv2
import wx
import wx.richtext as rt
import os


class VideoPage(wx.Frame):
    WITHOUT_PREV_BUTTON = 0
    WITH_PREV_BUTTON = 1
    PAYMENT = 2
    LAST = 3

    def __init__(self, parent, application, instructionFile, type = WITH_PREV_BUTTON):
        super(VideoPage, self).__init__(parent, title="Instruction", size=(640, 480),
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
        font = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD)
        labelTitle = wx.StaticText(panel, label="INSTRUCTION")
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

        boxVideo = wx.BoxSizer(wx.VERTICAL)
        buttonVideo = wx.Button(panel, label = "PLAY VIDEO")
        buttonVideo.SetFont(font)
        buttonVideo.Bind(wx.EVT_BUTTON, self.OnButtonVideoClick)
        boxVideo.Add(buttonVideo, flag = wx.ALIGN_RIGHT)

        boxPrev = wx.BoxSizer(wx.VERTICAL)
        buttonPrev = wx.Button(panel, label = "PREV")
        buttonPrev.SetFont(font)
        buttonPrev.Bind(wx.EVT_BUTTON, self.OnButtonPrevClick)
        boxPrev.Add(buttonPrev, flag=wx.ALIGN_LEFT)
        
        boxConfirm = wx.BoxSized(wx.VERTICAL)
        buttonConfirm = wx.BUtton(panel, label = "GO TO PROBLEMS")
        buttonConfirm.SetFont(font)
        buttonPrev.Bind(wx.EVT_BUTTON, self.OnButtonConfirmClick)
        boxConfirm.Add(buttonVideo, flag = wx.ALIGN_CENTRE)        

        hbox3.Add(boxPrev, flag = wx.ALIGN_LEFT, proportion = 1)
        hbox3.Add(boxVideo, flag = wx.ALIGN_RIGHT, proportion = 1)
        hbox3.Add(boxConfirm, flag = wx.ALIGN_CENTER, proportion = 1)
        vbox.Add(hbox3, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border = 8)

        panel.SetSizer(vbox)

        if self.type == self.WITHOUT_PREV_BUTTON:
            buttonPrev.Hide()
            
        elif self.type == self.PAYMENT:
            buttonVideo.SetLabel("GO TO PRACTICE SESSION")
            
        elif self.type == self.LAST:
            buttonVideo.SetLabel("GO TO THE EXPERIMENT")            
            buttonPrev.Hide()

    def OnButtonPrevClick(self, event):
        self.application.PrevPage()

    def OnButtonVideoClick(self, event):
        cap = cv2.VideoCapture('images/sample.flv')
        while True:
            ret, frame = cap.read()
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        cap.release()
        cv2.destroyAllWindows()

    def OnButtonConfirmClick(self, event):
        self.application.NextPage()


