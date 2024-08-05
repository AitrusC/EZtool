# -*- coding: UTF-8 -*-
# @FileName      : control
# @Time          : 2024-05-29
# @Author        : LJF
# @Contact       : 906629272@qq.com

"""
控制器设置
"""



import json
import os

import maya.cmds as cmds
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from maya.api.OpenMaya import *
from . import uiWidget

indexRGB = [[0.5, 0.5, 0.5], [0, 0, 0], [0.247, 0.247, 0.247], [0.498, 0.498, 0.498],
            [0.608, 0, 0.157], [0, 0.16, 0.376], [0, 0, 1], [0, 0.275, 0.094],
            [0.149, 0, 0.263], [0.78, 0, 0.78], [0.537, 0.278, 0.2], [0.243, 0.133, 0.121],
            [0.6, 0.145, 0], [1, 0, 0], [0, 1, 0], [0, 0.2549, 0.6],
            [1, 1, 1], [1, 1, 0], [0.388, 0.863, 1], [0.263, 1, 0.639], [1, 0.686, 0.686],
            [0.89, 0.674, 0.474], [1, 1, 0.388], [0, 0.6, 0.329], [0.627, 0.411, 0.188],
            [0.619, 0.627, 0.188], [0.408, 0.631, 0.188], [0.188, 0.631, 0.365], [0.188, 0.627, 0.627],
            [0.188, 0.403, 0.627], [0.434, 0.188, 0.627], [0.627, 0.188, 0.411]
            ]


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


def linear_to_srgb(linear):
    """RGB to sRGB."""
    if linear <= 0.0031308:
        return linear * 12.92
    else:
        return 1.055 * (linear ** (1 / 2.4)) - 0.055


def api_ls(*names):
    selection_list = MSelectionList()
    for name in names:
        selection_list.add(name)
    return selection_list


