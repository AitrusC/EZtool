# -*- coding: UTF-8 -*-
# @FileName      : showUI
# @Time          : 2024-05-23
# @Author        : LJF
# @Contact       : 906629272@qq.com

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from . import chToolW
from . import control
from . import remaneT
from . import rigT
from . import uiWidget


def get_host_app():
    try:
        app = QApplication.activeWindow()
        while True:
            last_win = app.parent()
            if last_win:
                app = last_win
            else:
                break
        return app
    except:
        pass


class EZWindow(QWidget):
    def __init__(self, parent = get_host_app()):
        super(EZWindow, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.Window)
        self.setWindowTitle(u"EZtool")
        self.resize(650, 800)
        self.setMinimumSize(600, 800)
        self.setObjectName("EZtoolW")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        with open(__file__ + "/../res/qss/TadWidgetQSS.qss", "r") as f:
            self.tag_lqss = f.read()
        self.left_tag = uiWidget.TadWidget()
        self.left_tag.setStyleSheetLR(lqss = self.tag_lqss, rqss = "")
        self.widget1 = chToolW.CHtoolUI(self)
        self.widget2 = remaneT.ReNameUI(self)
        self.widget3 = control.ControlUI(self)
        self.widget4 = rigT.RigToolUi(self)
        self.icon_p1 = QIcon(__file__ + "/../res/images/Gear.png")
        self.icon_p2 = QIcon(__file__ + "/../res/images/REname.png")
        self.icon_p3 = QIcon(__file__ + "/../res/images/controlP.png")
        self.icon_p4 = QIcon(__file__ + "/../res/images/RigTP.png")
        self.left_tag.addInsertItem(
            [self.icon_p1, self.icon_p2, self.icon_p3, self.icon_p4],
            [self.widget1, self.widget2, self.widget3, self.widget4]
        )
        self.left_tag.left_widget.setCurrentRow(0)
        self.main_layout.addWidget(self.left_tag)


window_ez = None


def show():
    """
    显示界面
    :return:
    """
    global window_ez
    if window_ez is None:
        window_ez = EZWindow()
    window_ez.show()


if __name__ == '__main__':

    main_wnd = EZWindow()
    main_wnd.show()
