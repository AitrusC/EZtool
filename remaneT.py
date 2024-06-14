# -*- coding: UTF-8 -*-
# @FileName      : remaneT
# @Time          : 2024-05-23
# @Author        : LJF
# @Contact       : 906629272@qq.com

from functools import partial

import maya.cmds as cmds
from . import uiWidget
from PySide2.QtCore import *
from PySide2.QtWidgets import *


class ReNameUI(QWidget):
    """
    重命名
    """

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setObjectName("ReNameWin")

        self._createLabel()
        self._createCBWidgets()
        self._createLineEdit()
        self._createPushBtn()
        self._createSplitter()
        self._createLineEditPBtn()
        self._createRadioB()
        self._createConnect()
        self._createLayout()

    def _createSplitter(self):
        """
        分割线
        """
        self.splitter1 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)
        self.splitter2 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)
        self.splitter3 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)
        self.splitter4 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)

    def _createLabel(self):
        """
        标签
        """
        qss = "color: rgb(248, 244, 237); font: bold 10pt Microsoft YaHei;"
        self.label1 = QLabel(u"重命名:")
        self.label2 = QLabel(u"位数:")
        self.label3 = QLabel(u"搜索:")
        self.label4 = QLabel(u"替换:")
        self.label1.setStyleSheet(qss)
        self.label2.setStyleSheet(qss)
        self.label3.setStyleSheet(qss)
        self.label4.setStyleSheet(qss)

    def _createCBWidgets(self):
        """
        下拉框
        :return:
        """
        self.numItems = QComboBox()
        self.numItems.addItems(["2", "3", "4"])

    def _createRadioB(self):
        """
        选框
        """
        qss = """QRadioButton {
                              font: bold 8pt Microsoft YaHei;
                              color: rgb(248, 244, 237);
                              }
                            """
        self.checkB1 = QRadioButton(u"所选")
        self.checkB1.setChecked(True)
        self.checkB2 = QRadioButton(u"层级")
        self.checkB3 = QRadioButton(u"全部")
        self.checkB1.setStyleSheet(qss)
        self.checkB2.setStyleSheet(qss)
        self.checkB3.setStyleSheet(qss)
        self.checkGroup = QButtonGroup()
        self.checkGroup.addButton(self.checkB1, 1)
        self.checkGroup.addButton(self.checkB2, 2)
        self.checkGroup.addButton(self.checkB3, 3)
        self.checkGroup.setExclusive(True)

    def _createLineEditPBtn(self):
        """
        文字 文本框 按钮
        """
        self.linePBtn1 = uiWidget.LineEditPBtn(u"前缀:")
        self.linePBtn2 = uiWidget.LineEditPBtn(u"后缀:")

    def _createLineEdit(self):
        """
        输入框
        """
        qss = """QLineEdit {
                              font: bold 8pt Microsoft YaHei;
                              color: rgb(248, 244, 237);
                              }
                            """
        self.lineE1 = QLineEdit()
        self.lineE3 = QLineEdit()
        self.lineE4 = QLineEdit()
        self.lineE1.setStyleSheet(qss)
        self.lineE3.setStyleSheet(qss)
        self.lineE4.setStyleSheet(qss)

    def _createPushBtn(self):
        """
        按钮
        """
        qss1 = """QPushButton {
                                background-color: rgb(82, 82, 136);
                                color: rgb(204, 204, 214);
                                border: 1px solid;
                                border-radius: 3px;border-color: rgb(82, 82, 136);
                                font: bold 10pt \"Microsoft YaHei\";height: 25px;
                                }
                QPushButton:hover {
                                border: rgb(116, 117, 155);
                                background-color: rgb(116, 117, 155);
                                }
                QPushButton:pressed {
                                background-color: rgb(128, 109, 158);
                                }"""
        qss2 = """QPushButton {
                                background-color: rgb(134, 112, 24);
                                color: rgb(204, 204, 214);
                                border: 1px solid;
                                border-radius: 3px;border-color: rgb(134, 112, 24);
                                font: bold 10pt \"Microsoft YaHei\";height: 25px;
                                }
                QPushButton:hover {
                                border: rgb(172, 150, 62);
                                background-color: rgb(172, 150, 62);
                                }
                QPushButton:pressed {
                                background-color: rgb(182, 160, 52);
                                }"""
        self.pushB1 = QPushButton(u"重命名及编号")
        self.pushB1.setFixedHeight(40)
        self.addGrp = QPushButton("_Grp")
        self.addCtrl = QPushButton("_Ctrl")
        self.addJnt = QPushButton("_Jnt")
        self.addOffset = QPushButton("_Offset")
        self.addSkin = QPushButton("_Skin")
        self.addDrv = QPushButton("_Drv")
        self.pushB2 = QPushButton(u"替换")
        self.pushB2.setFixedHeight(40)

        self.pushB1.setStyleSheet(qss1)
        self.addGrp.setStyleSheet(qss2)
        self.addCtrl.setStyleSheet(qss2)
        self.addJnt.setStyleSheet(qss2)
        self.addOffset.setStyleSheet(qss2)
        self.addSkin.setStyleSheet(qss2)
        self.addDrv.setStyleSheet(qss2)
        self.pushB2.setStyleSheet(qss1)

    def _createConnect(self):
        """
        连接
        Returns:

        """
        self.pushB1.clicked.connect(self._reName)
        self.addGrp.clicked.connect(partial(addSuffix, "_Grp"))
        self.addCtrl.clicked.connect(partial(addSuffix, "_Ctrl"))
        self.addJnt.clicked.connect(partial(addSuffix, "_Jnt"))
        self.addOffset.clicked.connect(partial(addSuffix, "_Offset"))
        self.addSkin.clicked.connect(partial(addSuffix, "_Skin"))
        self.addDrv.clicked.connect(partial(addSuffix, "_Drv"))
        self.linePBtn1.button.clicked.connect(self._addP)
        self.linePBtn2.button.clicked.connect(self._addS)
        self.pushB2.clicked.connect(self._replaceN)

    def _reName(self):
        """
        重命名
        Returns:

        """
        num = int(self.numItems.currentText())
        newName = self.lineE1.text()
        renameNum(num, newName)

    def _addP(self):
        """
        添加前缀
        Returns:

        """
        text = self.linePBtn1.getText()
        addPrefix(text)

    def _addS(self):
        """
        添加后缀
        Returns:

        """
        text = self.linePBtn2.getText()
        addSuffix(text)

    def _replaceN(self):
        """
        搜索替换
        Returns:

        """
        getID = self.checkGroup.checkedId()
        search = self.lineE3.text()
        replace = self.lineE4.text()
        replaceName(search, replace, getID)

    def _createLayout(self):
        """
        布局
        """
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(10, 5, 10, 10)
        self.setLayout(self.mainLayout)

        self.mainLayout.addWidget(self.splitter1)

        self.hbLayout1 = QHBoxLayout()
        self.mainLayout.addLayout(self.hbLayout1)
        self.hbLayout1.addWidget(self.label1, 1)
        self.hbLayout1.addWidget(self.lineE1, 4)
        self.hbLayout1.addWidget(self.label2, 1)
        self.hbLayout1.addWidget(self.numItems, 2)

        self.mainLayout.addSpacing(5)
        self.mainLayout.addWidget(self.pushB1)
        self.mainLayout.addWidget(self.splitter2)

        self.gridLayout1 = QGridLayout()
        self.mainLayout.addLayout(self.gridLayout1)
        self.gridLayout1.addWidget(self.addGrp, 0, 0)
        self.gridLayout1.addWidget(self.addCtrl, 0, 1)
        self.gridLayout1.addWidget(self.addJnt, 0, 2)
        self.gridLayout1.addWidget(self.addOffset, 0, 3)
        self.gridLayout1.addWidget(self.addSkin, 1, 0)
        self.gridLayout1.addWidget(self.addDrv, 1, 1)

        self.mainLayout.addWidget(self.splitter3)

        self.mainLayout.addWidget(self.linePBtn1)
        self.mainLayout.addWidget(self.linePBtn2)

        self.mainLayout.addWidget(self.splitter4)

        self.gridLayout2 = QGridLayout()
        self.mainLayout.addLayout(self.gridLayout2)
        self.gridLayout2.addWidget(self.label3, 0, 0)
        self.gridLayout2.addWidget(self.lineE3, 0, 1)
        self.gridLayout2.addWidget(self.label4, 1, 0)
        self.gridLayout2.addWidget(self.lineE4, 1, 1)

        self.mainLayout.addSpacing(5)
        self.hbLayout2 = QHBoxLayout()
        self.mainLayout.addLayout(self.hbLayout2)
        self.hbLayout2.addWidget(self.checkB1)
        self.hbLayout2.addWidget(self.checkB2)
        self.hbLayout2.addWidget(self.checkB3)
        self.hbLayout2.setAlignment(self.checkB1, Qt.AlignHCenter)
        self.hbLayout2.setAlignment(self.checkB2, Qt.AlignHCenter)
        self.hbLayout2.setAlignment(self.checkB3, Qt.AlignHCenter)

        self.mainLayout.addWidget(self.pushB2)