class ToolControl(object):
    """
    功能 修改控制器
    """

    def __init__(self, *args, **kwargs):
        u"""

        :param kwargs: 修改控制器的参数
        :param kwargs: -t -transform string 控制器
        :param kwargs: -n -name string 名字
        :param kwargs: -p -parent string 父对象
        :param kwargs: -s -shape string 形态
        :param kwargs: -c -color [int/(int, int, int), bool] 颜色或自定义颜色
        :param kwargs: -r -radius float 半径
        :param kwargs: -ro -rotate [float, float,float] 旋转
        :param kwargs: -o -offset [float, float,float] 偏移
        :param kwargs: -l -locked [str, ...] 锁定属性
        :param kwargs: -ou -outputs [str, str] 输出属性
        """
        self.uuid = None
        keys = [("t", "transform"), ("n", "name"), ("p", "parent"), ("s", "shape"), ("ot", "other"), ("c", "color"),
                ("r", "radius"), ("ro", "rotate"), ("o", "offset"), ("l", "locked"), ("ou", "outputs"), ("s", "scale")]
        for index, (short, long) in enumerate(keys):
            # 依次获取索引，短参， 长参
            arg = kwargs.get(long, kwargs.get(short, args[index] if index < len(args) else None))
            if arg is not None:
                # 如果 arg 不为None，则执行对应方法
                getattr(self, "set_" + long)(arg)

    def editShapeByCopyCtrl(self, callback):
        """

        :param callback: 回调函数, 用来修改copy_ctrl的位移,旋转,缩放
        :return:
        """
        # 创建一个临时控制器, 复制控制器形态
        copyCtrl = ToolControl(shape = self.get_shape())
        # 执行回调函数,对控制器位移,旋转,缩放进行修改
        callback(copyCtrl.get_transform())
        # 冻结copy_ctrl变换
        cmds.makeIdentity(copyCtrl.get_transform(), apply = True, t = True, r = True, s = True)
        cmds.xform(copyCtrl.get_transform(), piv = [0, 0, 0])
        # 设置控制器形态为临时控制器形态, 保留颜色与输出
        ToolControl(self.get_transform(), shape = copyCtrl.get_shape(), color = self.get_color(),
                    outputs = self.get_outputs())
        # 删除临时控制器
        cmds.delete(copyCtrl.get_transform())

    def set_transform(self, transform):
        """
        记录控制器id
        :param transform: string名字
        :return: self
        """
        uuids = cmds.ls(transform, type = ["transform", "joint"], o = True, uid = True)
        if len(uuids) != 1:
            # 存在不唯一的情况
            return self
        self.uuid = uuids[0]
        return self

    def get_transform(self):
        """
        根据uuid获取控制器的dag路径
        :return:
        """
        transform = cmds.ls(self.uuid, l = True)
        if len(transform) == 1:
            return transform[0]
        else:
            self.set_transform(cmds.group(em = True, n = "control"))
            return self.get_transform()

    def get_name(self):
        """
        获取短名
        :return: 名
        """
        return self.get_transform().split("|")[-1].split(":")[-1]

    def get_shape_names(self):
        """
        获取控制器所有的shape名
        :return: [name]
        """
        # 若结果为None则返回[]
        shapes = cmds.listRelatives(self.get_transform(), s = True, f = True) or []
        return [shape for shape in shapes if cmds.nodeType(shape) == "nurbsCurve"]

    def get_shape(self):
        """
        获取shape数据
        :return:
        """
        return [dict(
            points = cmds.xform(shape + ".cv[*]", q = 1, t = 1, ws = 0),  # 局部顶点坐标
            periodic = cmds.getAttr(shape + ".form") == 2,  # 是否闭合
            degree = cmds.getAttr(shape + ".degree"),  # 次数
            knot = list(MFnNurbsCurve(api_ls(shape).getDagPath(0)).knots()),  # 结点
        ) for shape in self.get_shape_names()]

    def set_shape(self, shape):
        """
        加载控制器
        :param shape: 对应名称
        :return: self
        """
        # 删除原有shape
        if self.get_shape_names():
            cmds.delete(self.get_shape_names())
        # shape是否为list判断是否获取对应json数据（shape为列表是从self.get_shape里获取）
        if not isinstance(shape, list):
            dataFile = os.path.abspath(__file__ + "/../res/Cdata/{shape}.json".format(shape = shape))
            if os.path.isfile(dataFile):
                with open(dataFile, "r") as f:
                    shape = json.load(f)
            else:
                shape = []
        for data in shape:
            # 获取points并将数据转为2X3
            points = data["points"]
            points = [points[i:i + 3] for i in range(0, len(points), 3)]
            # 是否闭合
            if data["periodic"]:
                points = points + points[:data["degree"]]
            # 创建替换曲线
            curve = cmds.curve(d = data["degree"], k = data["knot"], per = data["periodic"], p = points)
            # 放入控制器下
            cmds.parent(cmds.listRelatives(curve, s = True, f = True), self.get_transform(), s = True, add = True)
            # 删除替换曲线
            cmds.delete(curve)
        for shape_n in self.get_shape_names():
            cmds.rename(shape_n, self.get_name() + "Shape")
        return self

    def get_color(self):
        """
        获取颜色
        :return: 颜色[int/(int, int, int), bool]
        """
        for shape_n in self.get_shape_names():
            if cmds.getAttr(shape_n + ".overrideEnabled"):
                if cmds.getAttr(shape_n + ".overrideRGBColors"):
                    return [cmds.getAttr(shape_n + ".overrideColorRGB")[0], True]
                else:
                    return [cmds.getAttr(shape_n + ".overrideColor"), False]

    def set_color(self, color):
        """
        修改颜色
        :param color: [int/(int, int, int), bool] 颜色或自定义颜色
        :return:
        """
        cvalue, bol = color
        for shape_n in self.get_shape_names():
            cmds.setAttr(shape_n + ".overrideEnabled", True)
            if not bol:
                cmds.setAttr(shape_n + ".overrideRGBColors", 0)
                cmds.setAttr(shape_n + ".overrideColor", cvalue)
            else:
                cmds.setAttr(shape_n + ".overrideRGBColors", 1)
                cmds.setAttr(shape_n + ".overrideColorRGB", cvalue[0], cvalue[1], cvalue[2], type = "float3")

    def get_outputs(self):
        """
        获取控制器shape接口
        :return: [输出接口，输入接口]
        """
        for shape in self.get_shape_names():
            # 获取输出接口
            destination = cmds.listConnections(shape, d = True, p = True, c = True, s = False) or []
            # 获取输入接口
            source = cmds.listConnections(shape, d = False, p = True, c = True, s = True) or []
            # 将属性转化为[(输出入属性, 输出入节点.输出入属性)]
            destination = [destination[i:i + 2] for i in range(0, len(destination), 2)]
            destination = [(cmds.attributeName(src, l = True), dst) for src, dst in destination]
            source = [source[i:i + 2] for i in range(0, len(source), 2)]
            source = [(cmds.attributeName(src, l = True), dst) for src, dst in source]
            return [destination, source]

    def set_outputs(self, plugs):
        """
        将连接还原
        :return:
        """
        dst, src = plugs
        for shape_name in self.get_shape_names():
            for s in src:
                cmds.connectAttr(s[1], shape_name + "." + s[0], f = True)
            for d in dst:
                cmds.connectAttr(shape_name + "." + d[0], d[1], f = True)
            break
        return self

    def get_radius(self):
        """
        获取大小
        :return: 最大值
        """
        # 获取shape所有CV点的坐标
        points = sum([cmds.xform(shape + ".cv[*]", q = True, t = True) for shape in self.get_shape_names()], [])
        points = [points[i:i + 3] for i in range(0, len(points), 3)]
        # 求每条向量的长度
        lengths = [sum([v ** 2 for v in point]) ** 0.5 for point in points]
        # 取最长返回
        if len(lengths) > 0:
            return max(lengths)

    def set_radius(self, radius):
        """
        设置大小
        :param radius: 给定半径
        :return: self
        """
        # 获取原半径
        oldRadius = self.get_radius()
        # 若半径太小则不设置
        if oldRadius is None or radius < 0.0001 or oldRadius < 0.0001:
            return self
        # 比值
        scale = radius / oldRadius
        # 根据比值设置每个cv的位置
        for shape in self.get_shape_names():
            points = sum([cmds.xform(shape + ".cv[*]", q = True, t = True)], [])
            points = [points[i:i + 3] for i in range(0, len(points), 3)]
            points = [[p[0] * scale, p[1] * scale, p[2] * scale] for p in points]
            for i, p in enumerate(points):
                cmds.xform(shape + ".cv[{0}]".format(i), t = p)

    def set_rotate(self, rotate):
        """
        旋转控制器
        :param rotate: [轴向, 度数]
        :return: self
        """
        axial, rotate = rotate[0], int(rotate[1])
        for s in self.get_shape_names():
            cmds.rotate(rotate * axial[0], rotate * axial[1], rotate * axial[2], s + ".cv[*]", r = True, ocp = True,
                        os = True)
        return self

    def set_scale(self, scale):
        """
        缩放控制器
        :param scale: [轴向,缩放数值]
        :return: self
        """
        axial, scale = scale
        mods = cmds.getModifiers()
        if (mods & 4) > 0:
            scale = 1.0 / scale
        for s in self.get_shape_names():
            cmds.select(s, r = True)
            cmds.refresh()
            cmds.setToolTo("moveSuperContext")
            pos = cmds.manipMoveContext("Move", q = True, p = True)
            cmds.scale(axial[0] * scale or 1, axial[1] * scale or 1, axial[2] * scale or 1, s + ".cv[*]", r = True,
                       p = pos)


