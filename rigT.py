# -*- coding: UTF-8 -*-
# @FileName      : rigT
# @Time          : 2024-06-26
# @Author        : LJF
# @Contact       : 906629272@qq.com

"""
其他功能主面板
"""

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from . import motionP
from . import rigEZikfk
from . import jointOrientW


class RigToolUi(QWidget):
    """
    工具
    """

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setObjectName("RigToolWindow")

        self._createTabW()
        self._tabWidget()
        self._createLayout()

    def _createTabW(self):
        """
        几个工具的界面
        :return:
        """
        self.ezIkFk = rigEZikfk.EzIkFkUI()
        self.joint_ow = jointOrientW.JointOrientUI()
        self.motionp = motionP.MotionPUI()

    def _tabWidget(self):
        """
        tab
        :return:
        """
        qss = "QTabWidget { font: bold 10pt \"Microsoft YaHei\"; }"
        self.tab = QTabWidget()
        self.tab.setStyleSheet(qss)
        self.tab.addTab(self.ezIkFk, u"EzIkFk")
        self.tab.addTab(self.joint_ow, u"骨骼朝向设置")
        self.tab.addTab(self.motionp, u"路径约束")

    def _createLayout(self):
        """
        布局
        :return:
        """
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(10, 5, 10, 10)
        self.setLayout(self.mainLayout)

        self.mainLayout.addWidget(self.tab)

    def test(self):
        print(u"测试")


if __name__ == '__main__':
    import maya.OpenMayaUI as omui
    from shiboken2 import wrapInstance

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)


    class TestC(RigToolUi):

        def __init__(self, parent = mayaMainWindow):
            RigToolUi.__init__(self, parent)
            self.setWindowFlags(self.windowFlags() | Qt.Window)


    testUI = TestC()
    testUI.show()
