# -*- coding: UTF-8 -*-
# @FileName      : EZtoolW
# @Time          : 2024-04-07
# @Author        : LJF
# @Contact       : 906629272@qq.com

from functools import partial

import maya.cmds as cmds
from . import uiWidget
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from maya.OpenMaya import *


class CHtoolUI(QWidget):
    """
    窗口界面
    """
    item = [u"匹配变换", u"约束", u"矩阵约束", u"父子关系", u"复制权重", u"shape替换", u"材质传递", u"BS连接",
            u"BS拷贝", u"属性连接"]

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setObjectName("CHToolWin")

        self._createCBWidgets()
        self._createPushBtn()
        self._createLWidgets()
        self._createCheckbox()
        self._createConnect()
        self._createLayouts()

        self._initUI()

    def _createCBWidgets(self):
        """
        下拉框
        :return:
        """
        self.switch_items = QComboBox()
        self.switch_items.addItems(self.item)

    def _createPushBtn(self):
        """
        按钮
        :return:
        """
        qss = """QPushButton {
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
        self.select_left = QPushButton("OutP")
        self.select_right = QPushButton("InP")
        self.apply_btn = QPushButton(u"执行")
        self.apply_btn.setFixedHeight(40)
        self.apply_btn.setStyleSheet(qss)

    def _createLWidgets(self):
        """
        选择列表
        :return:
        """
        self.select_listl = QListWidget()
        self.select_listl.setDragDropMode(QListWidget.InternalMove)
        self.select_listr = QListWidget()
        self.select_listr.setDragDropMode(QListWidget.InternalMove)

        # self.select_listl.addItems(["test1", "test2", "test3", "test4", "test5"])

    def _createCheckbox(self):
        """
        滑动按钮
        :return:
        """
        self.match_translation_sbtn = uiWidget.TextSliderBtnE(w = 40, h = 20, text = "translation")
        self.match_rotation_sbtn = uiWidget.TextSliderBtnE(w = 40, h = 20, text = "rotation")

        self.parent_sbtn = uiWidget.TextSliderBtnE(w = 40, h = 20, text = u"父子")
        self.scale_sbtn = uiWidget.TextSliderBtnE(w = 40, h = 20, text = u"缩放")
        self.offset_constrain = uiWidget.TextSliderBtnE(w = 40, h = 20, text = u"是否偏移")

        self.offset_matrix = uiWidget.TextSliderBtnE(w = 40, h = 20, text = u"是否偏移")

        self.cop_blendshape = uiWidget.TextSliderBtnE(w = 40, h = 20, text = "DeltaMush")

        self.connect_attr_tx = uiWidget.TextSliderBtnE(w = 40, h = 20, text = "Tx")
        self.connect_attr_ty = uiWidget.TextSliderBtnE(w = 40, h = 20, text = "Ty")
        self.connect_attr_tz = uiWidget.TextSliderBtnE(w = 40, h = 20, text = "Tz")
        self.connect_attr_rx = uiWidget.TextSliderBtnE(w = 40, h = 20, text = "Rx")
        self.connect_attr_ry = uiWidget.TextSliderBtnE(w = 40, h = 20, text = "Ry")
        self.connect_attr_rz = uiWidget.TextSliderBtnE(w = 40, h = 20, text = "Rz")
        self.connect_attr_sx = uiWidget.TextSliderBtnE(w = 40, h = 20, text = "Sx")
        self.connect_attr_sy = uiWidget.TextSliderBtnE(w = 40, h = 20, text = "Sy")
        self.connect_attr_sz = uiWidget.TextSliderBtnE(w = 40, h = 20, text = "Sz")

        # self.parent_Hierarchy_oto = uiWidget.TextSliderBtnE(w = 40, h = 20, text = u"一对一")
        # self.parent_Hierarchy_otm = uiWidget.TextSliderBtnE(w = 40, h = 20, text = u"一对多")

    def _parentConstrainBtnSet(self):
        """
        设置约束按钮的状态
        :return:
        """
        if self.parent_sbtn.btn.getChecked():
            self.scale_sbtn.btn.setChecked(False)

    def _scaleConstrainBtnSet(self):
        """
        设置约束按钮的状态
        :return:
        """
        if self.scale_sbtn.btn.getChecked():
            self.parent_sbtn.btn.setChecked(False)

    # def _hierarchyOtoBtnSet(self):
    #     """
    #     设置约束按钮的状态
    #     :return:
    #     """
    #     if self.parent_Hierarchy_oto.btn.getChecked():
    #         self.parent_Hierarchy_otm.btn.setChecked(False)

    # def _hierarchyOtmBtnSet(self):
    #     """
    #     设置约束按钮的状态
    #     :return:
    #     """
    #     if self.parent_Hierarchy_otm.btn.getChecked():
    #         self.parent_Hierarchy_oto.btn.setChecked(False)

    def _visAuto(self, index):
        """
        隐藏控件
        :return:
        """
        if index == 0:
            self.match_translation_sbtn.setVisible(True)
            self.match_rotation_sbtn.setVisible(True)

            self.parent_sbtn.setVisible(False)
            self.scale_sbtn.setVisible(False)
            self.offset_constrain.setVisible(False)
            self.offset_matrix.setVisible(False)
            self.offset_constrain.setVisible(False)
            self.connect_attr_tx.setVisible(False)
            self.connect_attr_ty.setVisible(False)
            self.connect_attr_tz.setVisible(False)
            self.connect_attr_rx.setVisible(False)
            self.connect_attr_ry.setVisible(False)
            self.connect_attr_rz.setVisible(False)
            self.connect_attr_sx.setVisible(False)
            self.connect_attr_sy.setVisible(False)
            self.connect_attr_sz.setVisible(False)
            self.cop_blendshape.setVisible(False)
            # self.parent_Hierarchy_oto.setVisible(False)
            # self.parent_Hierarchy_otm.setVisible(False)
        elif index == 1:
            self.parent_sbtn.setVisible(True)
            self.scale_sbtn.setVisible(True)
            self.offset_constrain.setVisible(True)

            self.match_translation_sbtn.setVisible(False)
            self.match_rotation_sbtn.setVisible(False)
            self.offset_matrix.setVisible(False)
            self.connect_attr_tx.setVisible(False)
            self.connect_attr_ty.setVisible(False)
            self.connect_attr_tz.setVisible(False)
            self.connect_attr_rx.setVisible(False)
            self.connect_attr_ry.setVisible(False)
            self.connect_attr_rz.setVisible(False)
            self.connect_attr_sx.setVisible(False)
            self.connect_attr_sy.setVisible(False)
            self.connect_attr_sz.setVisible(False)
            self.cop_blendshape.setVisible(False)
            # self.parent_Hierarchy_oto.setVisible(False)
            # self.parent_Hierarchy_otm.setVisible(False)
        elif index == 2:
            self.offset_matrix.setVisible(True)

            self.match_translation_sbtn.setVisible(False)
            self.match_rotation_sbtn.setVisible(False)
            self.parent_sbtn.setVisible(False)
            self.scale_sbtn.setVisible(False)
            self.offset_constrain.setVisible(False)
            self.offset_constrain.setVisible(False)
            self.connect_attr_tx.setVisible(False)
            self.connect_attr_ty.setVisible(False)
            self.connect_attr_tz.setVisible(False)
            self.connect_attr_rx.setVisible(False)
            self.connect_attr_ry.setVisible(False)
            self.connect_attr_rz.setVisible(False)
            self.connect_attr_sx.setVisible(False)
            self.connect_attr_sy.setVisible(False)
            self.connect_attr_sz.setVisible(False)
            self.cop_blendshape.setVisible(False)
            # self.parent_Hierarchy_oto.setVisible(False)
            # self.parent_Hierarchy_otm.setVisible(False)
        elif index == 8:
            self.cop_blendshape.setVisible(True)

            self.offset_matrix.setVisible(False)
            self.match_translation_sbtn.setVisible(False)
            self.match_rotation_sbtn.setVisible(False)
            self.parent_sbtn.setVisible(False)
            self.scale_sbtn.setVisible(False)
            self.offset_constrain.setVisible(False)
            self.offset_constrain.setVisible(False)
            self.connect_attr_tx.setVisible(False)
            self.connect_attr_ty.setVisible(False)
            self.connect_attr_tz.setVisible(False)
            self.connect_attr_rx.setVisible(False)
            self.connect_attr_ry.setVisible(False)
            self.connect_attr_rz.setVisible(False)
            self.connect_attr_sx.setVisible(False)
            self.connect_attr_sy.setVisible(False)
            self.connect_attr_sz.setVisible(False)
        elif index == 9:
            self.connect_attr_tx.setVisible(True)
            self.connect_attr_ty.setVisible(True)
            self.connect_attr_tz.setVisible(True)
            self.connect_attr_rx.setVisible(True)
            self.connect_attr_ry.setVisible(True)
            self.connect_attr_rz.setVisible(True)
            self.connect_attr_sx.setVisible(True)
            self.connect_attr_sy.setVisible(True)
            self.connect_attr_sz.setVisible(True)

            self.offset_matrix.setVisible(False)
            self.match_translation_sbtn.setVisible(False)
            self.match_rotation_sbtn.setVisible(False)
            self.parent_sbtn.setVisible(False)
            self.scale_sbtn.setVisible(False)
            self.offset_constrain.setVisible(False)
            self.cop_blendshape.setVisible(False)
        else:
            # self.parent_Hierarchy_oto.setVisible(False)
            # self.parent_Hierarchy_otm.setVisible(False)
            self.offset_matrix.setVisible(False)
            self.match_translation_sbtn.setVisible(False)
            self.match_rotation_sbtn.setVisible(False)
            self.parent_sbtn.setVisible(False)
            self.scale_sbtn.setVisible(False)
            self.offset_constrain.setVisible(False)
            self.connect_attr_tx.setVisible(False)
            self.connect_attr_ty.setVisible(False)
            self.connect_attr_tz.setVisible(False)
            self.connect_attr_rx.setVisible(False)
            self.connect_attr_ry.setVisible(False)
            self.connect_attr_rz.setVisible(False)
            self.connect_attr_sx.setVisible(False)
            self.connect_attr_sy.setVisible(False)
            self.connect_attr_sz.setVisible(False)
            self.cop_blendshape.setVisible(False)

    def _initUI(self):
        """
        初始化控件状态
        :return:
        """
        self.parent_sbtn.setVisible(False)
        self.scale_sbtn.setVisible(False)
        self.offset_constrain.setVisible(False)
        self.offset_matrix.setVisible(False)
        self.connect_attr_tx.setVisible(False)
        self.connect_attr_ty.setVisible(False)
        self.connect_attr_tz.setVisible(False)
        self.connect_attr_rx.setVisible(False)
        self.connect_attr_ry.setVisible(False)
        self.connect_attr_rz.setVisible(False)
        self.connect_attr_sx.setVisible(False)
        self.connect_attr_sy.setVisible(False)
        self.connect_attr_sz.setVisible(False)
        self.cop_blendshape.setVisible(False)
        # self.parent_Hierarchy_oto.setVisible(False)
        # self.parent_Hierarchy_otm.setVisible(False)

    def _createConnect(self):
        """
        信号连接
        :return:
        """
        self.select_left.clicked.connect(partial(self._addSelect, "l"))
        self.select_right.clicked.connect(partial(self._addSelect, "r"))
        self.switch_items.currentIndexChanged.connect(self._visAuto)

        self.parent_sbtn.btn.toggled.connect(self._parentConstrainBtnSet)
        self.scale_sbtn.btn.toggled.connect(self._scaleConstrainBtnSet)

        self.apply_btn.clicked.connect(self.rootConnect)

        self.select_listl.itemDoubleClicked.connect(self._selectListItem)
        self.select_listr.itemDoubleClicked.connect(self._selectListItem)

        # self.parent_Hierarchy_oto.btn.toggled.connect(self._hierarchyOtoBtnSet)
        # self.parent_Hierarchy_otm.btn.toggled.connect(self._hierarchyOtmBtnSet)

    def testFun(self):
        print(self.switch_items.count())

    def _selectListItem(self, item):
        """
        双击选择对应的对象
        :param item:
        :return:
        """
        cmds.select(cl = True)
        cmds.select(item.text())

    def rootConnect(self):
        """
        执行功能
        :return:
        """
        out_list = []
        in_list = []
        index = self.switch_items.currentIndex()
        for idx in range(self.select_listl.count()):
            out_list.append(self.select_listl.item(idx).text())
        for idx in range(self.select_listr.count()):
            in_list.append(self.select_listr.item(idx).text())
        if index == 0:
            self._matchTransformConnect(out_list, in_list)
        elif index == 1:
            self._constrainConnect(out_list, in_list)
        elif index == 2:
            self._matrixConnect(out_list, in_list)
        elif index == 3:
            hierarchyConnect(out_list, in_list)
        elif index == 4:
            self._copSkinConnect(out_list, in_list)
        elif index == 5:
            self._replaceMeshConnect(out_list, in_list)
        elif index == 6:
            self._transmitShadingSets(out_list, in_list)
        elif index == 7:
            self._copBSConnect(out_list, in_list)
        elif index == 8:
            self._copBlendShape(out_list, in_list)
        elif index == 9:
            self._connectAttrConnect(out_list, in_list)

    def _matchTransformConnect(self, out_list, in_list):
        """
        匹配变换连接
        :param out_list:
        :param in_list:
        :return:
        """
        cmds.undoInfo(ock = True)
        if not self.match_translation_sbtn.btn.getChecked() and not self.match_rotation_sbtn.btn.getChecked():
            return 0
        if len(out_list) == 0 or len(in_list) == 0:
            return cmds.warning(u"请加载对象!")
        elif len(out_list) == 1 and len(in_list) > 0:
            for r in in_list:
                matchTransform(out_list[0], r, self.match_translation_sbtn.btn.getChecked(),
                               self.match_rotation_sbtn.btn.getChecked())
        elif len(out_list) == len(in_list):
            for l, r in zip(out_list, in_list):
                matchTransform(l, r, self.match_translation_sbtn.btn.getChecked(),
                               self.match_rotation_sbtn.btn.getChecked())
        else:
            return cmds.warning(u"请保持两边加载数量一致，或左边只加载一个!")
        cmds.undoInfo(cck = True)

    def _constrainConnect(self, out_list, in_list):
        """
        约束
        :param out_list:
        :param in_list:
        :return:
        """
        cmds.undoInfo(ock = True)
        if not self.parent_sbtn.btn.getChecked() and not self.scale_sbtn.btn.getChecked():
            return 0
        if len(out_list) == 0 or len(in_list) == 0:
            return cmds.warning(u"请加载对象!")
        elif len(out_list) == 1 and len(in_list) > 0:
            for r in in_list:
                constrainFun(out_list[0], r, self.parent_sbtn.btn.getChecked(), self.scale_sbtn.btn.getChecked(),
                             self.offset_constrain.btn.getChecked())
        elif len(out_list) == len(in_list):
            for l, r in zip(out_list, in_list):
                constrainFun(l, r, self.parent_sbtn.btn.getChecked(), self.scale_sbtn.btn.getChecked(),
                             self.offset_constrain.btn.getChecked())
        elif len(out_list) > len(in_list) == 1:
            for l in out_list:
                constrainFun(l, in_list[0], self.parent_sbtn.btn.getChecked(), self.scale_sbtn.btn.getChecked(),
                             self.offset_constrain.btn.getChecked())
        else:
            return cmds.warning(u"请保持两边加载数量一致，或左边或右边只加载一个!")
        cmds.undoInfo(cck = True)

    def _matrixConnect(self, out_list, in_list):
        """
        矩阵约束
        :param out_list:
        :param in_list:
        :return:
        """
        cmds.undoInfo(ock = True)
        if len(out_list) == 0 or len(in_list) == 0:
            return cmds.warning(u"请加载对象!")
        elif len(out_list) == 1 and len(in_list) > 0:
            for r in in_list:
                matrixConFun(out_list, [r], False, self.offset_matrix.btn.getChecked())
        elif len(out_list) == len(in_list):
            matrixConFun(out_list, in_list, False, self.offset_matrix.btn.getChecked())
        elif len(out_list) > len(in_list) == 1:
            matrixConFun(out_list, in_list, True, self.offset_matrix.btn.getChecked())
        else:
            return cmds.warning(u"请保持两边加载数量一致，或左边或右边只加载一个!")
        cmds.undoInfo(cck = True)

    def _copSkinConnect(self, out_list, in_list):
        """
        复制权重
        :param out_list:
        :param in_list:
        :return:
        """
        cmds.undoInfo(ock = True)
        if len(out_list) == 0 or len(in_list) == 0:
            return cmds.warning(u"请加载对象!")
        elif len(out_list) == 1 and len(in_list) > 0:
            for r in in_list:
                copSkin(out_list[0], r)
        elif len(out_list) == len(in_list):
            for l, r in zip(out_list, in_list):
                copSkin(l, r)
        else:
            return cmds.warning(u"请保持两边加载数量一致，或左边只加载一个!")
        cmds.undoInfo(cck = True)

    def _replaceMeshConnect(self, out_list, in_list):
        """
        替换模型shape
        :param out_list:
        :param in_list:
        :return:
        """
        cmds.undoInfo(ock = True)
        if len(out_list) == 0 or len(in_list) == 0:
            return cmds.warning(u"请加载对象!")
        elif len(out_list) == len(in_list):
            for l, r in zip(out_list, in_list):
                replaceTransferBsMesh(l, r)
        else:
            return cmds.warning(u"请保持两边加载数量一致!")
        cmds.undoInfo(cck = True)

    def _transmitShadingSets(self, out_list, in_list):
        """
        传递材质
        :param out_list:
        :param in_list:
        :return:
        """
        cmds.undoInfo(ock = True)
        if len(out_list) == 0 or len(in_list) == 0:
            return cmds.warning(u"请加载对象!")
        elif len(out_list) == 1 and len(in_list) > 0:
            for rm in in_list:
                cmds.select(out_list[0], r = True)
                cmds.select(rm, tgl = True)
                cmds.transferShadingSets(sampleSpace = 0, searchMethod = 3)
                cmds.select(cl = True)
        elif len(out_list) == len(in_list):
            for lm, rm in zip(out_list, in_list):
                cmds.select(lm, r = True)
                cmds.select(rm, tgl = True)
                cmds.transferShadingSets(sampleSpace = 0, searchMethod = 3)
                cmds.select(cl = True)
        else:
            return cmds.warning(u"请保持两边加载数量一致，或左边只加载一个!")
        cmds.undoInfo(cck = True)

    def _copBSConnect(self, out_list, in_list):
        """
        BS连接
        :param out_list:
        :param in_list:
        :return:
        """
        cmds.undoInfo(ock = True)
        if len(out_list) == 0 or len(in_list) == 0:
            return cmds.warning(u"请加载对象!")
        elif len(out_list) == 1 and len(in_list) > 0:
            for rm in in_list:
                copBlendShapeConnect(out_list[0], rm)
        elif len(out_list) == len(in_list):
            for lm, rm in zip(out_list, in_list):
                copBlendShapeConnect(lm, rm)
        else:
            return cmds.warning(u"请保持两边加载数量一致，或左边只加载一个!")
        cmds.undoInfo(cck = True)

    def _copBlendShape(self, out_list, in_list):
        """
        拷贝BS
        :param out_list:
        :param in_list:
        :return:
        """
        cmds.undoInfo(ock = True)
        if len(out_list) == 0 or len(in_list) == 0:
            return cmds.warning(u"请加载对象!")
        elif len(out_list) == 1 and len(in_list) > 0:
            for rm in in_list:
                wrapConvertBlendShape(out_list[0], rm, dm = self.cop_blendshape.btn.getChecked())
        elif len(out_list) == len(in_list):
            for lm, rm in zip(out_list, in_list):
                wrapConvertBlendShape(lm, rm, dm = self.cop_blendshape.btn.getChecked())
        else:
            return cmds.warning(u"请保持两边加载数量一致，或左边只加载一个!")
        cmds.undoInfo(cck = True)

    def _connectAttrConnect(self, out_list, in_list):
        """
        连接属性
        :param out_list:
        :param in_list:
        :return:
        """
        cmds.undoInfo(ock = True)
        list_trs = []
        tx = self.connect_attr_tx.btn.getChecked()
        ty = self.connect_attr_ty.btn.getChecked()
        tz = self.connect_attr_tz.btn.getChecked()
        rx = self.connect_attr_rx.btn.getChecked()
        ry = self.connect_attr_ry.btn.getChecked()
        rz = self.connect_attr_rz.btn.getChecked()
        sx = self.connect_attr_sx.btn.getChecked()
        sy = self.connect_attr_sy.btn.getChecked()
        sz = self.connect_attr_sz.btn.getChecked()
        if tx:
            list_trs.append("tx")
        if ty:
            list_trs.append("ty")
        if tz:
            list_trs.append("tz")
        if rx:
            list_trs.append("rx")
        if ry:
            list_trs.append("ry")
        if rz:
            list_trs.append("rz")
        if sx:
            list_trs.append("sx")
        if sy:
            list_trs.append("sy")
        if sz:
            list_trs.append("sz")
        if len(out_list) == 0 or len(in_list) == 0:
            return cmds.warning(u"请加载对象!")
        elif len(out_list) == 1 and len(in_list) > 0:
            for rm in in_list:
                connectObjAttr(out_list[0], rm, list_trs)
        elif len(out_list) == len(in_list):
            for lm, rm in zip(out_list, in_list):
                connectObjAttr(lm, rm, list_trs)
        else:
            return cmds.warning(u"请保持两边加载数量一致，或左边只加载一个!")
        cmds.undoInfo(cck = True)

    def _createLayouts(self):
        """
        布局
        :return:
        """
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 5, 10, 10)
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(self.switch_items)

        self.grid_layout_lr = QGridLayout()
        self.main_layout.addLayout(self.grid_layout_lr)
        self.grid_layout_lr.addWidget(self.select_left, 0, 0)
        self.grid_layout_lr.addWidget(self.select_right, 0, 1)
        self.grid_layout_lr.addWidget(self.select_listl, 1, 0)
        self.grid_layout_lr.addWidget(self.select_listr, 1, 1)

        self.match_sbtn_layout = QHBoxLayout()
        self.main_layout.addLayout(self.match_sbtn_layout)
        self.match_sbtn_layout.addWidget(self.match_translation_sbtn)
        self.match_sbtn_layout.addWidget(self.match_rotation_sbtn)
        self.match_sbtn_layout.setAlignment(self.match_translation_sbtn, Qt.AlignHCenter)
        self.match_sbtn_layout.setAlignment(self.match_rotation_sbtn, Qt.AlignHCenter)

        self.parent_sbtn_layout = QHBoxLayout()
        self.main_layout.addLayout(self.parent_sbtn_layout)
        # self.parent_sbtn_layout.addWidget(self.parent_Hierarchy_oto)
        # self.parent_sbtn_layout.addWidget(self.parent_Hierarchy_otm)
        # self.parent_sbtn_layout.setAlignment(self.parent_Hierarchy_oto, Qt.AlignHCenter)
        # self.parent_sbtn_layout.setAlignment(self.parent_Hierarchy_otm, Qt.AlignHCenter)

        self.grid_layout_constrain = QGridLayout()
        self.main_layout.addLayout(self.grid_layout_constrain)
        self.grid_layout_constrain.addWidget(self.parent_sbtn, 0, 0, Qt.AlignHCenter)
        self.grid_layout_constrain.addWidget(self.scale_sbtn, 0, 2, Qt.AlignHCenter)
        self.grid_layout_constrain.addWidget(self.offset_constrain, 1, 1, Qt.AlignHCenter)

        self.main_layout.addWidget(self.offset_matrix)
        self.main_layout.setAlignment(self.offset_matrix, Qt.AlignHCenter)

        self.main_layout.addWidget(self.cop_blendshape)
        self.main_layout.setAlignment(self.cop_blendshape, Qt.AlignHCenter)

        self.grid_layout_attr = QGridLayout()
        self.main_layout.addLayout(self.grid_layout_attr)
        self.grid_layout_constrain.addWidget(self.connect_attr_tx, 0, 0, Qt.AlignHCenter)
        self.grid_layout_constrain.addWidget(self.connect_attr_ty, 0, 1, Qt.AlignHCenter)
        self.grid_layout_constrain.addWidget(self.connect_attr_tz, 0, 2, Qt.AlignHCenter)
        self.grid_layout_constrain.addWidget(self.connect_attr_rx, 1, 0, Qt.AlignHCenter)
        self.grid_layout_constrain.addWidget(self.connect_attr_ry, 1, 1, Qt.AlignHCenter)
        self.grid_layout_constrain.addWidget(self.connect_attr_rz, 1, 2, Qt.AlignHCenter)
        self.grid_layout_constrain.addWidget(self.connect_attr_sx, 2, 0, Qt.AlignHCenter)
        self.grid_layout_constrain.addWidget(self.connect_attr_sy, 2, 1, Qt.AlignHCenter)
        self.grid_layout_constrain.addWidget(self.connect_attr_sz, 2, 2, Qt.AlignHCenter)

        self.main_layout.addWidget(self.apply_btn)

    def _addSelect(self, lorr):
        """
        加载选择项
        :param lorr:左还是右
        :return:
        """
        select_list = cmds.ls(sl = True)
        if lorr == "l":
            self.select_listl.clear()
            self.select_listl.addItems(select_list)
        else:
            self.select_listr.clear()
            self.select_listr.addItems(select_list)


