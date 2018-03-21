import sys
import  os

from PySide import  QtGui, QtCore, QtUiTools
import shiboken

import maya.cmds as cmds
import maya.OpenMayaUI as maya_ui
import pymel.core as pm



####################
# GLOBAL VARIABLES #
####################
SCRIPT_LOC = os.path.split(__file__)[0]
WINDOW_TITLE = "CheckTool"
MAIN_WINDOW_FILE = SCRIPT_LOC + "//check_tool.ui"


def load_ui_layout(filename, parent=None):
    loader = QtUiTools.QUiLoader()
    ui_file = QtCore.QFile(filename)
    ui_file.open(QtCore.QFile.ReadOnly)
    ui_layout = loader.load(ui_file, parent)
    ui_file.close()
    return ui_layout


def run():
    if not (cmds.window(WINDOW_TITLE, exists=True)):
        CheckToolUI()
    else:
        print('Check Tool is already opened\n')


class CheckToolUI(QtGui.QMainWindow):
    def __init__(self):
        maya_main = shiboken.wrapInstance(long(maya_ui.MQtUtil.mainWindow()),QtGui.QWidget)
        super(CheckToolUI, self).__init__(maya_main)

        #load main layout by qt
        self.MainWindowUI = load_ui_layout(MAIN_WINDOW_FILE, maya_main)
        self.MainWindowUI.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.MainWindowUI.destroyed.connect(self.on_exit)
        self.MainWindowUI.show()

        #add button event
        self.add_button_event()

    def add_button_event(self):
        self.MainWindowUI.pushButton.clicked.connect(lambda: self.check_non_manifold_geometry())
        self.MainWindowUI.pushButton_2.clicked.connect(lambda: self.check_default_shader())
        self.MainWindowUI.pushButton_3.clicked.connect(lambda: self.check_same_name())
        self.MainWindowUI.pushButton_4.clicked.connect(lambda: self.remove_empty_group())

    def on_exit(self):
        print('Close the ui')

    def on_result_message(self, value):
        self.MainWindowUI.labe_2.setText("Output:\n{0}", format(value))

    def check_non_manifold_geometry(self):
        self.on_result_message('check_non_manifold_geometry')

    def check_default_shader(self):
        self.on_result_message('check_default_shader')

    def check_same_name(self):
        self.on_result_message('check_same_name')

    def remove_empty_group(self):
        self.on_result_message('remove_empty_group')
