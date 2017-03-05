import wx
import wx.richtext as rt
import wx.grid as gr
import os
import csv
import ftplib
from MyUtil import UnicodeWriter
import requests
import ConfigParser

COL_HEADER = 0


class PreferencePage(wx.Frame):
    TYPE_EXAMPLE = 0
    TYPE_DEMO = 1
    TYPE_REAL = 2
    TYPE_REAL_FINAL = 3

    def __init__(self, parent, application, instructionFile, sheetFile, type=TYPE_REAL):
        super(PreferencePage, self).__init__(parent, title="Preference Page", size=(640, 480),
                                             style=wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX))
        self.application = application
        self.type = type
        self.instructionFile = instructionFile;
        self.sheetFile = sheetFile;

        self.Hide()
        self.Center()
        self.initUI()
        # self.Maximize(True)
        self.ShowFullScreen(True)
        self.Hide()

        self.prevCellRow = -1
        self.prevCellCol = -1

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
        richText.SetEditable(False)
        richText.SetFocus()
        # richText.SetBackgroundColour(wx.Colour(240,240,240))
        hbox1.Add(richText, flag=wx.EXPAND, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=8)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.grid = gr.Grid(panel, -1)
        grid = self.grid
        grid.CreateGrid(0, 0)

        csvPath = os.path.abspath(self.sheetFile)
        with open(csvPath, 'rb') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            nCol = len(next(csvReader))
            grid.AppendCols(numCols=nCol)
            csvfile.seek(0)
            y = 0
            for row in csvReader:
                if y > COL_HEADER:
                    grid.AppendRows(1)
                x = 0
                for cell in row:
                    if y == COL_HEADER:
                        grid.SetColLabelValue(x, cell)
                    if y > COL_HEADER:
                        grid.SetCellValue(y - 1, x, cell)
                        if x == 0:
                            grid.SetCellBackgroundColour(y - 1, 0, wx.Colour(240, 240, 240))
                    x += 1
                y += 1

        grid.EnableEditing(False)
        grid.AutoSizeColumns()
        grid.SetCellHighlightColour(wx.Colour(200, 200, 200))
        grid.SetSelectionBackground(wx.Colour(200, 200, 200))
        grid.SetCellHighlightPenWidth(10)
        grid.Bind(gr.EVT_GRID_SELECT_CELL, self.OnCellSelect)
        grid.Bind(gr.EVT_GRID_RANGE_SELECT, self.OnGridRangeSelect)

        hbox2.Add(grid, flag=wx.GROW | wx.ALL, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM,
                 border=10, proportion=1)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD)

        boxNext = wx.BoxSizer(wx.VERTICAL)
        buttonNext = wx.Button(panel, label="NEXT")
        buttonNext.SetFont(font)
        buttonNext.Bind(wx.EVT_BUTTON, self.OnButtonNextClick)
        boxNext.Add(buttonNext, flag=wx.ALIGN_RIGHT)

        boxConfirm = wx.BoxSizer(wx.VERTICAL)
        buttonConfirm = wx.Button(panel, label="CONFIRM")
        buttonConfirm.SetFont(font)
        buttonConfirm.Bind(wx.EVT_BUTTON, self.OnButtonConfirmClick)
        boxConfirm.Add(buttonConfirm, flag=wx.ALIGN_CENTER)

        boxPrev = wx.BoxSizer(wx.VERTICAL)
        buttonPrev = wx.Button(panel, label="PREV")
        buttonPrev.SetFont(font)
        buttonPrev.Bind(wx.EVT_BUTTON, self.OnButtonPrevClick)
        boxPrev.Add(buttonPrev, flag=wx.ALIGN_LEFT)

        hbox3.Add(boxPrev, flag=wx.ALIGN_LEFT, proportion=1)
        hbox3.Add(boxConfirm, flag=wx.EXPAND | wx.ALIGN_CENTRE, proportion=1)
        hbox3.Add(boxNext, flag=wx.ALIGN_RIGHT, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=8)

        panel.SetSizer(vbox)

        if self.type == self.TYPE_EXAMPLE:
            buttonConfirm.Hide()
        elif self.type == self.TYPE_REAL:
            buttonNext.Hide()
            buttonPrev.Hide()
        elif self.type == self.TYPE_REAL_FINAL:
            buttonNext.Hide()
            buttonPrev.Hide()
            buttonConfirm.SetLabelText("FINISH THE EXPERIMENT")

    def OnButtonNextClick(self, event):
        self.application.NextPage()

    def OnButtonPrevClick(self, event):
        self.application.PrevPage()

    def OnButtonConfirmClick(self, event):
        grid = self.grid
        lines = []
        sheetName = os.path.basename(self.sheetFile).split(".")[0]
        filename = self.application.subjectNumber +"_" + sheetName
        filenameWithExt = filename + ".csv"
        csvPath = os.path.abspath("results/" + filenameWithExt)
        with open(csvPath, 'wb') as csvfile:
            writer = UnicodeWriter(csvfile, delimiter=",")
            header = ["No"]
            for i in range(0, grid.GetNumberCols(), 1):
                header.append(grid.GetColLabelValue(i))
            lines.append(header)

            for row in range(0, grid.GetNumberRows(), 1):
                line = [str(row + 1)]
                for col in range(0, grid.GetNumberCols(), 1):
                    grayColor = wx.Colour(200, 200, 200)
                    whiteColor = wx.Colour(255, 255, 255)
                    currentColor = grid.GetCellBackgroundColour(row, col)
                    if currentColor.GetRGBA() == grayColor.GetRGBA():
                        line.append(str(1))
                    else:
                        if currentColor.GetRGBA() == whiteColor.GetRGBA():
                            line.append(str(0))
                        else:
                            line.append(grid.GetCellValue(row, col))
                lines.append(line)

            writer.writerows(lines)
            csvfile.close()

        try:
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

            wx.MessageBox('Data have been saved!', 'Info', wx.OK | wx.ICON_INFORMATION)
            if self.type == self.TYPE_REAL or self.type == self.TYPE_REAL_FINAL:
                self.application.NextPage()
        except:
            wx.MessageBox('Failed to save data!', 'Info', wx.OK | wx.ICON_INFORMATION)

    def OnGridRangeSelect(self, event):
        grid = self.grid
        grayColor = wx.Colour(200, 200, 200)
        whiteColor = wx.Colour(255, 255, 255)

        if event.ShiftDown():
            topRow = event.GetTopLeftCoords().Row
            topCol = event.GetTopLeftCoords().Col
            bottomRow = event.GetBottomRightCoords().Row
            bottomCol = event.GetBottomRightCoords().Col

            grid.SetCellHighlightPenWidth(0)

            prevCellColour = grid.GetCellBackgroundColour(self.prevCellRow, self.prevCellCol)
            if prevCellColour.GetRGBA() == whiteColor.GetRGBA():
                grid.SetCellBackgroundColour(self.prevCellRow, self.prevCellCol, whiteColor)
            else:
                grid.SetCellBackgroundColour(self.prevCellRow, self.prevCellCol, grayColor)
            prevCellNewColour = grid.GetCellBackgroundColour(self.prevCellRow, self.prevCellCol)

            for row in range(topRow, bottomRow + 1, 1):
                for col in range(topCol, bottomCol + 1, 1):
                    if col == 0:
                        continue
                    grid.SetCellBackgroundColour(row, col, prevCellNewColour)

        if event.ControlDown():
            grid.SetCellHighlightPenWidth(0)

            prevCellColour = grid.GetCellBackgroundColour(self.prevCellRow, self.prevCellCol)
            if prevCellColour.GetRGBA() == whiteColor.GetRGBA():
                grid.SetCellBackgroundColour(self.prevCellRow, self.prevCellCol, whiteColor)
            else:
                grid.SetCellBackgroundColour(self.prevCellRow, self.prevCellCol, grayColor)
            prevCellNewColour = grid.GetCellBackgroundColour(self.prevCellRow, self.prevCellCol)

            for cell in grid.GetSelectedCells():
                row = cell[0]
                col = cell[1]
                if col == 0:
                    continue
                grid.SetCellBackgroundColour(row, col, prevCellNewColour)

    def OnCellSelect(self, event):
        grid = self.grid
        row = event.GetRow()
        col = event.GetCol()
        if col == 0:
            return
        grayColor = wx.Colour(200, 200, 200)
        whiteColor = wx.Colour(255, 255, 255)
        currentColor = grid.GetCellBackgroundColour(row, col)
        if event.Selecting():
            grid.SetCellHighlightPenWidth(10)
            if currentColor.GetRGBA() == grayColor.GetRGBA():
                grid.SetCellBackgroundColour(row, col, whiteColor)
                grid.SetSelectionBackground(whiteColor)
                grid.SetCellHighlightColour(whiteColor)
            else:
                grid.SetCellBackgroundColour(row, col, grayColor)
                grid.SetSelectionBackground(grayColor)
                grid.SetCellHighlightColour(grayColor)

        self.prevCellRow = row
        self.prevCellCol = col