def matchTransform(outp, inp, ps, ro):
    """
    匹配变换
    :param inp: 需匹配（right）list
    :param outp: 被匹配（left）list
    :param ps: 匹配位移
    :param ro: 匹配旋转
    :return:
    """
    cmds.matchTransform(inp, outp, pos = ps, rot = ro)


def constrainFun(outp, inp, parentc, scalec, offset):
    """
    maya约束
    :param outp:
    :param inp:
    :param parentc:
    :param scalec:
    :param offset:
    :return:
    """
    if parentc:
        cmds.parentConstraint(outp, inp, mo = offset)
    elif scalec:
        cmds.scaleConstraint(outp, inp, mo = offset)


def matrixToList(matrix):
    """
    将MMatrix对象转成4*4的列表
    :param matrix: MMatrix
    :return: matrix_list
    """
    matrix_list = list()
    for i in range(4):
        for o in range(4):
            matrix_list.append(matrix(i, o))
    return matrix_list


def matrixConFun(parent, children, ctype, offset):
    """
    矩阵约束
    :param parent: 约束者(父级)列表
    :param children: 被约束者(子级)列表
    :param ctype: 是否为多对一，True是，False不是
    :param offset: 是否偏移
    :return: 所有的节点
    """
    cmds.undoInfo(ock = True)
    node_name = children[0]
    children_type = cmds.objectType(children[0])
    if ctype:
        offset_v = 1.0 / len(parent)
        pma_matrix = cmds.createNode("plusMinusAverage", n = "{0}_{1}".format(node_name, "PMAmatrix"))
        wt_matrix = cmds.createNode("wtAddMatrix", n = "{0}_{1}".format(node_name, "WTmatrix"))
        dp_matrix = cmds.createNode("decomposeMatrix", n = "{0}_{1}".format(node_name, "DPmatrix"))
        cmds.connectAttr(wt_matrix + ".matrixSum", dp_matrix + ".inputMatrix", f = True)
    for i, par in enumerate(parent):
        if not ctype:
            node_name = children[i]
            children_type = cmds.objectType(children[i])
        m_matrix = cmds.createNode("multMatrix", n = "{0}_{1}_{2}".format(node_name, "Mmatrix", i))
        if not ctype:
            dp_matrix = cmds.createNode("decomposeMatrix", n = "{0}_{1}_{2}".format(node_name, "DPmatrix", i))
            cmds.connectAttr(m_matrix + ".matrixSum", dp_matrix + ".inputMatrix", f = True)
        if ctype:
            attr_name = children[0] + "." + par + "_W"
            cmds.addAttr(children[0], ln = par + "_W", at = "double", min = 0, dv = offset_v)
            cmds.setAttr(attr_name, e = True, k = True)
            cmds.connectAttr(m_matrix + ".matrixSum", wt_matrix + ".wtMatrix[{0}].matrixIn".format(i), f = True)
            cmds.connectAttr(attr_name, pma_matrix + ".input1D[{0}]".format(i), f = True)
            md_matrix = cmds.createNode("multiplyDivide", n = "{0}_{1}_{2}".format(node_name, "MDmatrix", i))
            cmds.setAttr(md_matrix + ".operation", 2)
            cmds.connectAttr(attr_name, md_matrix + ".input1X", f = True)
            cmds.connectAttr(pma_matrix + ".output1D", md_matrix + ".input2X", f = True)
            cmds.connectAttr(md_matrix + ".outputX", wt_matrix + ".wtMatrix[{0}].weightIn".format(i), f = True)
        if offset:
            wmatrix = MMatrix()
            wimatrix = MMatrix()
            MScriptUtil.createMatrixFromList(
                cmds.getAttr(children[0] + ".worldMatrix[0]") if ctype else cmds.getAttr(
                    children[i] + ".worldMatrix[0]"),
                wmatrix)
            MScriptUtil.createMatrixFromList(cmds.getAttr(par + ".worldInverseMatrix[0]"), wimatrix)
            offset_matrix = wmatrix * wimatrix
            offset_matrix = matrixToList(offset_matrix)
            cmds.setAttr(m_matrix + ".matrixIn[0]", offset_matrix, type = "matrix")
        cmds.connectAttr(par + ".worldMatrix[0]", m_matrix + ".matrixIn[1]", f = True)
        if ctype:
            cmds.connectAttr(children[0] + ".parentInverseMatrix[0]", m_matrix + ".matrixIn[2]", f = True)
        else:
            cmds.connectAttr(children[i] + ".parentInverseMatrix[0]", m_matrix + ".matrixIn[2]", f = True)
        if not ctype:
            if children_type == "joint":
                etq_node = cmds.createNode('eulerToQuat', n = '{0}_{1}'.format(node_name, 'ETQ'))
                cmds.connectAttr(children[i] + ".rotateOrder", etq_node + ".inputRotateOrder", f = True)
                cmds.connectAttr(children[i] + ".jointOrient", etq_node + ".inputRotate", f = True)
                qi_node = cmds.createNode('quatInvert', n = '{0}_{1}'.format(node_name, 'QI'))
                cmds.connectAttr(etq_node + ".outputQuat", qi_node + ".inputQuat", f = True)
                qp_node = cmds.createNode('quatProd', n = '{0}_{1}'.format(node_name, 'QP'))
                cmds.connectAttr(qi_node + ".outputQuat", qp_node + ".input2Quat", f = True)
                cmds.connectAttr(dp_matrix + ".outputQuat", qp_node + ".input1Quat", f = True)
                qte_node = cmds.createNode('quatToEuler', n = '{0}_{1}'.format(node_name, 'QTE'))
                cmds.connectAttr(qp_node + ".outputQuat", qte_node + ".inputQuat", f = True)
                cmds.connectAttr(qte_node + ".outputRotate", children[i] + ".rotate", f = True)
                cmds.connectAttr(dp_matrix + ".outputTranslate", children[i] + ".translate", f = True)
                cmds.connectAttr(dp_matrix + ".outputScale", children[i] + ".scale", f = True)
                cmds.connectAttr(children[i] + ".rotateOrder", dp_matrix + ".inputRotateOrder", f = True)
            else:
                cmds.connectAttr(children[i] + ".rotateOrder", dp_matrix + ".inputRotateOrder", f = True)
                cmds.connectAttr(dp_matrix + ".outputTranslate", children[i] + ".translate", f = True)
                cmds.connectAttr(dp_matrix + ".outputRotate", children[i] + ".rotate", f = True)
                cmds.connectAttr(dp_matrix + ".outputScale", children[i] + ".scale", f = True)
    if ctype:
        if children_type == "joint":
            etq_node = cmds.createNode('eulerToQuat', n = '{0}_{1}'.format(node_name, 'ETQ'))
            cmds.connectAttr(children[0] + ".rotateOrder", etq_node + ".inputRotateOrder", f = True)
            cmds.connectAttr(children[0] + ".jointOrient", etq_node + ".inputRotate", f = True)
            qi_node = cmds.createNode('quatInvert', n = '{0}_{1}'.format(node_name, 'QI'))
            cmds.connectAttr(etq_node + ".outputQuat", qi_node + ".inputQuat", f = True)
            qp_node = cmds.createNode('quatProd', n = '{0}_{1}'.format(node_name, 'QP'))
            cmds.connectAttr(qi_node + ".outputQuat", qp_node + ".input2Quat", f = True)
            cmds.connectAttr(dp_matrix + ".outputQuat", qp_node + ".input1Quat", f = True)
            qte_node = cmds.createNode('quatToEuler', n = '{0}_{1}'.format(node_name, 'QTE'))
            cmds.connectAttr(qp_node + ".outputQuat", qte_node + ".inputQuat", f = True)
            cmds.connectAttr(qte_node + ".outputRotate", children[0] + ".rotate", f = True)
            cmds.connectAttr(dp_matrix + ".outputTranslate", children[0] + ".translate", f = True)
            cmds.connectAttr(dp_matrix + ".outputScale", children[0] + ".scale", f = True)
            cmds.connectAttr(children[0] + ".rotateOrder", dp_matrix + ".inputRotateOrder", f = True)
        else:
            cmds.connectAttr(children[0] + ".rotateOrder", dp_matrix + ".inputRotateOrder", f = True)
            cmds.connectAttr(dp_matrix + ".outputTranslate", children[0] + ".translate", f = True)
            cmds.connectAttr(dp_matrix + ".outputRotate", children[0] + ".rotate", f = True)
            cmds.connectAttr(dp_matrix + ".outputScale", children[0] + ".scale", f = True)
    cmds.undoInfo(cck = True)
    if ctype:
        return [dp_matrix]
    else:
        return [m_matrix, dp_matrix]


