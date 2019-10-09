"""
This is version 9 for imprecise preference
Modified on 22/06/17
This version imports files from directory Imprecise 9
"""

import wx
import os
import csv
import threading

from SubjectNumberPage import SubjectNumberPage
from GuessNumberPage import GuessNumberPage
from WelcomePage import WelcomePage
from PreferencePage import PreferencePage
from InstructionPage import InstructionPage
from EndPage import EndPage
from MyUtil import isfloat
from Simulation import Simulation


class Application():
    def __init__(self, mainProcess):
        self.mainProcess = mainProcess
        self.pageList = []
        self.currentPage = 0
        self.subjectNumber = ""

        # # These are the screens of the experiment. It is ordered as explained in its lists
        # self.pageList.append(GuessNumberPage(None, self))  # a guess number quiz
        self.pageList.append(SubjectNumberPage(None, self))  # write down the subject number
        # self.pageList.append(WelcomePage(None, self))  # nothing fancy. Just click continue
        # self.pageList.append(
        #     InstructionPage(None, self, "instruction/Instruction1.xml", InstructionPage.WITHOUT_PREV_BUTTON))
        # self.pageList.append(PreferencePage(None, self, "instruction/ExampleInstruction.xml",
        #                                     PreferencePage.TYPE_EXAMPLE, 0, 10, 0, 10, 80, 10, -1))
        # self.pageList.append(InstructionPage(None, self, "instruction/Instruction2a.xml"))
        # self.pageList.append(PreferencePage(None, self, "instruction/ExampleInstruction.xml",
        #                                     PreferencePage.TYPE_DEMO, 0, 20, 0, 20, 60, 10, -1))
        # self.pageList.append(InstructionPage(None, self, "instruction/Instruction2b.xml"))
        # self.pageList.append(PreferencePage(None, self, "instruction/ExampleInstruction.xml",
        #                                     PreferencePage.TYPE_DEMO2, 0, 30, 0, 30, 40, 10, -1))
        # self.pageList.append(InstructionPage(None, self, "instruction/Instruction3.xml", InstructionPage.PAYMENT))
        # # These are practice session 1 and 2
        # self.pageList.append(PreferencePage(None, self, "instruction/Practice1.xml",
        #                                     PreferencePage.TYPE_PRACTICE, 0, 10, 0, 10, 80, 10, -1))
        # self.pageList.append(PreferencePage(None, self, "instruction/Practice2.xml",
        #                                     PreferencePage.TYPE_PRACTICE, 0, 40, 0, 40, 60, 10, -1))
        # self.pageList.append(InstructionPage(None, self, "instruction/Instruction4.xml", InstructionPage.LAST))

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
            mc1 = float(row[1]) if isfloat(row[1]) else -1
            mc2 = float(row[2]) if isfloat(row[1]) else -1
            n = float(row[3]) if isfloat(row[2]) else -1
            u = float(row[4]) if isfloat(row[3]) else -1
            o1 = float(row[5]) if isfloat(row[4]) else -1
            o2 = float(row[6]) if isfloat(row[5]) else -1

            # choose appropriate instruction file according to the value of Money Colour 2
            instructionFile = "instruction/InstructionIntervalAmbiguity.xml"
            if mc2 > 0:
                instructionFile = "instruction/InstructionIntervalCompound.xml"

            self.pageList.append(PreferencePage(None, self, instructionFile,
                                                type, pn, mc1, mc2, n, u, o1, o2))
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
            page.Close(True)
        self.mainProcess.Exit()


#-----
def simulate(main):
    simulation = Simulation(main)
    simulation.simulate()
#-----

app = wx.App(False)
main = Application(app)
main.Start()

#-----
thread1 = threading.Thread(target = simulate, args = (main,))
thread1.start()
#-----

app.MainLoop()
