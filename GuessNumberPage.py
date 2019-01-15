from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import QFile, QTextStream, Qt
from customutil import CountDownTimer, format_decimal, COUNTDOWN_COUNT


class InputNumberDialog(QtGui.QDialog):
    def __init__(self, main_form, text, experiment_name):
        super(InputNumberDialog, self).__init__()

        uic.loadUi('ui/dialog.ui', self)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.main_form = main_form
        self.label_title.setText(experiment_name)
        self.button_ok.clicked.connect(self.on_button_ok_clicked)

        self.text_edit_instruction.setHtml(text)

        self.counter = COUNTDOWN_COUNT
        self.countDownTimer = CountDownTimer(10, 0, 1, self.countdown)
        self.countDownTimer.start()

    def countdown(self):
        if self.counter > 0:
            self.button_ok.setText("NEXT (" + str(self.counter) + ")")
            self.counter -= 1
        else:
            self.countDownTimer.stop()
            self.button_ok.setEnabled(True)
            self.button_ok.setText("NEXT")

    def keyPressEvent(self, event):
        if not event.key() == Qt.Key_Escape:
            super(InputNumberDialog, self).keyPressEvent(event)

    def on_button_ok_clicked(self):
        self.accept()

    def get_initial_asset_percentage(self):
        value = self.spinbox_asset_value.value()
        return value