def hierarchyConnect(out_list, in_list):
    """
    父子关系
    :param out_list:
    :param in_list:
    :return:
    """
    cmds.undoInfo(ock = True)
    if len(out_list) == 0:
        return cmds.warning(u"请加载对象!")
    elif len(out_list) == 1 and len(in_list) > 0:
        for r in in_list:
            cmds.parent(r, out_list[0])
    elif len(out_list) == len(in_list):
        for l, r in zip(out_list, in_list):
            cmds.parent(r, l)
    elif len(out_list) > 1 and len(in_list) == 0:
        i = 1
        for l in range(len(out_list)):
            cmds.parent(out_list[i], out_list[l])
            i += 1
            if i == len(out_list):
                break
    else:
        return cmds.warning(u"请保持两边加载数量一致，或右边为0!")
    cmds.undoInfo(cck = True)


def getHistoryNodeByType(obj, the_type):
    """
    获取对象指定类型节点
    :param obj: 对象
    :param the_type: 类型
    :return:
    """
    nodes = cmds.listHistory(obj)
    for n in nodes:
        if cmds.objectType(n) == the_type:
            out_node = n
            break
    try:
        if out_node:
            return out_node
    except NameError:
        return 0


def copSkin(outp, inp):
    """
    拷贝权重
    :param outp:
    :param inp:
    :return:
    """
    get_skin_node = getHistoryNodeByType(outp, "skinCluster")
    if get_skin_node:
        get_joint = cmds.skinCluster(get_skin_node, q = True, inf = True)
        get_skin = getHistoryNodeByType(inp, "skinCluster")
        if get_skin:
            pass
        else:
            get_skin = cmds.skinCluster(get_joint, inp, nw = 1, tsb = True)[0]
        cmds.copySkinWeights(surfaceAssociation = "closestPoint", ds = get_skin, ss = get_skin_node, nm = True,
                             ia = ('oneToOne', 'oneToOne', 'oneToOne'))
    else:
        return cmds.warning(u"对象没有蒙皮！")


