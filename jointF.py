# -*- coding: UTF-8 -*-
# @FileName      : jointOrientF
# @Time          : 2024-08-01
# @Author        : LJF
# @Contact       : 906629272@qq.com
"""
骨骼方向设置功能函数
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


def selectAllJointByHierarchy(joints):
    """
    按顺序选择层级下所有的骨骼
    :param joints: list 用来存骨骼名的列表
    :return: 骨骼列表
    """
    children = cmds.listRelatives(joints[-1], c = True, type = "joint") or []
    for j in children:
        joints.append(j)
        if len(cmds.listRelatives(j, c = True, type = "joint") or []) == 0:
            continue
        else:
            selectAllJointByHierarchy(joints)
    return joints


class JointFn():
    """
    骨骼方向设置
    """

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs: -j -joint string 骨骼
        :param kwargs: -ad -axisDisplay bool 显示局部轴向
        :param kwargs: -jo -jointOrient list [主轴, 次轴, 世界方向] 设置骨骼轴向
        """
        self.uuid = None
        keys = [("j", "joint"), ("ad", "axisDisplay"), ("jo", "jointOrient"), ("oo", "offsetOrient")]
        for index, (short, long) in enumerate(keys):
            # 依次获取索引，短参， 长参
            arg = kwargs.get(long, kwargs.get(short, args[index] if index < len(args) else None))
            if arg is not None:
                # 执行对应的set方法
                getattr(self, "set_" + long)(arg)

    def set_joint(self, joint):
        """
        记录骨骼uuid
        :param joint: string名字
        :return: self
        """
        uuids = cmds.ls(joint, type = "joint", o = True, uid = True)
        if len(uuids) != 1:
            # 存在不唯一的情况
            return self
        self.uuid = uuids[0]
        return self

    def get_joint(self):
        """
        根据uuid获取骨骼的dag路径
        :return: dag
        """
        joint = cmds.ls(self.uuid, l = True)
        if len(joint) == 1:
            return joint[0]
        else:
            self.set_joint(cmds.group(em = True, n = "control"))
            return self.get_joint()

    def get_axisDisplay(self):
        """
        获取轴向显示信息
        :return:
        """
        return cmds.getAttr(self.get_joint() + ".displayLocalAxis")

    def set_axisDisplay(self, sorh):
        """
        显示局部轴向
        :param sorh: True显示,False隐藏
        :return: self
        """
        cmds.setAttr(self.get_joint() + ".displayLocalAxis", sorh)
        return self

    def set_jointOrient(self, *args, **kwargs):
        """
        设置骨骼轴向
        :param args: aim_axis 主轴方向 0为X 1为Y 2为Z
        :param args: up_axis 次轴方向
        :param args: world_axis 次轴世界方向
        :return: self
        """
        aim_axis, up_axis, world_axis = args[0]
        joint = self.get_joint()
        # 获取子级，并放入世界层级下,并重新获取名称
        joint_childs = cmds.listRelatives(joint, c = True, type = ["joint", "transform"]) or []
        if joint_childs:
            joint_childs = cmds.parent(joint_childs, w = True)
        # 获取父级
        parent = cmds.listRelatives(joint, p = True)
        # 获取指向骨骼
        aim_joint = cmds.ls(joint_childs, type = "joint")
        # 使用目标约束设置方向
        if aim_joint:
            cmds.delete(
                cmds.aimConstraint(aim_joint[0], joint, aim = aim_axis, u = up_axis, wu = world_axis, wut = "vector",
                                   w = 1.0))
            # 冻结旋转
            cmds.joint(joint, e = True, zso = True)
            cmds.makeIdentity(joint, apply = True)
        elif parent is not None:
            # 不存在需要对齐的目标骨骼 则与父骨骼一致
            cmds.matchTransform(joint, parent[0], rot = True)
        if joint_childs:
            cmds.parent(joint_childs, joint)
        return self

    def set_offsetOrient(self, value):
        """
        设置偏移值
        :param value: [xx, xx, xx]
        :return: self
        """
        joint = self.get_joint()
        cmds.xform(joint, r = True, os = True, ra = value)
        cmds.joint(joint, e = True, zso = True)
        cmds.makeIdentity(joint, apply = True)
        return self

    def set_jointOrientToZero(self):
        """
        将骨骼的轴向值归零（与父级方向保持一致）
        :return: self
        """
        joint = self.get_joint()
        cmds.setAttr(joint + ".jointOrientX", 0)
        cmds.setAttr(joint + ".jointOrientY", 0)
        cmds.setAttr(joint + ".jointOrientZ", 0)
        return self


def set_selected_joint(*args, **kwargs):
    """
    获取所选骨骼，执行对应功能
    :param args:
    :param kwargs:
    :return:
    """
    joints = cmds.ls(sl = True, l = True, type = "joint")
    for jnt in joints:
        # 使用JointFn里的get方法保留骨骼相关的属性
        kwargs.update({key: getattr(JointFn(jnt), "get_" + key)() for key in args})
        JointFn(jnt, **kwargs)


@undo
def setJointAxisDisplay(sorh, children):
    """
    设置骨骼轴向显示
    :param sorh: bool True显示,False隐藏
    :param children: bool 包括子对象
    :return:
    """
    if children:
        cmds.select(selectAllJointByHierarchy(cmds.ls(sl = True, type = "joint")))
    set_selected_joint(ad = sorh)


@undo
def setJointOrient(*args, **kwargs):
    """
    设置骨骼轴向
    :param kwargs: aim_axis 主轴方向 0为X 1为Y 2为Z
    :param kwargs: aim_rev 主轴是否为负方向
    :param kwargs: up_axis 次轴方向
    :param kwargs: up_rev 次轴是否为负方向
    :param kwargs: world_axis 次轴世界方向
    :param kwargs: world_rev 次轴世界是否为负方向
    :param kwargs: children bool 包括子对象
    :return:
    """
    axis = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    children = kwargs.get("children")
    aim_rev = kwargs.get("aim_rev")
    aim_axis = [a * -1 if aim_rev else a for a in axis[kwargs.get("aim_axis")]]
    up_rev = kwargs.get("up_rev")
    up_axis = [a * -1 if up_rev else a for a in axis[kwargs.get("up_axis")]]
    world_rev = kwargs.get("world_rev")
    world_axis = [a * -1 if world_rev else a for a in axis[kwargs.get("world_axis")]]
    if children:
        cmds.select(selectAllJointByHierarchy(cmds.ls(sl = True, type = "joint")))
    set_selected_joint(jo = [aim_axis, up_axis, world_axis])


@undo
def setOffsetOrient(value, children):
    """
    设置偏移
    :param value: list 偏移值
    :param children: bool 包括子对象
    :return:
    """
    if children:
        cmds.select(selectAllJointByHierarchy(cmds.ls(sl = True, type = "joint")))
    set_selected_joint(oo = value)


@undo
def setJointOrientToZero(children):
    """
    将骨骼的轴向值归零（与父级方向保持一致）
    :param children: bool 包括子对象
    :return:
    """
    joints = cmds.ls(sl = True, type = "joint")
    if children:
        joints = selectAllJointByHierarchy(joints)
    for j in joints:
        JointFn(j).set_jointOrientToZero()
