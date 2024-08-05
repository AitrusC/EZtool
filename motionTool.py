# -*- coding: UTF-8 -*-
# @FileName      : motionTool
# @Time          : 2024-07-19
# @Author        : LJF
# @Contact       : 906629272@qq.com
"""
路径控制设置
"""
import maya.cmds as cmds


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


def selectedCurve():
    """
    选择曲线
    :return:
    """
    try:
        selected_shape = cmds.listRelatives(cmds.ls(sl = True)[0] or [], s = True) or []
    except IndexError:
        return 0
    if selected_shape:
        if cmds.objectType(selected_shape) == "nurbsCurve":
            return cmds.ls(sl = True)[0]
    return 0


def createCurve(name, ref_curve, joint_num):
    """
    创建骨骼定位曲线
    :param name: 名字
    :param ref_curve: 参考的曲线名字
    :param joint_num: 骨骼数量
    :return:
    """
    curve_joint = cmds.duplicate(ref_curve, rr = True, n = "{0}_joint".format(ref_curve))[0]
    cmds.rebuildCurve(curve_joint, ch = False, rpo = True, end = 1, kr = 1, kt = False, s = joint_num - 1, d = 3)
    joints = [
        cmds.joint(rad = 0.5, p = cmds.pointPosition(ep, w = True), n = "{0}_skinJoint{1:0>2}".format(name, index + 1))
        for index, ep in enumerate(cmds.ls(curve_joint + ".ep[*]", fl = True))]


class ControlTool():
    """
    创建工具
    """

    def __init__(self):
        """
        创建初始层级
        """
        self.main_group = cmds.createNode("transform", name = "motionControlSystem")