def replaceTransferBsMesh(outp, inp):
    """
    传递型节点
    :param outp:
    :param inp:
    :return:
    """
    cmds.blendShape(outp)
    cmds.delete(outp, ch = True)
    outp_shape = cmds.listRelatives(outp, s = True)[0]
    for s in cmds.listRelatives(inp, s = True):
        is_orig = cmds.getAttr(s + ".io")
        if is_orig:
            get_orig = s
    try:
        if get_orig:
            cmds.currentTime(0)
            cmds.connectAttr(outp_shape + ".outMesh", get_orig + ".inMesh", f = True)
            cmds.currentTime(1)
            cmds.disconnectAttr(outp_shape + ".outMesh", get_orig + ".inMesh")
            cmds.currentTime(0)
            index = cmds.polyEvaluate(get_orig, v = True)
            for i in range(index):
                cmds.setAttr(get_orig + ".pnts[{}].pntx".format(i), 0)
                cmds.setAttr(get_orig + ".pnts[{}].pnty".format(i), 0)
                cmds.setAttr(get_orig + ".pnts[{}].pntz".format(i), 0)
    except NameError:
        inp_shape = cmds.listRelatives(inp, s = True)[0]
        cmds.currentTime(0)
        cmds.connectAttr(outp_shape + ".outMesh", inp_shape + ".inMesh", f = True)
        cmds.currentTime(1)
        cmds.disconnectAttr(outp_shape + ".outMesh", inp_shape + ".inMesh")
        cmds.currentTime(0)