def set_selected_controls(*args, **kwargs):
    """
    获取所选控制器或骨骼，执行对应功能
    :param args:
    :param kwargs:
    :return:
    """
    controls = cmds.ls(sl = True, l = True, type = ["joint", "transform"])
    for ctrl in controls:
        # 使用ToolControl里的get方法保留控制器相关的属性
        kwargs.update({key: getattr(ToolControl(ctrl), "get_" + key)() for key in args})
        ToolControl(ctrl, **kwargs)
    # 刷新节点
    cmds.dgdirty(controls)


@undo
def setColorBySelected(color):
    """
    根据所选对象设置颜色
    :param color: [int/(int, int, int), bool] 颜色或自定义颜色
    :return:
    """
    set_selected_controls(color = color)


@undo
def createControl(shape):
    """
    创建控制器
    :param shape: 所选控制器名称
    :return:
    """
    # 是否选择控制器，否则创建控制器
    cmds.ls(sl = True, l = True, type = ["joint", "transform"]) or cmds.group(em = True, n = shape)
    set_selected_controls("color", "outputs", "radius", shape = shape)


@undo
def setRotateControl(axial, rotate):
    """
    旋转控制器
    :param axial: 旋转轴向
    :param rotate: 旋转度数
    :return:
    """
    cmds.ls(sl = True, l = True, type = ["joint", "transform"])
    set_selected_controls(rotate = [axial, rotate])


