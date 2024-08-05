# -*- coding: UTF-8 -*-
# @FileName      : rigEZikfk
# @Time          : 2024-06-26
# @Author        : LJF
# @Contact       : 906629272@qq.com
"""
创建简易的IKFK
"""
import maya.cmds as cmds
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from . import uiWidget

crv_points = [(-1, 1, -1), (-1, -1, -1), (-1, -1, 1), (1, -1, 1), (1, -1, -1),
              (-1, -1, -1), (-1, 1, -1), (-1, 1, 1), (-1, -1, 1), (-1, 1, 1),
              (1, 1, 1),
              (1, -1, 1), (1, -1, -1), (1, 1, -1), (1, 1, 1), (1, 1, -1),
              (-1, 1, -1)]
crv_knots = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
crv_degree = 1


def undo(fun):
    u"""
    回撤
    """

    def undo_fun(*args, **kwargs):
        # 打开undo
        cmds.undoInfo(ock = True)
        # 记录选择物体
        long_names = cmds.ls(sl = 1, l = 1)
        fun(*args, **kwargs)
        # 保持选择物体
        cmds.select(cmds.ls(long_names))
        # 关闭undo
        cmds.undoInfo(cck = True)

    return undo_fun


class EzIkFkUI(QWidget):
    """
    控制创建工具面板
    """

    def __init__(self):
        QWidget.__init__(self)
        self.setObjectName("EzIkFkWindow")
        self.getSelf = None
        self.fk = False
        self.ik = False
        self.fkCon = []
        self.ikCon = []

        self._createLabel()
        # self._createLineEdit()
        self._createPushButton()
        self._connectCommand()
        self._createSplitter()
        self._createLayout()

    def _createLabel(self):
        """
        标签
        :return:
        """
        qss = "color: rgb(228, 224, 217); font: bold 10pt Microsoft YaHei;"
        self.description_label = QLabel(u"沿着按钮往下点, 创建ADV的FK控制效果, 还可添加简易IK效果")
        self.description_label.setStyleSheet(qss)
        # gif
        # self.gif_label = QLabel()
        # gif_movie = QMovie(__file__ + "/../res/images/important.gif")
        # gif_movie.setScaledSize(self.gif_label.size())
        # self.gif_label.setMovie(gif_movie)
        # gif_movie.start()

    def _createPushButton(self):
        """
        按钮
        :return:
        """
        with open(__file__ + "/../res/qss/QPushButtonA.qss", "r") as f:
            qss = f.read()
        self.createPB = QPushButton(u"创建")
        self.createPB.setFixedHeight(35)
        self.createADCfk = QPushButton(u"创建ADVfk控制效果")
        self.createADCfk.setFixedHeight(35)
        self.createEZik = QPushButton(u"添加简易IK效果")
        self.createEZik.setFixedHeight(35)
        self.selectFK = QPushButton(u"选择FK控制器")
        self.selectFK.setFixedHeight(35)
        self.selectIK = QPushButton(u"选择IK控制器")
        self.selectIK.setFixedHeight(35)
        self.createPB.setStyleSheet(qss)
        self.createADCfk.setStyleSheet(qss)
        self.createEZik.setStyleSheet(qss)
        self.selectFK.setStyleSheet(qss)
        self.selectIK.setStyleSheet(qss)

    def _commandCreateCV(self):
        """

        :return:
        """
        self.getSelf = createCon()
        self.fk = True
        self.fkCon = []
        self.ikCon = []

    def _commandCreateADVfk(self):
        """

        :return:
        """
        if self.fk:
            self.getSelf.createADVfk()
            self.fk = False
            self.ik = True
            self.fkCon = self.getSelf.listCtrl
        else:
            return 0

    def _commandCreateEZik(self):
        """

        :return:
        """
        if self.ik:
            self.getSelf.createEZik()
            self.ik = False
            self.ikCon = self.getSelf.listIkCtrl
        else:
            return 0

    def _connectCommand(self):
        """
        信号连接
        :return:
        """
        self.createPB.clicked.connect(self._commandCreateCV)
        self.createADCfk.clicked.connect(self._commandCreateADVfk)
        self.createEZik.clicked.connect(self._commandCreateEZik)
        self.selectFK.clicked.connect(lambda x: cmds.select(self.fkCon))
        self.selectIK.clicked.connect(lambda x: cmds.select(self.ikCon))

    def _createSplitter(self):
        """
        分割线
        """
        self.splitter1 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)
        self.splitter2 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)
        self.splitter3 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)
        self.splitter4 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)
        self.splitter5 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)
        self.splitter6 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)

    def _createLayout(self):
        """
        布局
        :return:
        """
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.splitter1)
        self.mainLayout.addWidget(self.description_label)
        self.mainLayout.setAlignment(self.description_label, Qt.AlignHCenter)
        self.mainLayout.addWidget(self.splitter2)

        self.mainLayout.addWidget(self.createPB)
        self.mainLayout.addWidget(self.splitter3)
        self.mainLayout.addWidget(self.createADCfk)
        self.mainLayout.addWidget(self.splitter4)
        self.mainLayout.addWidget(self.createEZik)
        self.mainLayout.addWidget(self.splitter5)

        self.hboxLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.hboxLayout)
        self.hboxLayout.addWidget(self.selectFK)
        self.hboxLayout.addWidget(self.selectIK)
        # gif
        self.mainLayout.addWidget(self.splitter6)
        # self.mainLayout.addWidget(self.gif_label)
        # self.mainLayout.setAlignment(self.gif_label, Qt.AlignHCenter)
        # 布局末端添加一个空项，将所有子部件往上挤
        self.mainLayout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.Expanding))


