import wx
import wx.richtext as rt
import wx.grid as gr
import os
import requests
import ConfigParser

from StringIO import StringIO
from threading import Timer

COL_HEADER = 0
NUM_OF_COLS = 3  # for now it can create 3 or 5 columns


class PreferencePage(wx.Frame):
    TYPE_EXAMPLE = 0
    TYPE_DEMO = 1
    TYPE_REAL = 2
    TYPE_REAL_FINAL = 3
    TYPE_PRACTICE = 4
    TYPE_DEMO2 = 5

    def __init__(self, parent, application, instructionFile, type=TYPE_REAL, pn=0, mc1=0, mc2=0, n=0, u=0, o1=0, o2=0):
        super(PreferencePage, self).__init__(parent, title="Preference Page", size=(640, 480))
        self.application = application
        self.type = type
        self.instructionFile = instructionFile
        self.selectedColor = wx.Colour(67, 110, 238)
        self.inactiveColor = wx.Colour(254, 254, 254)
        self.blankColor = wx.Colour(255, 255, 255)
        self.pn = pn
        self.mc1 = mc1
        self.mc2 = mc2
        self.n = n
        self.u = u
        self.o1 = o1
        self.o2 = o2
        self.mc1u = self.mc1 + self.u
        self.g = "gain"
        if self.o1 < 0:
            self.g = "loss"

        self.payoff = 0.00
        self.fromPayoff = 0.00
        self.toPayoff = 0.00

        self.Hide()
        self.Center()
        self.initUI()
        # self.Maximize(True)
        self.ShowFullScreen(True)
        self.Hide()

        self.prevCellRow = -1
        self.prevCellCol = -1
        self.topRow = 0
        self.bottomRow = 0

        self.lastSelectedColumn = 0

        self.duration = 10  # Timer duration for the 'CONFIRM' button in seconds
        self.isBlankCellExists = True  # the cell is still blank
        self.timerActive = False  # 'FALSE' if the timer is active; 'TRUE' if the timer is inactive
        # self.Bind(wx.EVT_SHOW, self.pageShow)

    def initUI(self):  # define a panel for the preference page

        self.increment = 0.25
        pn, mc, n, u, o1, o2 = self.pn, self.mc1, self.n, self.u, self.o1, self.o2
        row, col = 0, 0

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        fontRichText = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())  # add suppport to read xml for richtext
        wx.FileSystem.AddHandler(wx.MemoryFSHandler())  # add suppport to read xml for richtext
        richText = rt.RichTextCtrl(panel, style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER, size=(-1, 190));
        richText.SetFont(fontRichText)
        path = os.path.abspath(self.instructionFile)
        richText.LoadFile(path, rt.RICHTEXT_TYPE_XML)

        # reading the xml from the richtext
        handler = wx.richtext.RichTextXMLHandler()
        buffer = richText.GetBuffer()
        inputOutput = StringIO()
        handler.SaveStream(buffer, inputOutput)
        inputOutput.seek(0)
        text = inputOutput.read()

        # replace the variable markups with the real values
        text = text.replace("[pn]", ('%.0f' % self.pn))
        text = text.replace("[mc1]", ('%.0f' % self.mc1))
        text = text.replace("[mc2]", ('%.0f' % self.mc2))
        text = text.replace("[n]", ('%.0f' % self.n))
        text = text.replace("[u]", ('%.0f' % self.u))
        text = text.replace("[o1]", ('%.2f' % self.o1))
        text = text.replace("[o2]", ('%.2f' % self.o2))
        text = text.replace("[mc1u]", ('%.0f' % self.mc1u))
        text = text.replace("[g]", self.g)

        # rewrite the xml back to the richtext
        handler2 = wx.richtext.RichTextXMLHandler()
        buffer2 = richText.GetBuffer()
        inputOutput2 = StringIO()
        buffer2.AddHandler(handler2)
        inputOutput2.write(text)
        inputOutput2.seek(0)
        handler.LoadStream(buffer2, inputOutput2)
        richText.Refresh()

        richText.SetEditable(False)
        # richText.SetBackgroundColour(wx.Colour(240,240,240))
        hbox1.Add(richText, flag=wx.EXPAND, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=8)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.grid = gr.Grid(panel, -1)
        grid = self.grid
        grid.CreateGrid(0, 0)

        grid.AppendCols(4)

        grid.SetColLabelValue(0, "Certain amount")
        grid.SetColLabelValue(2, "I am not sure about my preference")
        if o1 >= 0.0:
            grid.SetColLabelValue(1, "I am sure I prefer the lottery")
            grid.SetColLabelValue(3, "I am sure I prefer to get the certain amount")
        else:
            grid.SetColLabelValue(1, "I am sure I prefer to get the certain amount")
            grid.SetColLabelValue(3, "I am sure I prefer the lottery")



        if o1 >= 0.0:
            bottomValue = 0.0
            topValue = o1
            while bottomValue <= topValue:
                grid.AppendRows(1)
                grid.SetCellValue(row, col, "Receiving " + unichr(163) + ('%.2f' % bottomValue))
                grid.SetCellFont(row, col, wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                grid.SetCellBackgroundColour(row, col, wx.Colour(240, 240, 240))
                grid.SetCellAlignment(row, col, wx.ALIGN_CENTRE, wx.ALIGN_TOP)
                bottomValue += self.increment
                row += 1
        else:
            bottomValue = 0.0
            topValue = o1
            while bottomValue >= topValue:
                grid.AppendRows(1)
                grid.SetCellValue(row, col, "Receiving " + unichr(163) + ('%.2f' % bottomValue))
                grid.SetCellFont(row, col, wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                grid.SetCellBackgroundColour(row, col, wx.Colour(240, 240, 240))
                grid.SetCellAlignment(row, col, wx.ALIGN_CENTRE, wx.ALIGN_TOP)
                bottomValue -= self.increment
                row += 1

        grid.EnableEditing(False)
        grid.Bind(gr.EVT_GRID_SELECT_CELL, self.OnCellSelect)

        # add payoff number section
        vboxPayoff = wx.BoxSizer(wx.VERTICAL)
        fontPayoff = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD)
        self.labelPayoff = wx.StaticText(panel, label="Insert the amount of money\n"
                                                      "at which you are willing to switch\n"
                                                      "from being sure you prefer Option B\n"
                                                      "to being sure you prefer Option A.\n"
                                                      "Choose a value between " + unichr(163) +
                                                      ('%.2f' % self.fromPayoff) +
                                                      " and " + unichr(163) + ('%.2f' % self.toPayoff) + ".")

        self.labelPayoff.SetFont(fontPayoff)
        self.spinPayoff = wx.SpinCtrlDouble(panel, size=(200, -1), style=wx.TE_CENTRE)
        self.spinPayoff.SetFont(fontPayoff)
        self.spinPayoff.SetDigits(2)
        self.spinPayoff.SetMax(100.00)
        self.spinPayoff.SetMin(-100.00)
        self.spinPayoff.SetValue(100.00)
        self.spinPayoff.SetIncrement(self.increment)
        self.spinPayoff.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnSpinPayoffValueChanged)

        vboxPayoff.Add(self.labelPayoff, border=10)
        vboxPayoff.AddSpacer(10)
        vboxPayoff.Add(self.spinPayoff, border=10)

        hbox2.Add(grid, flag=wx.GROW | wx.ALL, proportion=3)
        hbox2.AddSpacer(10)
        hbox2.Add(vboxPayoff, flag=wx.FIXED_MINSIZE, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM,
                 border=10, proportion=1)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD)

        self.buttonConfirm = wx.Button(panel, label="CONFIRM")
        self.buttonConfirm.SetFont(font)
        self.buttonConfirm.Bind(wx.EVT_BUTTON, self.OnButtonConfirmClick)
        self.buttonConfirm.Disable()

        buttonNext = wx.Button(panel, label="NEXT")
        buttonNext.SetFont(font)
        buttonNext.Bind(wx.EVT_BUTTON, self.OnButtonNextClick)

        buttonClear = wx.Button(panel, label="CLEAR")
        buttonClear.SetFont(font)
        buttonClear.Bind(wx.EVT_BUTTON, self.OnButtonClearCLick)

        buttonPrev = wx.Button(panel, label="PREV")
        buttonPrev.SetFont(font)
        buttonPrev.Bind(wx.EVT_BUTTON, self.OnButtonPrevClick)

        self.buttonCon = wx.Button(panel, label="CONFIRM")
        self.buttonCon.SetFont(font)
        self.buttonCon.Bind(wx.EVT_BUTTON, self.OnButtonNextClick)
        self.buttonCon.Disable()

        if self.type == self.TYPE_EXAMPLE:
            leftBox = wx.BoxSizer(wx.VERTICAL)
            leftBox.Add(buttonPrev, flag=wx.ALIGN_LEFT)
            rightBox = wx.BoxSizer(wx.VERTICAL)
            rightBox.Add(buttonNext, flag=wx.ALIGN_RIGHT)
            hbox3.Add(leftBox, flag=wx.ALIGN_LEFT, proportion=1)
            hbox3.Add(rightBox, flag=wx.ALIGN_RIGHT, proportion=1)
            self.buttonConfirm.Hide()
            buttonClear.Hide()
            self.buttonCon.Hide()

        elif self.type == self.TYPE_DEMO:
            rightBox = wx.BoxSizer(wx.VERTICAL)
            rightBox.Add(buttonNext, flag=wx.ALIGN_RIGHT)
            centerBox = wx.BoxSizer(wx.VERTICAL)
            centerBox.Add(self.buttonConfirm, flag=wx.EXPAND | wx.ALIGN_CENTER)
            leftBox = wx.BoxSizer(wx.VERTICAL)
            leftBox.Add(buttonPrev, flag=wx.ALIGN_LEFT)
            hbox3.Add(leftBox, flag=wx.ALIGN_LEFT)
            hbox3.Add(centerBox, flag=wx.ALIGN_CENTRE, proportion=1)
            hbox3.Add(rightBox, flag=wx.ALIGN_RIGHT)
            buttonClear.Hide()
            self.buttonCon.Hide()

            for row in range(0, grid.GetNumberRows(), 1):
                for col in range(1, grid.GetNumberCols(), 1):
                    grid.SetCellValue(row, col, "")
                    grid.SetCellBackgroundColour(row, col, self.inactiveColor)

            if NUM_OF_COLS == 3:
                for row in range(0, 21, 1):
                    grid.SetCellValue(row, 1, "")
                    grid.SetCellBackgroundColour(row, 1, self.selectedColor)

                for row in range(21, 35, 1):
                    grid.SetCellValue(row, 2, "")
                    grid.SetCellBackgroundColour(row, 2, self.selectedColor)

                for row in range(35, grid.GetNumberRows(), 1):
                    grid.SetCellValue(row, 3, "")
                    grid.SetCellBackgroundColour(row, 3, self.selectedColor)

            elif NUM_OF_COLS == 5:
                for row in range(0, 8, 1):
                    grid.SetCellValue(row, 1, "")
                    grid.SetCellBackgroundColour(row, 1, self.selectedColor)

                for row in range(8, 13, 1):
                    grid.SetCellValue(row, 2, "")
                    grid.SetCellBackgroundColour(row, 2, self.selectedColor)

                for row in range(13, 17, 1):
                    grid.SetCellValue(row, 3, "")
                    grid.SetCellBackgroundColour(row, 3, self.selectedColor)

                for row in range(17, 20, 1):
                    grid.SetCellValue(row, 4, "")
                    grid.SetCellBackgroundColour(row, 4, self.selectedColor)

                for row in range(20, grid.GetNumberRows(), 1):
                    grid.SetCellValue(row, 5, "")
                    grid.SetCellBackgroundColour(row, 5, self.selectedColor)

        elif self.type == self.TYPE_DEMO2:
            rightBox = wx.BoxSizer(wx.VERTICAL)
            rightBox.Add(buttonNext, flag=wx.ALIGN_RIGHT)
            centerBox = wx.BoxSizer(wx.VERTICAL)
            centerBox.Add(self.buttonConfirm, flag=wx.EXPAND | wx.ALIGN_CENTER)
            leftBox = wx.BoxSizer(wx.VERTICAL)
            leftBox.Add(buttonPrev, flag=wx.ALIGN_LEFT)
            hbox3.Add(leftBox, flag=wx.ALIGN_LEFT)
            hbox3.Add(centerBox, flag=wx.ALIGN_CENTRE, proportion=1)
            hbox3.Add(rightBox, flag=wx.ALIGN_RIGHT)
            buttonClear.Hide()
            self.buttonCon.Hide()

            for row in range(0, grid.GetNumberRows(), 1):
                for col in range(1, grid.GetNumberCols(), 1):
                    grid.SetCellValue(row, col, "")
                    grid.SetCellBackgroundColour(row, col, self.inactiveColor)

            if NUM_OF_COLS == 3:
                for row in range(0, 15, 1):
                    grid.SetCellValue(row, 1, "")
                    grid.SetCellBackgroundColour(row, 1, self.selectedColor)

                for row in range(15, 31, 1):
                    grid.SetCellValue(row, 2, "")
                    grid.SetCellBackgroundColour(row, 2, self.selectedColor)

                for row in range(31, 41, 1):
                    grid.SetCellValue(row, 3, "")
                    grid.SetCellBackgroundColour(row, 3, self.selectedColor)

            elif NUM_OF_COLS == 5:
                for row in range(0, 8, 1):
                    grid.SetCellValue(row, 1, "")
                    grid.SetCellBackgroundColour(row, 1, self.selectedColor)

                for row in range(8, 13, 1):
                    grid.SetCellValue(row, 2, "")
                    grid.SetCellBackgroundColour(row, 2, self.selectedColor)

                for row in range(13, 17, 1):
                    grid.SetCellValue(row, 3, "")
                    grid.SetCellBackgroundColour(row, 3, self.selectedColor)

                for row in range(17, 20, 1):
                    grid.SetCellValue(row, 4, "")
                    grid.SetCellBackgroundColour(row, 4, self.selectedColor)

                for row in range(20, grid.GetNumberRows(), 1):
                    grid.SetCellValue(row, 5, "")
                    grid.SetCellBackgroundColour(row, 5, self.selectedColor)

        elif self.type == self.TYPE_PRACTICE:
            centerBox = wx.BoxSizer(wx.VERTICAL)
            centerBox.Add(self.buttonCon, flag=wx.EXPAND | wx.ALIGN_CENTER)
            hbox3.Add(centerBox, flag=wx.ALIGN_CENTRE, proportion=1)
            rightBox = wx.BoxSizer(wx.VERTICAL)
            rightBox.Add(buttonClear, flag=wx.ALIGN_RIGHT)
            hbox3.Add(rightBox, flag=wx.ALIGN_RIGHT)
            buttonNext.Hide()
            buttonPrev.Hide()
            self.buttonConfirm.Hide()

        elif self.type == self.TYPE_REAL:
            centerBox = wx.BoxSizer(wx.VERTICAL)
            centerBox.Add(self.buttonConfirm, flag=wx.EXPAND | wx.ALIGN_CENTER)
            hbox3.Add(centerBox, flag=wx.ALIGN_CENTRE, proportion=1)
            rightBox = wx.BoxSizer(wx.VERTICAL)
            rightBox.Add(buttonClear, flag=wx.ALIGN_RIGHT)
            hbox3.Add(rightBox, flag=wx.ALIGN_RIGHT)
            buttonNext.Hide()
            buttonPrev.Hide()
            self.buttonCon.Hide()

        elif self.type == self.TYPE_REAL_FINAL:
            self.buttonConfirm.SetLabel("FINISH THE EXPERIMENT")
            centerBox = wx.BoxSizer(wx.VERTICAL)
            centerBox.Add(self.buttonConfirm, flag=wx.EXPAND | wx.ALIGN_CENTER)
            hbox3.Add(centerBox, flag=wx.ALIGN_CENTRE, proportion=1)
            rightBox = wx.BoxSizer(wx.VERTICAL)
            rightBox.Add(buttonClear, flag=wx.ALIGN_RIGHT)
            hbox3.Add(rightBox, flag=wx.ALIGN_RIGHT)
            buttonNext.Hide()
            buttonPrev.Hide()
            self.buttonCon.Hide()

        panel.SetSizer(vbox)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=8)

        ###Resize columns
        grid.SetDefaultCellOverflow(True)
        grid.SetDefaultEditor(wx.grid.GridCellAutoWrapStringEditor())
        grid.AutoSizeColumns()
        for col in range(1, grid.GetNumberCols(), 1):
            grid.SetCellOverflow(0, col, True)

        total = 0
        widestCol = 0
        for col in range(1, grid.GetNumberCols(), 1):
            if widestCol < grid.GetColSize(col):
                widestCol = grid.GetColSize(col)

        for col in range(1, grid.GetNumberCols(), 1):
            grid.SetColSize(col, widestCol)

        grid.DisableDragColSize()
        grid.DisableDragRowSize()

    def OnSpinPayoffValueChanged(self, event):
        self.payoff = self.spinPayoff.GetValue()
        grid = self.grid

        # Check whether blank cell exists or not
        if (
                self.fromPayoff <= self.toPayoff and self.spinPayoff.GetValue() >= self.fromPayoff and self.spinPayoff.GetValue() <= self.toPayoff) \
                or (
                self.fromPayoff > self.toPayoff and self.spinPayoff.GetValue() >= self.toPayoff and self.spinPayoff.GetValue() <= self.fromPayoff):
            self.isBlankCellExists = False
            for row in range(0, grid.GetNumberRows(), 1):
                for col in range(1, grid.GetNumberCols(), 1):
                    cellColor = grid.GetCellBackgroundColour(row, col)
                    if cellColor.GetRGBA() == self.blankColor.GetRGBA():
                        self.isBlankCellExists = True
                        break
                if self.isBlankCellExists:
                    break
            if self.isBlankCellExists:
                self.buttonConfirm.Disable()
                self.buttonCon.Disable()
            else:
                if self.timerActive == False:
                    self.buttonConfirm.Enable()
                    self.buttonCon.Enable()
                else:
                    self.buttonConfirm.Disable()
                    self.buttonCon.Disable()
        else:
            self.buttonConfirm.Disable()
            self.buttonCon.Disable()

    def OnButtonNextClick(self, event):
        self.application.NextPage()

    def OnButtonPrevClick(self, event):
        self.application.PrevPage()

    def OnButtonConfirmClick(self, event):
        if self.type == self.TYPE_REAL:
            self.application.NextPage()
        elif self.type == self.TYPE_REAL_FINAL:
            if self.SubmitDataToServer():
                self.application.NextPage()

    def OnButtonClearCLick(self, event):
        self.lastSelectedColumn = 0
        grid = self.grid
        for row in range(0, grid.GetNumberRows(), 1):
            for col in range(1, grid.GetNumberCols(), 1):
                grid.SetCellValue(row, col, "")
                grid.SetCellBackgroundColour(row, col, self.blankColor)

        self.topRow = 0
        self.bottomRow = 0
        self.buttonConfirm.Disable()
        self.buttonCon.Disable()

        self.fromPayoff = 0.00
        self.toPayoff = 0.00
        self.labelPayoff.SetLabel("Insert the amount of money\n"
                                  "at which you are willing to switch\n"
                                  "from being sure you prefer Option B\n"
                                  "to being sure you prefer Option A.\n"
                                  "Choose a value between " + unichr(163) + ('%.2f' % self.fromPayoff) +
                                  " and " + unichr(163) + ('%.2f' % self.toPayoff) + ".")

    def OnCellSelect(self, event):
        grid = self.grid
        row = event.GetRow()
        col = event.GetCol()

        if self.type in [self.TYPE_DEMO, self.TYPE_EXAMPLE]:
            return

        # No response if a user clicks on cells on column proposed amount of money
        if event.GetCol() == 0:
            return

        # # prevent selecting other cells except selecting the top left cell first
        # topLeftCellColour = grid.GetCellBackgroundColour(0, 1)
        # if (row > 0 or col > 1) and topLeftCellColour.GetRGBA() == self.blankColor.GetRGBA():
        #     return

        # force users to select middle and right cells and prevent users to select back the left cells if middle
        # and right cells already selected
        elif col > self.lastSelectedColumn + 1:
            return

        if col > self.lastSelectedColumn:
            self.lastSelectedColumn = col

        if col < self.lastSelectedColumn:
            return
        elif col == 1 and (row >= grid.GetNumberRows() - 2):
            return
        elif col == 2 and (row >= grid.GetNumberRows() - 1):
            return

        # No response if a user clicks on inactive cells
        selectedGridColor = grid.GetCellBackgroundColour(row, col)
        if selectedGridColor.GetRGBA() == self.inactiveColor.GetRGBA():
            return

        # Set color to the inactive cells
        self.bottomRow = row;
        # left inactive cells
        for r in range(self.topRow, self.bottomRow + 1, 1):
            for c in range(1, col, 1):
                grid.SetCellValue(r, col, "")
                grid.SetCellBackgroundColour(r, c, self.inactiveColor)
        # right inactive cells
        for r in range(self.topRow, self.bottomRow + 1, 1):
            for c in range(col + 1, grid.GetNumberCols(), 1):
                grid.SetCellValue(r, col, "")
                grid.SetCellBackgroundColour(r, c, self.inactiveColor)

        # Set color to selected cells
        for r in range(self.topRow, self.bottomRow + 1, 1):
            grid.SetCellValue(r, col, "")
            grid.SetCellBackgroundColour(r, col, self.selectedColor)

        # determine fromPayoff and toPayoff
        if col == 1:
            for row in range(0, grid.GetNumberRows(), 1):
                cellColor = grid.GetCellBackgroundColour(row, 1)
                if cellColor.GetRGBA() == self.selectedColor.GetRGBA():
                    text = grid.GetCellValue(row, 0).encode("utf-8")
                    nominalValue = text[12:]
                    self.fromPayoff = float(nominalValue)
        elif col == 3:
            for row in range(0, grid.GetNumberRows(), 1):
                cellColor = grid.GetCellBackgroundColour(row, col)
                if cellColor.GetRGBA() == self.selectedColor.GetRGBA():
                    text = grid.GetCellValue(row, 0).encode("utf-8")
                    nominalValue = text[12:]
                    self.toPayoff = float(nominalValue)
                    break

        self.labelPayoff.SetLabel("Insert the amount of money\n"
                                  "at which you are willing to switch\n"
                                  "from being sure you prefer Option B\n"
                                  "to being sure you prefer Option A.\n"
                                  "Choose a value between " + unichr(163) + ('%.2f' % self.fromPayoff) +
                                  " and " + unichr(163) + ('%.2f' % self.toPayoff) + ".")

        # Check whether blank cell exists or not
        self.isBlankCellExists = False
        for row in range(0, grid.GetNumberRows(), 1):
            for col in range(1, grid.GetNumberCols(), 1):
                cellColor = grid.GetCellBackgroundColour(row, col)
                if cellColor.GetRGBA() == self.blankColor.GetRGBA():
                    self.isBlankCellExists = True
                    break
            if self.isBlankCellExists:
                break
        if self.isBlankCellExists:
            self.buttonConfirm.Disable()
            self.buttonCon.Disable()
        else:
            if self.timerActive == False:
                if (
                        self.fromPayoff <= self.toPayoff and self.spinPayoff.GetValue() >= self.fromPayoff and self.spinPayoff.GetValue() <= self.toPayoff) \
                        or (
                        self.fromPayoff > self.toPayoff and self.spinPayoff.GetValue() >= self.toPayoff and self.spinPayoff.GetValue() <= self.fromPayoff):
                    self.buttonConfirm.Enable()
                    self.buttonCon.Enable()
            else:
                self.buttonConfirm.Disable()
                self.buttonCon.Disable()

        # Update top row and col for next selection iteration
        self.topRow = row
        self.topCol = col

    # The following codes are to save the subjects' data into csv and send it to the server
    def SubmitDataToServer(self):
        try:
            preferenceSheetList = [sheet for sheet in self.application.pageList
                                   if isinstance(sheet, PreferencePage) and sheet.type in [self.TYPE_REAL,
                                                                                           self.TYPE_REAL_FINAL]]
            preferenceSheetNumber = 1
            data = []
            for preferenceSheet in preferenceSheetList:
                row = [str(preferenceSheetNumber)]
                row.append(str(preferenceSheet.payoff))
                grid = preferenceSheet.grid

                for gridRow in range(0, grid.GetNumberRows(), 1):
                    text = grid.GetCellValue(gridRow, 0).encode("utf-8")
                    nominalValue = text[12:]
                    row.append(nominalValue)

                    for gridCol in range(1, grid.GetNumberCols(), 1):
                        cellColor = grid.GetCellBackgroundColour(gridRow, gridCol)
                        if cellColor.GetRGBA() == self.selectedColor.GetRGBA():
                            value = gridCol
                            row.append(str(value))

                rowString = ", ".join(row)
                data.append(rowString)
                preferenceSheetNumber += 1

            filename = self.application.subjectNumber
            filenameWithExt = filename + ".csv"
            csvPath = os.path.abspath("results/subject" + filenameWithExt)

            csvfile = open(csvPath, 'w')
            csvfile.write("\n".join(data))
            csvfile.close()

            config = ConfigParser.ConfigParser()
            config.read("client.ini")
            server = config.get("Config", "Server")
            server += "/post"

            file = open(csvPath, 'r')
            text = file.read()
            file.close()
            myData = {
                "subject": filename,
                "data": text
            }
            response = requests.post(server, data=myData)
            if (response.text <> "1"):
                print "Error Save on Server"
                raise NameError("Error Save on Server")

            return True
        except Exception as e:
            print e.message
            return False

    # Set the timer
    def pageShow(self, event):
        if event.IsShown:
            if self.type in [PreferencePage.TYPE_REAL, PreferencePage.TYPE_REAL_FINAL, PreferencePage.TYPE_PRACTICE]:
                self.ticking()
                self.timerActive = True

    # Define the timer on the CONFIRM button
    def ticking(self):
        self.buttonConfirm.SetLabelText("CONFIRM (" + str(self.duration) + " second(s))")
        self.buttonCon.SetLabelText("CONFIRM (" + str(self.duration) + " second(s))")
        self.timer = Timer(1.0, self.ticking)
        self.timer.start()

        if self.duration <= 0:
            self.timer.cancel()
            self.timerActive = False
            self.buttonConfirm.SetLabelText("CONFIRM")
            self.buttonCon.SetLabelText("CONFIRM")
            if self.isBlankCellExists == False:
                self.buttonConfirm.Enable()
                self.buttonCon.Enable()
            else:
                self.buttonConfirm.Disable()
                self.buttonCon.Disable()
            return

        self.duration -= 1