def copBlendShapeConnect(outp, inp):
    """
    拷贝BS的连接
    :param outp:
    :param inp:
    :return:
    """
    get_outp_bs = getHistoryNodeByType(outp, "blendShape")
    target_bs = cmds.listAttr(get_outp_bs + ".w", m = True, w = True)
    get_inp_bs = getHistoryNodeByType(inp, "blendShape")
    for attr in target_bs:
        if cmds.objExists(get_inp_bs + "." + attr):
            out_conn = cmds.connectionInfo(get_outp_bs + "." + attr, sfd = True)
            cmds.connectAttr(out_conn, get_inp_bs + "." + attr, f = True)


def connectObjAttr(outp, inp, list_trs):
    """
    连接对应属性
    :param outp:
    :param inp:
    :param list_trs:
    :return:
    """
    for key in list_trs:
        if key == "tx":
            cmds.connectAttr(outp + ".tx", inp + ".tx", f = True)
        elif key == "ty":
            cmds.connectAttr(outp + ".ty", inp + ".ty", f = True)
        elif key == "tz":
            cmds.connectAttr(outp + ".tz", inp + ".tz", f = True)
        elif key == "rx":
            cmds.connectAttr(outp + ".rx", inp + ".rx", f = True)
        elif key == "ry":
            cmds.connectAttr(outp + ".ry", inp + ".ry", f = True)
        elif key == "rz":
            cmds.connectAttr(outp + ".rz", inp + ".rz", f = True)
        elif key == "sx":
            cmds.connectAttr(outp + ".sx", inp + ".sx", f = True)
        elif key == "sy":
            cmds.connectAttr(outp + ".sy", inp + ".sy", f = True)
        elif key == "sz":
            cmds.connectAttr(outp + ".sz", inp + ".sz", f = True)