@undo
def setScaleControl(axial, scale):
    """
    缩放控制器
    :param axial: 缩放轴向
    :param scale: 缩放系数
    :return:
    """
    cmds.ls(sl = True, l = True, type = ["joint", "transform"])
    set_selected_controls(scale = [axial, scale])


@undo
def freezeControl():
    """
    冻结控制器
    :return:
    """
    controls = cmds.ls(sl = True, l = True, type = ["joint", "transform"])
    for ctrl in controls:
        ToolControl(ctrl).editShapeByCopyCtrl(
            lambda copyCtrl: cmds.xform(copyCtrl, m = cmds.xform(ctrl, q = True, m = True)))
        cmds.xform(ctrl, ws = False, m = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])


@undo
def replaceControl():
    """
    替换控制器，以最后所选为准
    :return:
    """
    control = cmds.ls(sl = True, l = True, type = ["joint", "transform"])
    if control:
        set_selected_controls("color", "outputs", shape = ToolControl(control[-1]).get_shape())


@undo
def mirrorControl():
    """
    镜像控制器（根据"_L"，"_R"）
    :return:
    """
    listL = ["_L", "_l", "_left", "_Left"]
    listR = ["_R", "_r", "_right", "_Right"]
    control = cmds.ls(sl = True, l = True, type = ["joint", "transform"])
    controlSrc = [ctrl for ctrl in control if
                  any(s in ctrl for s in listR + listL)]
    controlDst = []
    # ind = 0
    for ctrl in controlSrc:
        # ind += 1
        bor = [[s, index] for index, s in enumerate(listR) if s in ctrl]
        bol = [[s, index] for index, s in enumerate(listL) if s in ctrl]
        # print(ctrl, bor, ind)
        if bor:
            controlDst.append(ctrl.replace(listR[bor[0][1]], listL[bor[0][1]]))
        else:
            controlDst.append(ctrl.replace(listL[bol[0][1]], listR[bol[0][1]]))
    for s, d in zip(controlSrc, controlDst):
        def mirrorCallback(copyCtrl):
            ToolControl(copyCtrl, shape = ToolControl(s).get_shape())
            cmds.xform(copyCtrl, ws = True, m = cmds.xform(s, q = True, ws = True, m = True))
            cmds.makeIdentity(copyCtrl, apply = True, t = True, r = True, s = True)
            cmds.xform(copyCtrl, piv = [0, 0, 0])
            cmds.setAttr(copyCtrl + ".sx", -1)
            cmds.makeIdentity(copyCtrl, apply = True, t = True, r = True, s = True)
            cmds.xform(copyCtrl, piv = [0, 0, 0])
            cmds.parent(copyCtrl, d)

        ToolControl(d).editShapeByCopyCtrl(mirrorCallback)


