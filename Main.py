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
        self.pageList.append(InstructionPage(None, self, "instruction/I00.xml", InstructionPage.WITHOUT_PREV_BUTTON))
        self.pageList.append(PreferencePage(None, self, "instruction/PSI-Example.xml", "sheets/PS-Example.csv",
                                            PreferencePage.TYPE_EXAMPLE))
        self.pageList.append(InstructionPage(None, self, "instruction/I01.xml"))
        self.pageList.append(PreferencePage(None, self, "instruction/PSI-Demo.xml", "sheets/PS-Demo.csv",
                                            PreferencePage.TYPE_DEMO))
        self.pageList.append(InstructionPage(None, self, "instruction/I02.xml"))
        self.pageList.append(InstructionPage(None, self, "instruction/I03.xml"))
        self.pageList.append(PreferencePage(None, self, "instruction/PSI-01.xml", "sheets/PS-01.csv",
                                            PreferencePage.TYPE_REAL))
        self.pageList.append(PreferencePage(None, self, "instruction/PSI-02.xml", "sheets/PS-02.csv",
                                            PreferencePage.TYPE_REAL))
        self.pageList.append(PreferencePage(None, self, "instruction/PSI-03.xml", "sheets/PS-03.csv",
                                            PreferencePage.TYPE_REAL_FINAL))
        self.pageList.append(EndPage(None, self, "instruction/END.xml"))

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
