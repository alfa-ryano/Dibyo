"""
This is version 9 for imprecise preference
Modified on 22/06/17
This version imports files from directory Imprecise 9
"""

import wx
import os
import csv

from SubjectNumberPage import SubjectNumberPage
from WelcomePage import WelcomePage
from PreferencePage import PreferencePage
from InstructionPage import InstructionPage
from EndPage import EndPage
from MyUtil import isfloat


class Application():
    def __init__(self, mainProcess):
        self.mainProcess = mainProcess
        self.pageList = []
        self.currentPage = 0
        self.subjectNumber = ""

        # These are the screens of the experiment. It is ordered as explained in its lists
        self.pageList.append(SubjectNumberPage(None, self))  # write down the subject number
        self.pageList.append(WelcomePage(None, self))  # nothing fancy. Just click continue
        self.pageList.append(
            InstructionPage(None, self, "instruction/Instruction1.xml", InstructionPage.WITHOUT_PREV_BUTTON))
        self.pageList.append(PreferencePage(None, self, "instruction/ExampleInstruction.xml",
                                            PreferencePage.TYPE_EXAMPLE, 0, 30, 0.65, 15, 0.35, -1, -1))
        self.pageList.append(InstructionPage(None, self, "instruction/Instruction2a.xml"))
        self.pageList.append(PreferencePage(None, self, "instruction/ExampleInstruction.xml",
                                            PreferencePage.TYPE_DEMO, 0, 30, 0.65, 15, 0.35, -1, -1))
        self.pageList.append(InstructionPage(None, self, "instruction/Instruction2b.xml"))
        self.pageList.append(PreferencePage(None, self, "instruction/ExampleInstruction.xml",
                                            PreferencePage.TYPE_DEMO2, 0, 30, 0.65, 15, 0.35, -1, -1))
        self.pageList.append(InstructionPage(None, self, "instruction/Instruction3.xml", InstructionPage.PAYMENT))
        # These are practice session 1 and 2
        self.pageList.append(PreferencePage(None, self, "instruction/Practice1.xml",
                                            PreferencePage.TYPE_PRACTICE, 0, 30, 0.65, 15, 0.35, -1, -1))
        self.pageList.append(PreferencePage(None, self, "instruction/Practice2.xml",
                                            PreferencePage.TYPE_PRACTICE, 0, 35, 0.5, 20, 0.5, -1, -1))
        self.pageList.append(InstructionPage(None, self, "instruction/Instruction4.xml", InstructionPage.LAST))

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

            pn = float(row[0]) if isfloat(row[0]) else -1
            v1 = float(row[1]) if isfloat(row[1]) else -1
            p1 = float(row[2]) if isfloat(row[2]) else -1
            v2 = float(row[3]) if isfloat(row[3]) else -1
            p2 = float(row[4]) if isfloat(row[4]) else -1
            v3 = float(row[5]) if isfloat(row[5]) else -1
            p3 = float(row[6]) if isfloat(row[6]) else -1

            instructionFile = "instruction/PreferenceSheetInstruction.xml"
            if (p1 == -1 or p1 == 0) and (p2 == -1 or p2 == 0) and (p3 == -1 or p3 == 0):
                instructionFile = "instruction/PreferenceSheetInstruction-Empty.xml"
            elif (p1 == -1 or p1 == 0) and (p2 == -1 or p2 == 0) and (p3 != -1 and p3 != 0):
                instructionFile = "instruction/PreferenceSheetInstruction-One.xml"
            elif (p1 == -1 or p1 == 0) and (p2 != -1 and p2 != 0) and (p3 == -1 or p3 == 0):
                instructionFile = "instruction/PreferenceSheetInstruction-One.xml"
            elif (p1 == -1 or p1 == 0) and (p2 != -1 and p2 != 0) and (p3 != -1 and p3 != 0):
                instructionFile = "instruction/PreferenceSheetInstruction-Two.xml"
            elif (p1 != -1 and p1 != 0) and (p2 == -1 or p2 == 0) and (p3 == -1 or p3 == 0):
                instructionFile = "instruction/PreferenceSheetInstruction-One.xml"
            elif (p1 != -1 and p1 != 0) and (p2 == -1 or p2 == 0) and (p3 != -1 and p3 != 0):
                instructionFile = "instruction/PreferenceSheetInstruction-Two.xml"
            elif (p1 != -1 and p1 != 0) and (p2 != -1 and p2 != 0) and (p3 == -1 or p3 == 0):
                instructionFile = "instruction/PreferenceSheetInstruction-Two.xml"
            elif (p1 != -1 and p1 != 0) and (p2 != -1 and p2 != 0) and (p3 != -1 and p3 != 0):
                instructionFile = "instruction/PreferenceSheetInstruction-Three.xml"

            self.pageList.append(PreferencePage(None, self, instructionFile,
                                                type, pn, v1, p1, v2, p2, v3, p3))
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
        # self.mainProcess.Exit()
        for page in self.pageList:
            page.Hide()
            page.Close(True)


app = wx.App(False)
Application(app).Start()
app.MainLoop()
