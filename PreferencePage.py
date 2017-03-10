import wx
import wx.richtext as rt
import wx.grid as gr
import os
import requests
import ConfigParser
from StringIO import StringIO

COL_HEADER = 0


class PreferencePage(wx.Frame):
    TYPE_EXAMPLE = 0
    TYPE_DEMO = 1
    TYPE_REAL = 2
    TYPE_REAL_FINAL = 3

    def __init__(self, parent, application, instructionFile, type=TYPE_REAL, v1=0, p1=0, v2=0, p2=0):
        super(PreferencePage, self).__init__(parent, title="Preference Page", size=(640, 480))
        self.application = application
        self.type = type
        self.instructionFile = instructionFile
        self.selectedColor = wx.Colour(200, 200, 200)
        self.inactiveColor = wx.Colour(0, 0, 0)
        self.blankColor = wx.Colour(255, 255, 255)
        self.v1 = v1;
        self.p1 = p1;
        self.v2 = v2;
        self.p2 = p2;

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

    def initUI(self):
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        fontRichText = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())  # add suppport to read xml for richtext
        wx.FileSystem.AddHandler(wx.MemoryFSHandler())  # add suppport to read xml for richtext
        richText = rt.RichTextCtrl(panel, style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER, size=(-1, 100));
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
        text = text.replace("[v1]", ('%.2f' % self.v1))
        text = text.replace("[v2]", ('%.2f' % self.v2))
        text = text.replace("[p1]", ('%.2f' % self.p1))
        text = text.replace("[p2]", ('%.2f' % self.p2))
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
        grid.AppendCols(6)

        grid.SetColLabelValue(0, "Proposed Amount of Money")
        grid.SetColLabelValue(1, "I'm sure I prefer Option A")
        grid.SetColLabelValue(2, "I think I prefer Option A but I'm not sure")
        grid.SetColLabelValue(3, "I'm indifferent between Option A and Option B")
        grid.SetColLabelValue(4, "I think I prefer Option B but I'm not sure")
        grid.SetColLabelValue(5, "I'm sure I prefer Option B")

        decrement = 0.50
        v1, v2, p1, p2 = self.v1, self.v2, self.p1, self.p2
        row, col = 0, 0
        while v1 >= v2:
            grid.AppendRows(1)
            grid.SetCellValue(row, col, "For \xA3" + ('%.2f' % v1))
            grid.SetCellFont(row, col, wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            grid.SetCellBackgroundColour(row, col, wx.Colour(240, 240, 240))
            grid.SetCellAlignment(row, col, wx.ALIGN_CENTRE, wx.ALIGN_TOP)
            v1 -= decrement
            row += 1

        grid.EnableEditing(False)
        grid.AutoSizeColumns()
        grid.Bind(gr.EVT_GRID_SELECT_CELL, self.OnCellSelect)

        hbox2.Add(grid, flag=wx.GROW | wx.ALL, proportion=1)
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

        if self.type == self.TYPE_EXAMPLE:
            leftBox = wx.BoxSizer(wx.VERTICAL)
            leftBox.Add(buttonPrev, flag=wx.ALIGN_LEFT)
            rightBox = wx.BoxSizer(wx.VERTICAL)
            rightBox.Add(buttonNext, flag=wx.ALIGN_RIGHT)
            hbox3.Add(leftBox, flag=wx.ALIGN_LEFT, proportion=1)
            hbox3.Add(rightBox, flag=wx.ALIGN_RIGHT, proportion=1)
            self.buttonConfirm.Hide()
            buttonClear.Hide()

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

            for row in range(0, grid.GetNumberRows(), 1):
                for col in range(1, grid.GetNumberCols(), 1):
                    grid.SetCellValue(row, col, "")
                    grid.SetCellBackgroundColour(row, col, self.inactiveColor)

            for row in range(0, 7, 1):
                grid.SetCellValue(row, 1, "")
                grid.SetCellBackgroundColour(row, 1, self.selectedColor)

            for row in range(7, 13, 1):
                grid.SetCellValue(row, 2, "")
                grid.SetCellBackgroundColour(row, 2, self.selectedColor)

            for row in range(13, 19, 1):
                grid.SetCellValue(row, 3, "")
                grid.SetCellBackgroundColour(row, 3, self.selectedColor)

            for row in range(19, 25, 1):
                grid.SetCellValue(row, 4, "")
                grid.SetCellBackgroundColour(row, 4, self.selectedColor)

            for row in range(25, grid.GetNumberRows(), 1):
                grid.SetCellValue(row, 5, "")
                grid.SetCellBackgroundColour(row, 5, self.selectedColor)


        elif self.type == self.TYPE_REAL:
            centerBox = wx.BoxSizer(wx.VERTICAL)
            centerBox.Add(self.buttonConfirm, flag=wx.EXPAND | wx.ALIGN_CENTER)
            hbox3.Add(centerBox, flag=wx.ALIGN_CENTRE, proportion=1)
            rightBox = wx.BoxSizer(wx.VERTICAL)
            rightBox.Add(buttonClear, flag=wx.ALIGN_RIGHT)
            hbox3.Add(rightBox, flag=wx.ALIGN_RIGHT)
            buttonNext.Hide()
            buttonPrev.Hide()

        elif self.type == self.TYPE_REAL_FINAL:
            self.buttonConfirm.SetLabelText("FINISH THE EXPERIMENT")
            centerBox = wx.BoxSizer(wx.VERTICAL)
            centerBox.Add(self.buttonConfirm, flag=wx.EXPAND | wx.ALIGN_CENTER)
            hbox3.Add(centerBox, flag=wx.ALIGN_CENTRE, proportion=1)
            rightBox = wx.BoxSizer(wx.VERTICAL)
            rightBox.Add(buttonClear, flag=wx.ALIGN_RIGHT)
            hbox3.Add(rightBox, flag=wx.ALIGN_RIGHT)
            buttonNext.Hide()
            buttonPrev.Hide()

        panel.SetSizer(vbox)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=8)

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
        grid = self.grid
        for row in range(0, grid.GetNumberRows(), 1):
            for col in range(1, grid.GetNumberCols(), 1):
                grid.SetCellValue(row, col, "")
                grid.SetCellBackgroundColour(row, col, self.blankColor)

        self.topRow = 0
        self.bottomRow = 0
        self.buttonConfirm.Disable()

    def OnCellSelect(self, event):
        grid = self.grid
        row = event.GetRow()
        col = event.GetCol()

        if self.type in [self.TYPE_DEMO, self.TYPE_EXAMPLE]:
            return

        # No response if a user clicks on cells on column proposed amount of money
        if event.GetCol() == 0:
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
        # left bottom side inactive cells
        for r in range(self.bottomRow, grid.GetNumberRows(), 1):
            for c in range(1, col, 1):
                grid.SetCellValue(r, col, "")
                grid.SetCellBackgroundColour(r, c, self.inactiveColor)

        # Set color to selected cells
        for r in range(self.topRow, self.bottomRow + 1, 1):
            grid.SetCellValue(r, col, "")
            grid.SetCellBackgroundColour(r, col, self.selectedColor)

        # Check whether blank cell exists or not
        isBlankCellExists = False
        for row in range(0, grid.GetNumberRows(), 1):
            for col in range(1, grid.GetNumberCols(), 1):
                cellColor = grid.GetCellBackgroundColour(row, col)
                if cellColor.GetRGBA() == self.blankColor.GetRGBA():
                    isBlankCellExists = True
                    break;
            if isBlankCellExists:
                break;
        if isBlankCellExists:
            self.buttonConfirm.Disable()
        else:
            self.buttonConfirm.Enable()

        # update top row and col for next selection iteration
        self.topRow = row
        self.topCol = col

    def SubmitDataToServer(self):
        try:
            preferenceSheetList = [sheet for sheet in self.application.pageList
                                   if isinstance(sheet, PreferencePage) and sheet.type in [self.TYPE_REAL,
                                                                                           self.TYPE_REAL_FINAL]]
            preferenceSheetNumber = 1
            data = []
            for preferenceSheet in preferenceSheetList:
                row = [str(preferenceSheetNumber)]
                grid = preferenceSheet.grid

                for gridRow in range(0, grid.GetNumberRows(), 1):
                    text = grid.GetCellValue(gridRow, 0).encode("utf-8")
                    nominalValue = text[6:]
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
            csvPath = os.path.abspath("results/" + filenameWithExt)

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

                ### Uncomment this if you want to use FTP
                # ftp = ftplib.FTP("files.000webhost.com")
                # ftp.login("alfa-ryano", "ZXCzxc")
                # # ftp = ftplib.FTP("localhost")
                # # ftp.login("user", "1234")
                # file = open(csvPath, "r")
                # ftp.storlines("STOR " + filename, file)
                # file.close()
                # ftp.quit()

            return True
        except Exception as e:
            print e.message
            return False
