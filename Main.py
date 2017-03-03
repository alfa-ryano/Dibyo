import wx

from SubjectNumberPage import SubjectNumberPage
from WelcomePage import WelcomePage
from PreferencePage import PreferencePage
from InstructionPage import InstructionPage
from EndPage import EndPage


class Application():
    def __init__(self):
        self.pageList = []
        self.currentPage = 0
        self.subjectNumber = ""
        self.pageList.append(SubjectNumberPage(None, self))
        self.pageList.append(WelcomePage(None, self))
        self.pageList.append(InstructionPage(None, self))
        self.pageList.append(PreferencePage(None, self))
        self.pageList.append(EndPage(None, self))

    def Start(self):
        self.pageList[self.currentPage].Show()

    def NextPage(self):
        self.currentPage += 1
        if self.currentPage >= len(self.pageList):
            self.currentPage = len(self.pageList) - 1
        else:
            self.pageList[self.currentPage].Show()
            self.pageList[self.currentPage - 1].Hide()


    def PrevPage(self):
        self.currentPage -= 1
        if self.currentPage < 0:
            self.currentPage = 0
        else:
            self.pageList[self.currentPage].Show()
            self.pageList[self.currentPage + 1].Hide()

    def Shutdown(self):
        for page in self.pageList:
            page.Hide()
            page.Close()


app = wx.App()
Application().Start()
app.MainLoop()