def getSelectionList():
    """
    获取选择列表
    :return: sel
    """
    sel = cmds.ls(sl = True, type = "joint") or []
    if len(sel) != 1:
        cmds.error(u"选择一个骨骼")
    else:
        return sel[0]


def createCtrlC(name):
    """
    创建曲线
    :param name: 曲线名
    :return: 曲线名
    """
    cvName = cmds.curve(name = name, d = crv_degree, k = crv_knots, p = crv_points)
    cmds.rename(cmds.listRelatives(cvName, s = True)[0], name + "Shape")
    return cvName


def createCon():
    """
    创建曲线
    :return: self
    """
    joint = getSelectionList()
    ikFk = IKFKTool()
    ikFk.createCV(joint)
    return ikFk


class IKFKTool(object):
    """
    创建工具
    """

    def __init__(self):
        """

        :param seleJnt: 所选骨骼
        """
        self.conSel = []
        self.listOffset = []
        self.listDrv = []
        self.listCtrl = []
        self.listJoint = []
        self.listSJoint = []
        self.listPs1 = []
        self.listPs2 = []
        self.listIkCtrl = []
        self.selectJoint = []
        self.sideName = ["_L", "_l", "_left", "_Left", "_R", "_r", "_right", "_Right"]

    @undo
    def createCV(self, joint = None, parent = None):
        """
        创建曲线
        :param joint: 骨骼
        :param parent: 父级
        :return: self
        """
        try:
            longest = ""
            for s in self.sideName:
                if s in joint and len(s) > len(longest):
                    longest = s
            if len(longest) > 0:
                side = longest
            name = joint.replace(side, "")
            offset = "{0}_{1}".format(name, "Offset" + side)
            drv = "{0}_{1}".format(name, "Drv" + side)
            con = "{0}_{1}".format(name, "Con" + side)
            jnt = "{0}_{1}".format(name, "CJnt" + side)
        except NameError:
            name = joint
            offset = "{0}_{1}".format(name, "Offset")
            drv = "{0}_{1}".format(name, "Drv")
            con = "{0}_{1}".format(name, "Con")
            jnt = "{0}_{1}".format(name, "CJnt")
        # print(name)
        self.listOffset.append(
            cmds.createNode("transform", name = offset))
        self.listDrv.append(
            cmds.createNode("transform", name = drv))
        self.listCtrl.append(createCtrlC(name = con))
        self.listJoint.append(cmds.joint(con, n = jnt))
        self.selectJoint.append(joint)
        cmds.setAttr(jnt + ".drawStyle", 2)
        cmds.parent(con, drv)
        cmds.parent(drv, offset)
        cmds.matchTransform(offset, joint, pos = True, rot = True)
        try:
            cmds.parent(offset, parent)
        except:
            pass
        children = cmds.listRelatives(joint, c = True, type = "joint") or []
        for j in children:
            if len(cmds.listRelatives(j, c = True, type = "joint") or []) == 0:
                continue
            else:
                self.createCV(joint = j, parent = jnt)

    @undo
    def createADVfk(self):
        """

        :return: self
        """
        psIndex = 0
        for index, o in enumerate(self.listOffset):
            cmds.connectAttr(self.listCtrl[index] + ".scale", self.listJoint[index] + ".inverseScale")
            cmds.parentConstraint(self.listJoint[index], self.selectJoint[index], mo = True, weight = 1)
            cmds.connectAttr(self.listCtrl[index] + ".scale", self.selectJoint[index] + ".scale")
            ctran = cmds.listRelatives(self.listJoint[index], c = True, type = "transform") or []
            ctran = [ct for ct in ctran if not "PS" in ct]
            if len(cmds.listRelatives(self.listJoint[index], c = True, type = "transform") or []) == 0:
                continue
            elif len(ctran) > 1:
                for t in ctran:
                    self.listPs1.append(cmds.createNode("transform", n = t.replace("Offset", "PS1")))
                    self.listPs2.append(
                        cmds.createNode("transform", n = t.replace("Offset", "PS2"),
                                        p = self.listPs1[psIndex]))
                    cmds.xform(self.listPs1[psIndex], ws = True,
                               m = cmds.xform(self.listCtrl[index], q = True, ws = True, m = True))
                    cmds.xform(self.listPs2[psIndex], ws = True,
                               m = cmds.xform(t, q = True, ws = True, m = True))
                    cmds.parent(self.listPs1[psIndex], self.listJoint[index])
                    cmds.scaleConstraint(self.listCtrl[index], self.listPs1[psIndex], mo = True, weight = 1)
                    cmds.pointConstraint(self.listPs2[psIndex], t, mo = True, weight = 1)
                    psIndex += 1
            else:
                self.listPs1.append(cmds.createNode("transform", n = self.listCtrl[index + 1].replace("Con", "PS1")))
                self.listPs2.append(
                    cmds.createNode("transform", n = self.listCtrl[index + 1].replace("Con", "PS2"),
                                    p = self.listPs1[psIndex]))
                cmds.xform(self.listPs1[psIndex], ws = True,
                           m = cmds.xform(self.listCtrl[index], q = True, ws = True, m = True))
                cmds.xform(self.listPs2[psIndex], ws = True,
                           m = cmds.xform(self.listCtrl[index + 1], q = True, ws = True, m = True))
                cmds.parent(self.listPs1[psIndex], self.listJoint[index])
                cmds.scaleConstraint(self.listCtrl[index], self.listPs1[psIndex], mo = True, weight = 1)
                cmds.pointConstraint(self.listPs2[psIndex], self.listOffset[index + 1], mo = True, weight = 1)
                psIndex += 1

    @undo
    def createEZik(self):
        """

        :return: self
        """
        jIndex = 0
        parent = [cmds.listRelatives(p1, p = True, type = "joint")[0] for p1 in self.listPs1]
        for index in range(len(self.listPs1)):
            if index != 0:
                if cmds.objExists(parent[index].replace("CJnt", "IKCon")):
                    continue
            self.listSJoint.append(
                cmds.joint(parent[index].replace("CJnt", "Con"), n = self.listPs1[index].replace("PS1", "SJnt")))
            cmds.setAttr(self.listSJoint[jIndex] + ".drawStyle", 2)
            cmds.connectAttr(parent[index].replace("CJnt", "Con") + ".scale", self.listSJoint[jIndex] + ".inverseScale")
            try:
                cmds.disconnectAttr(parent[index].replace("CJnt", "Con") + ".scale", parent[index] + ".inverseScale")
            except RuntimeError:
                pass
            self.listIkCtrl.append(
                cmds.circle(nr = [0, 1, 0], sweep = 360, n = parent[index].replace("CJnt", "IKCon"))[0])
            cmds.setAttr(self.listIkCtrl[jIndex] + ".sx", l = True, k = False, cb = False)
            cmds.setAttr(self.listIkCtrl[jIndex] + ".sy", l = True, k = False, cb = False)
            cmds.setAttr(self.listIkCtrl[jIndex] + ".sz", l = True, k = False, cb = False)
            grp = cmds.createNode("transform", n = parent[index].replace("CJnt", "IKCon_Grp"))
            offset = cmds.createNode("transform", n = parent[index].replace("CJnt", "IKCon_Offset"), p = grp)
            cmds.parent(self.listIkCtrl[jIndex], offset)
            cmds.parent(grp, parent[index].replace("CJnt", "Con"))
            cmds.xform(grp, ws = False, m = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
            cmds.parent(cmds.listRelatives(parent[index], c = True), self.listSJoint[jIndex])
            cmds.parent(parent[index], self.listIkCtrl[jIndex])
            jIndex += 1