class ControlUI(QWidget):
    """
    控制器
    """

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setObjectName("ControlWindow")

        self._createListWidget()
        self._colorPicker()
        self._createSplitter()
        self._createPushBtn()
        self._createLabel()
        self._createLineEdit()
        self._createCBWidgets()
        self._createConnect()

        self._createLayout()

    def _createListWidget(self):
        """
        添加图标,颜色
        :return:
        """
        self.iconList = PixmapList()
        self.colorList = ColorList()
        self.colorList.setFixedHeight(100)

    def _colorPicker(self):
        """
        颜色选取
        :return:
        """
        self.colorPik = ColorPickerWidget()

    def _createSplitter(self):
        """
        分割线
        """
        self.splitter1 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)
        self.splitter2 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)
        self.splitter3 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)
        self.splitter4 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)

    def _createPushBtn(self):
        """
        按钮
        :return:
        """
        with open(__file__ + "/../res/qss/QPushButtonA.qss", "r") as f:
            qss = f.read()
        self.setColorP = QPushButton(u"自定义颜色")
        self.setColorP.setFixedHeight(35)
        # 旋转
        self.rotateX = QPushButton(u"X")
        self.rotateY = QPushButton(u"Y")
        self.rotateZ = QPushButton(u"Z")
        # 缩放
        self.scaleC = QPushButton(u"缩放")
        # 冻结
        self.freezeC = QPushButton(u"冻结")
        # 镜像
        self.mirrorC = QPushButton(u"镜像")
        # 替换
        self.replaceC = QPushButton(u"替换")
        # 设置样式
        self.setColorP.setStyleSheet(qss)
        self.rotateX.setStyleSheet(qss)
        self.rotateY.setStyleSheet(qss)
        self.rotateZ.setStyleSheet(qss)
        self.scaleC.setStyleSheet(qss)
        self.freezeC.setStyleSheet(qss)
        self.mirrorC.setStyleSheet(qss)
        self.replaceC.setStyleSheet(qss)

    def _createLabel(self):
        """
        标签
        :return:
        """
        qss = "QLabel { color: rgb(204, 204, 214); font: bold 10pt \"Microsoft YaHei\"; }"
        self.rotateL = QLabel(u"旋转控制器：")
        self.rotateL.setStyleSheet(qss)
        self.scaleL = QLabel(u"缩放控制器：")
        self.scaleL.setStyleSheet(qss)

    def _createLineEdit(self):
        """
        输入框
        :return:
        """
        qss = "QLabel { color: rgb(204, 204, 214); font: bold 10pt \"Microsoft YaHei\"; }"
        self.rotateLE = QLineEdit()
        self.rotateLE.setFixedWidth(100)
        self.rotateLE.setText("90")
        self.rotateLE.setValidator(QIntValidator())
        self.rotateLE.setStyleSheet(qss)

        self.scaleLE = QLineEdit()
        self.scaleLE.setFixedWidth(75)
        self.scaleLE.setText("1.1")
        # 创建一个 QDoubleValidator 对象,设置范围为 [0.0, 2147483647.0]，小数点后1位
        doubleValidator = QDoubleValidator(0.0, 2147483647.0, 1)
        doubleValidator.setNotation(QDoubleValidator.StandardNotation)
        self.scaleLE.setValidator(doubleValidator)
        self.scaleLE.setStyleSheet(qss)

    def _createCBWidgets(self):
        """
        下拉框
        :return:
        """
        self.scaleXYZ = QComboBox()
        self.scaleXYZ.addItems(["XYZ", "X", "Y", "Z"])

    def _createConnect(self):
        """

        :return:
        """
        self.setColorP.clicked.connect(lambda c: setColorBySelected([self.colorPik.getRgb, True]))
        self.rotateX.clicked.connect(lambda r: setRotateControl([1, 0, 0], self.rotateLE.text()))
        self.rotateY.clicked.connect(lambda r: setRotateControl([0, 1, 0], self.rotateLE.text()))
        self.rotateZ.clicked.connect(lambda r: setRotateControl([0, 0, 1], self.rotateLE.text()))
        self.scaleC.clicked.connect(self._scaleConnect)
        self.freezeC.clicked.connect(freezeControl)
        self.replaceC.clicked.connect(replaceControl)
        self.mirrorC.clicked.connect(mirrorControl)

    def _scaleConnect(self):
        """
        缩放
        :return:
        """
        axial = [[1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
        axial = axial[self.scaleXYZ.currentIndex()]
        scale = float(self.scaleLE.text())
        setScaleControl(axial, scale)

    def _createLayout(self):
        """
        布局
        """
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(10, 5, 10, 10)
        self.setLayout(self.mainLayout)

        self.mainLayout.addWidget(self.iconList)
        self.mainLayout.addWidget(self.colorList)
        self.mainLayout.addWidget(self.colorPik)
        self.mainLayout.addWidget(self.setColorP)

        self.mainLayout.addWidget(self.splitter1)
        self.hboxLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.hboxLayout)
        self.hboxLayout.addWidget(self.rotateL)
        self.hboxLayout.addWidget(self.rotateX)
        self.hboxLayout.addWidget(self.rotateY)
        self.hboxLayout.addWidget(self.rotateZ)
        self.hboxLayout.addWidget(self.rotateLE)

        self.mainLayout.addWidget(self.splitter2)
        self.hboxLayout2 = QHBoxLayout()
        self.mainLayout.addLayout(self.hboxLayout2)
        self.hboxLayout2.addWidget(self.scaleL)
        self.hboxLayout2.addWidget(self.scaleC)
        self.hboxLayout2.addWidget(self.scaleXYZ)
        self.hboxLayout2.addWidget(self.scaleLE)

        self.mainLayout.addWidget(self.splitter3)
        self.hboxLayout3 = QHBoxLayout()
        self.mainLayout.addLayout(self.hboxLayout3)
        self.hboxLayout3.addWidget(self.freezeC)
        self.hboxLayout3.addWidget(self.mirrorC)
        self.hboxLayout3.addWidget(self.replaceC)

        self.mainLayout.addWidget(self.splitter4)


class PixmapList(QListWidget):
    """
    展示图标
    """

    def __init__(self):
        QListWidget.__init__(self)
        # 图标显示
        self.setViewMode(self.IconMode)
        # 设置图标尺寸
        self.setIconSize(QSize(61, 61))
        # 无法拖拽
        self.setMovement(self.Static)
        # 隐藏横向滑条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 实时排列
        self.setResizeMode(self.Adjust)
        # 双击事件
        self.itemDoubleClicked.connect(lambda n: createControl(n.name))
        # 剔除边框
        self.setStyleSheet("QListWidget { border: none; background-color: rgb(73, 73, 73)}")
        # 刷新
        self.showIcon()

    def showIcon(self):
        """
        显示图标
        :return:
        """
        # 清空图标
        self.clear()
        # 获取图标路径
        dateDir = os.path.abspath(__file__ + "/../res/Cdata/")
        for file_n in os.listdir(dateDir):
            # 获取图片
            if not file_n.endswith(".png"):
                continue
            # 获取文件路径
            pngPath = os.path.join(dateDir, file_n)
            # item
            item = QListWidgetItem(QIcon(pngPath), "", self)
            # 获取名称
            name, _ = os.path.splitext(file_n)
            item.name = name
            # 设置item尺寸
            item.setSizeHint(QSize(64, 64))


class ColorPickerWidget(QLabel):
    """
    颜色选取
    """

    def __init__(self):
        QLabel.__init__(self)
        # 设置默认rgb
        self.setRgb = QColor.fromRgb(255, 255, 255)
        # 颜色显示
        self.setStyleSheet("QLabel {{ background-color: {} }}".format(self.setRgb.name()))
        # 输出rgb
        self.getRgb = [255, 255, 255]

    def showColorDialog(self):
        """
        调色板
        :return: rgb
        """
        cmds.colorEditor()
        if cmds.colorEditor(q = True, r = True):
            self.getRgb = cmds.colorEditor(q = True, rgb = True)
            self.setRgb = QColor.fromRgbF(self.getRgb[0], self.getRgb[1], self.getRgb[2])
            self.setStyleSheet("QLabel {{ background-color: {} }}".format(self.setRgb.name()))
        print(self.getRgb)
        return self.getRgb

    def mouseDoubleClickEvent(self, event):
        """
        双击调出调色板
        :param event:
        :return:
        """
        if event.buttons() == Qt.LeftButton:
            return self.showColorDialog()


class ColorList(QListWidget):
    """
    颜色图标
    """

    def __init__(self):
        QListWidget.__init__(self)
        # 图标显示
        self.setViewMode(self.IconMode)
        # 设置图标尺寸
        self.setIconSize(QSize(32, 32))
        # 无法拖拽
        self.setMovement(self.Static)
        # 隐藏横向滑条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 实时排列
        self.setResizeMode(self.Adjust)
        # 剔除边框
        self.setStyleSheet("QListWidget { border: none; background-color: rgb(73, 73, 73)}")
        # 显示
        for i, rgb in enumerate(indexRGB):
            pix = QPixmap(32, 32)
            pix.fill(QColor.fromRgbF(*rgb))
            item = QListWidgetItem(QIcon(pix), "", self)
            item.setSizeHint(QSize(35, 35))
        # 双击
        self.itemDoubleClicked.connect(lambda x: setColorBySelected([self.indexFromItem(x).row(), False]))


if __name__ == '__main__':
    import maya.OpenMayaUI as omui
    from shiboken2 import wrapInstance

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)


    class TestC(ControlUI):

        def __init__(self, parent = mayaMainWindow):
            ControlUI.__init__(self, parent)
            self.setWindowFlags(self.windowFlags() | Qt.Window)


    showUI = TestC()
    showUI.show()
