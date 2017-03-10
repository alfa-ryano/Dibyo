import wx
import os
import csv

from SubjectNumberPage import SubjectNumberPage
from WelcomePage import WelcomePage
from PreferencePage import PreferencePage
from InstructionPage import InstructionPage
from EndPage import EndPage


class Application():
    def __init__(self, mainProcess):
        self.mainProcess = mainProcess
        self.pageList = []
        self.currentPage = 0
        self.subjectNumber = ""
        self.pageList.append(SubjectNumberPage(None, self))
        self.pageList.append(WelcomePage(None, self))
        self.pageList.append(InstructionPage(None, self, "instruction/I00.xml", InstructionPage.WITHOUT_PREV_BUTTON))
        self.pageList.append(PreferencePage(None, self, "instruction/PreferenceSheetInstruction.xml",
                                            PreferencePage.TYPE_EXAMPLE, 30, 0.65, 15, 0.35))
        self.pageList.append(InstructionPage(None, self, "instruction/I01.xml"))
        self.pageList.append(PreferencePage(None, self, "instruction/PreferenceSheetInstruction.xml",
                                            PreferencePage.TYPE_DEMO, 30, 0.65, 15, 0.35))
        self.pageList.append(InstructionPage(None, self, "instruction/I02.xml"))
        self.pageList.append(InstructionPage(None, self, "instruction/I03.xml"))


        csvPath = os.path.abspath("sheets/Lottery.csv")
        csvfile = open(csvPath, 'rb')
        csvReader = csv.reader(csvfile, delimiter=',')
        rows = list(csvReader)
        i = 0
        while i < len(rows):
            row = rows[i]
            type = PreferencePage.TYPE_REAL
            # if it's the last form then the type of Pref. Sheet should be TYPE_REAL_FINAL
            if i == len(rows) - 1:
                type = PreferencePage.TYPE_REAL_FINAL
            print row

            v1, p1, v2, p2 = float(row[0]), float(row[1]), float(row[2]), float(row[3])
            self.pageList.append(PreferencePage(None, self, "instruction/PreferenceSheetInstruction.xml",
                                                type , v1, p1, v2, p2))
            i += 1
        csvfile.close()
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
        self.mainProcess.Destroy()

app = wx.App()
Application(app).Start()
app.MainLoop()
