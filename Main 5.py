"""
This is version 5 for imprecise preference
Modified on 13/03/17
This version imports files from directory Imprecise 5
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
        
        # You write your number down on the box
        self.pageList.append(SubjectNumberPage(None, self))     
        # Nothing fancy, but you can click 'CONTINUE' as it is opened by the server
        self.pageList.append(WelcomePage(None, self))
        # The first page of instruction. This page is with next button but without previous button. It reads particular instruction file
        self.pageList.append(InstructionPage(None, self, "instruction/Instruction1.xml", InstructionPage.WITHOUT_PREV_BUTTON))
        # Page 2 of instruction. It shows you the example of Preference Sheet. It comes with next and previous button.
        # The confirm button is shown but inactive. It reads particular instruction file and append PreferencePage.Type Example below instruction.
        self.pageList.append(PreferencePage(None, self, "instruction/ExampleInstruction.xml",
                                            PreferencePage.TYPE_EXAMPLE, 0, 30, 0.65, 15, 0.35))
        # Page 3 of instruction, comes with next and previous buttons. This reads particular instruction file
        self.pageList.append(InstructionPage(None, self, "instruction/Instruction2.xml"))
        # Page 4 of instruction. Instruction on the top, followed by the filled preference page.
        # It comes with next and previous buttons. The confirm button is inactive.
        self.pageList.append(PreferencePage(None, self, "instruction/ExampleInstruction.xml",
                                            PreferencePage.TYPE_DEMO, 0, 30, 0.65, 15, 0.35))
        # Page 5 of instruction, showing the payment scheme. Next page is practice session
        self.pageList.append(InstructionPage(None, self, "instruction/Instruction3.xml", InstructionPage.PAYMENT))
        # This is practice session 1
        self.pageList.append(PreferencePage(None, self, "instruction/Practice1.xml",
                                            PreferencePage.TYPE_PRACTICE, 0, 30, 0.65, 15, 0.35))
        # This is practice session 2
        self.pageList.append(PreferencePage(None, self, "instruction/Practice2.xml",
                                            PreferencePage.TYPE_PRACTICE, 0, 35, 0.5, 20, 0.5))
        # This is the last page of instruction before going to the real experiment
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
            if v3 != -1 and p3 != -1:
                instructionFile = "instruction/PreferenceSheetInstruction-v3p3.xml"

            self.pageList.append(PreferencePage(None, self, instructionFile,
                                                type , pn, v1, p1, v2, p2, v3, p3))
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
