# -*- coding: UTF-8 -*-
# @FileName      : control
# @Time          : 2024-05-29
# @Author        : LJF
# @Contact       : 906629272@qq.com

import os
import maya.cmds as cmds
from maya.api.OpenMaya import *
import json
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

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
                ("r", "radius"), ("ro", "rotate"), ("o", "offset"), ("l", "locked"), ("ou", "outputs")]
        for index, (short, long) in enumerate(keys):
            # 依次获取索引，短参， 长参
            arg = kwargs.get(long, kwargs.get(short, args[index] if index < len(args) else None))
            if arg is not None:
                # 如果 arg 不为None，则执行对应方法
                getattr(self, "set_" + long)(arg)

    def edit_shape_by_copy_ctrl(self, callback):
        """

        :param callback: 回调函数, 用来修改copy_ctrl的位移,旋转,缩放
        :return:
        """
        # 创建一个临时控制器, 复制控制器形态
        copy_ctrl = ToolControl(shape = self.get_shape())
        # 执行回调函数,对控制器位移,旋转,缩放进行修改
        callback(copy_ctrl.get_transform())
        # 冻结copy_ctrl变换
        cmds.makeIdentity(copy_ctrl.get_transform(), apply = True, t = True, r = True, s = True)
        cmds.xform(copy_ctrl.get_transform(), piv = [0, 0, 0])
        # 设置控制器形态为临时控制器形态, 保留颜色与输出
        ToolControl(self.get_transform(), shape = copy_ctrl.get_shape(), color = self.get_color(),
                    outputs = self.get_outputs())
        # 删除临时控制器
        cmds.delete(copy_ctrl.get_transform())

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
        # 获取对应json数据
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
                    return [cmds.getAttr(shape_n + ".overrideColorRGB"), True]
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
            # 将属性转化为[(输出如属性, 输出如节点.输出属性)]
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


class ControlUI(QWidget):
    """
    控制器
    """

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setObjectName("ControlWindow")

        self._createListWidget()
        self._colorPicker()
        self._createPushBtn()
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
        self.setColorP = QPushButton(u"自定义颜色")
        self.setColorP.setFixedHeight(35)
        self.setColorP.setStyleSheet(qss)

    def _createConnect(self):
        """

        :return:
        """
        self.setColorP.clicked.connect(lambda c: setColorBySelected([self.colorPik.getRgb, True]))

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