def checkDuplicateName(obj):
    """
    检测是否有重复名称，并返回短名
    Args:
        obj:给定名称

    Returns:短名

    """
    try:
        trueName = obj.split("|")
        return trueName[len(trueName) - 1]
    except:
        return obj


def renameNum(num, newName):
    """
    重命名
    Args:
        num: 位数
        newName: 名称

    Returns:

    """
    selection = cmds.ls(sl = True)
    number = 1
    for sel in selection:
        name = "{0}_{1:0>{2}}".format(newName, number, num)
        cmds.rename(sel, name)
        number += 1


def addSuffix(text):
    """
    添加后缀
    Args:
        text: 文本

    Returns:

    """
    selection = cmds.ls(sl = True, sn = True)
    for sel in selection:
        trueName = checkDuplicateName(sel)
        newName = trueName + text
        try:
            cmds.rename(sel, newName)
        except:
            pass


def addPrefix(text):
    """
    添加前缀
    Args:
        text: 文本

    Returns:

    """
    selection = cmds.ls(sl = True, sn = True)
    for sel in selection:
        trueName = checkDuplicateName(sel)
        newName = text + trueName
        try:
            cmds.rename(sel, newName)
        except:
            pass


def replaceName(*args):
    """

    Args:
        *args: search,replace:替换文本，getID:替换对象

    Returns:

    """
    search, replace, getID = args
    if getID == 1:
        selection = cmds.ls(sl = True, sn = True)
    if getID == 2:
        cmds.select(hi = True)
        selection = cmds.ls(sl = True, sn = True)
    if getID == 3:
        cmds.select(ado = True, hi = True)
        selection = cmds.ls(sl = True, sn = True)
    for sel in selection:
        trueName = checkDuplicateName(sel)
        newName = trueName.replace(search, replace)
        try:
            cmds.rename(sel, newName)
        except:
            pass