def createWrap(outp, inp):
    """
    创建包裹变形
    :param outp:
    :param inp:
    :return:
    """
    outp_shape = cmds.listRelatives(outp, s = True)[0]
    wrap_node = cmds.deformer(inp, type = "wrap")[0]

    cmds.setAttr(wrap_node + '.weightThreshold', 0.0)
    cmds.setAttr(wrap_node + '.maxDistance', 1.0)
    cmds.setAttr(wrap_node + '.exclusiveBind', False)
    cmds.setAttr(wrap_node + '.autoWeightThreshold', True)
    cmds.setAttr(wrap_node + '.falloffMode', 0)
    cmds.connectAttr(inp + '.worldMatrix[0]', wrap_node + '.geomMatrix')
    base_mesh = cmds.duplicate(outp, n = outp + "Base")[0]
    base_shape = cmds.listRelatives(base_mesh, s = True)[0]
    cmds.hide(base_mesh)
    if not cmds.attributeQuery('dropoff', n = outp, exists = True):
        cmds.addAttr(outp, sn = 'dr', ln = 'dropoff', dv = 4.0, min = 0.0, max = 20.0)
        cmds.setAttr(outp + '.dr', k = True)
    if not cmds.attributeQuery('smoothness', n = outp, exists = True):
        cmds.addAttr(outp, sn = 'smt', ln = 'smoothness', dv = 0.0, min = 0.0)
        cmds.setAttr(outp + '.smt', k = True)
    if not cmds.attributeQuery('inflType', n = outp, exists = True):
        cmds.addAttr(outp, at = 'short', sn = 'ift', ln = 'inflType', dv = 2, min = 1, max = 2)

    cmds.connectAttr(outp_shape + '.worldMesh', wrap_node + '.driverPoints[0]')
    cmds.connectAttr(base_shape + '.worldMesh', wrap_node + '.basePoints[0]')
    cmds.connectAttr(outp + '.inflType', wrap_node + '.inflType[0]')
    cmds.connectAttr(outp + '.smoothness', wrap_node + '.smoothness[0]')
    cmds.connectAttr(outp + '.dropoff', wrap_node + '.dropoff[0]')
    return [wrap_node, base_mesh]


