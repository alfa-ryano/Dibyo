import wx
import wx.grid as gr
import ConfigParser
import requests
from time import sleep
from PreferencePage import PreferencePage
from EndPage import EndPage
from wx.grid import GridEvent

SLEEP_DURATION = 0.1


class Simulation(wx.Frame):
    def __init__(self, parent):
        self.parent = parent

    def simulate(self):
        sleep(SLEEP_DURATION)
        subjectNumberPage = self.parent.pageList[0]
        subjectNumberPage.subjectNumberText.SetValue("1")
        sleep(SLEEP_DURATION)
        subjectButton = subjectNumberPage.button
        evt = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, subjectButton.GetId())
        wx.PostEvent(subjectButton, evt)
        sleep(SLEEP_DURATION)

        length = len(self.parent.pageList)
        for index in range(1, length):
            page = self.parent.pageList[index]
            # page = self.parent.pageList[1]

            if isinstance(page, PreferencePage):
                sleep(SLEEP_DURATION)
                gridEvent = gr.GridEvent(page.grid.GetId(), gr.wxEVT_GRID_SELECT_CELL, page.grid, row=13, col=1,
                                         sel=True)
                wx.PostEvent(page.grid, gridEvent)
                sleep(SLEEP_DURATION)
                gridEvent = gr.GridEvent(page.grid.GetId(), gr.wxEVT_GRID_SELECT_CELL, page.grid, row=26, col=2,
                                         sel=True)
                wx.PostEvent(page.grid, gridEvent)
                sleep(SLEEP_DURATION)
                gridEvent = gr.GridEvent(page.grid.GetId(), gr.wxEVT_GRID_SELECT_CELL, page.grid, row=40, col=3,
                                         sel=True)
                wx.PostEvent(page.grid, gridEvent)
                sleep(SLEEP_DURATION)
                payoff = (page.fromPayoff + page.toPayoff) / 2.0
                page.spinPayoff.SetValue(payoff)
                sleep(SLEEP_DURATION)
                gridEvent = gr.GridEvent(page.grid.GetId(), gr.wxEVT_GRID_SELECT_CELL, page.grid, row=40, col=3,
                                         sel=True)
                wx.PostEvent(page.grid, gridEvent)
                sleep(SLEEP_DURATION)
                confirmButton = page.buttonConfirm
                evt = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, confirmButton.GetId())
                wx.PostEvent(confirmButton, evt)
                sleep(SLEEP_DURATION)

            if isinstance(page, EndPage):
                sleep(SLEEP_DURATION)
                closeButton = page.buttonNext
                evt = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, closeButton.GetId())
                wx.PostEvent(closeButton, evt)
                sleep(SLEEP_DURATION)