def wrapConvertBlendShape(outp, inp, dm):
    """
    包裹传递BS
    :param outp:
    :param inp:
    :param dm: deltaMush
    :return:
    """
    get_blendshape = getHistoryNodeByType(outp, "blendShape")
    bs_target = cmds.listAttr(get_blendshape + ".w", m = True, w = True)
    if len(bs_target) != 0:
        wrap_node, base_mesh = createWrap(outp, inp)
        list_target = []
        if dm:
            dm_node = cmds.deltaMush(inp)
        if cmds.objExists("WCT"):
            cmds.delete("WCT")
            wct = cmds.createNode("transform", n = "WCT")
        else:
            wct = cmds.createNode("transform", n = "WCT")
        for t in bs_target:
            bs_w = cmds.getAttr(get_blendshape + ".{}".format(t))
            if bs_w != 1 and not cmds.connectionInfo(get_blendshape + ".{}".format(t), il = True):
                cmds.setAttr(get_blendshape + ".{}".format(t), 1)
                copy_mesh = cmds.duplicate(inp)
                cmds.parent(copy_mesh, wct)
                cmds.rename(copy_mesh, t)
                cmds.setAttr(get_blendshape + ".{}".format(t), 0)
                list_target.append("WCT|{}".format(t))
        cmds.delete([wrap_node, base_mesh])
        if dm:
            cmds.delete(dm_node)
        cmds.blendShape(list_target, inp, frontOfChain = True)
        cmds.delete(wct)
    else:
        return cmds.warning(u"{}BS列表为空！".format(outp))
