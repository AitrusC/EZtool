# -*- coding: UTF-8 -*-
# @FileName      : motionP
# @Time          : 2024-07-10
# @Author        : LJF
# @Contact       : 906629272@qq.com
"""
路径控制器面板
"""
import maya.cmds as cmds
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from . import motionTool
from . import uiWidget


# major_version = sys.version_info.major
#
#
# def mayaToPyside(widget):
#     """
#     将mayaUI转为pyside2对象
#     :param widget: ui
#     :return: pyside2
#     """
#     ptr = omui.MQtUtil.findControl(widget)
#     if ptr is None:
#         ptr = omui.MQtUtil.findLayout(widget)
#     if ptr is None:
#         ptr = omui.MQtUtil.findMenuItem(widget)
#     if ptr is None:
#         ptr = omui.MQtUtil.findWindow(widget)
#     if major_version == 2:
#         ret = wrapInstance(long(ptr), QWidget)
#     if major_version == 3:
#         ret = wrapInstance(int(ptr), QWidget)
#     return ret

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


def addCurve(btn):
    """
    添加曲线
    :param btn: uiWidget.LineEditPBtn
    :return:
    """
    curve = motionTool.selectedCurve()
    if curve:
        btn.cleanText()
        btn.setText(curve)
    else:
        btn.cleanText()


class MotionPUI(QWidget):
    """

    """

    def __init__(self):
        QWidget.__init__(self)
        self.setObjectName("MotionPWindow")
        # self.deleteMayaWidget()

        self._createLineEditPBtn()
        self._createLabel()
        self._createLineEdit()
        self._createPushBtn()
        self._createRadioB()
        self._createSplitter()
        self._createCollapsibleBox()
        self._createConnect()
        self._createLayout()
        # self._createMayaWidget()

    # def deleteMayaWidget(self):
    #     """
    #     删除maya的控件
    #     :return:
    #     """
    #     if cmds.layout("rigFrameL", exists = True):
    #         cmds.deleteUI("rigFrameL", lay = True)
    #     if cmds.layout("rigColumnL", exists = True):
    #         cmds.deleteUI("rigColumnL", lay = True)
    #     if cmds.control("numberOfJointsGrp", exists = True):
    #         cmds.deleteUI("numberOfJointsGrp", ctl = True)
    #     if cmds.control("numberOfControlsGrp", exists = True):
    #         cmds.deleteUI("numberOfControlsGrp", ctl = True)

    def _createLabel(self):
        """
        标签
        """
        qss = "QLabel { color: rgb(248, 244, 237); font: bold 10pt Microsoft YaHei; }"
        self.set_name_lb = QLabel(u"设置名字:")
        self.set_name_lb.setStyleSheet(qss)
        self.set_obj_direction = QLabel(u"设置朝向:")
        self.set_obj_direction.setStyleSheet(qss)
        # 绑定设置
        self.rig_num_joints_lb = QLabel(u"骨骼数量:")
        self.rig_num_control_lb = QLabel(u"控制器数量:")
        self.rig_num_joints_lb.setStyleSheet(qss)
        self.rig_num_control_lb.setStyleSheet(qss)
        # 动画设置
        self.anim_start_frame_lb = QLabel(u"开始帧:")
        self.anim_end_frame_lb = QLabel(u"结束帧:")
        self.anim_speed_lb = QLabel(u"运动速度(cm/F):")
        self.anim_wave_axis = QLabel(u"摆动轴向:")
        self.anim_wave_length_lb = QLabel(u"波动长度:")
        self.anim_wave_amplitude_lb = QLabel(u"波动幅度:")
        self.anim_wave_rate_lb = QLabel(u"波动频率:")
        self.anim_start_frame_lb.setStyleSheet(qss)
        self.anim_end_frame_lb.setStyleSheet(qss)
        self.anim_speed_lb.setStyleSheet(qss)
        self.anim_wave_axis.setStyleSheet(qss)
        self.anim_wave_length_lb.setStyleSheet(qss)
        self.anim_wave_amplitude_lb.setStyleSheet(qss)
        self.anim_wave_rate_lb.setStyleSheet(qss)

    def _createLineEdit(self):
        """
        输入框
        """
        qss = "QLineEdit { font: bold 8pt Microsoft YaHei; color: rgb(248, 244, 237); }"
        self.set_name_le = QLineEdit()
        self.set_name_le.setStyleSheet(qss)
        # 绑定设置
        self.rig_num_joints_le = QLineEdit()
        self.rig_num_control_le = QLineEdit()
        self.rig_num_joints_le.setStyleSheet(qss)
        self.rig_num_control_le.setStyleSheet(qss)
        # 设置rig_num_joints_le初始值为15，并且只能输入整数
        self.rig_num_joints_le.setText("15")
        self.rig_num_joints_le.setValidator(QIntValidator())
        self.rig_num_control_le.setText("6")
        self.rig_num_control_le.setValidator(QIntValidator())
        # 动画设置
        self.anim_start_frame_le = QLineEdit()
        self.anim_end_frame_le = QLineEdit()
        self.anim_speed_le = QLineEdit()
        self.anim_wave_length_le = QLineEdit()
        self.anim_wave_amplitude_le = QLineEdit()
        self.anim_wave_rate_le = QLineEdit()
        self.anim_start_frame_le.setStyleSheet(qss)
        self.anim_end_frame_le.setStyleSheet(qss)
        self.anim_speed_le.setStyleSheet(qss)
        self.anim_wave_length_le.setStyleSheet(qss)
        self.anim_wave_amplitude_le.setStyleSheet(qss)
        self.anim_wave_rate_le.setStyleSheet(qss)
        # 设置输入值为小数点后一位
        self.anim_start_frame_le.setText("0.0")
        self.anim_end_frame_le.setText("2000.0")
        self.anim_speed_le.setText("1.0")
        self.anim_wave_length_le.setText("4.0")
        self.anim_wave_amplitude_le.setText("1.0")
        self.anim_wave_rate_le.setText("1.0")
        double_validator = QDoubleValidator(0.0, 2147483647.0, 1)
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        self.anim_start_frame_le.setValidator(double_validator)
        self.anim_end_frame_le.setValidator(double_validator)
        self.anim_speed_le.setValidator(double_validator)
        self.anim_wave_length_le.setValidator(double_validator)
        self.anim_wave_amplitude_le.setValidator(double_validator)
        self.anim_wave_rate_le.setValidator(double_validator)

    # def _createMayaWidget(self):
    #     """
    #     mayaUI工具
    #     :return:
    #     """
    #     cmds.setParent("rigColumnL")
    #     number_joints = cmds.intFieldGrp("numberOfJointsGrp", label = u"骨骼数量", numberOfFields = 1, value1 = 15)
    #     pyside_number_joints = mayaToPyside(number_joints)
    #     cmds.setParent("rigColumnL")
    #     number_controls = cmds.intFieldGrp("numberOfControlsGrp", label = "Number of Controls", numberOfFields = 1,
    #                                        value1 = 5)
    #     pyside_number_controls = mayaToPyside(number_controls)
    #     self.rig_pyside_column.layout().addWidget(pyside_number_joints)
    #     self.rig_pyside_column.layout().addWidget(pyside_number_controls)

    def _createPushBtn(self):
        """
        按钮
        :return:
        """
        with open(__file__ + "/../res/qss/QPushButtonA.qss", "r") as f:
            qss = f.read()
        self.create_rig_btn = QPushButton(u"绑定生成")
        self.create_rig_btn.setFixedHeight(35)
        self.create_rig_btn.setStyleSheet(qss)
        self.create_path_btn = QPushButton(u"创建路径控制")
        self.create_path_btn.setFixedHeight(35)
        self.create_path_btn.setStyleSheet(qss)
        self.create_animation = QPushButton(u"生成动画")
        self.create_animation.setFixedHeight(35)
        self.create_animation.setStyleSheet(qss)

    def _createLineEditPBtn(self):
        """
        选择添加
        :return:
        """
        self.add_curve_btn = uiWidget.LineEditPBtn(u"加载曲线:", width = 90)
        self.add_curve_btn.line.setReadOnly(True)
        self.add_path_curve_btn = uiWidget.LineEditPBtn(u"加载路径曲线:", width = 130)
        self.add_path_curve_btn.line.setReadOnly(True)
        self.add_driven_curve_btn = uiWidget.LineEditPBtn(u"加载驱动曲线:", width = 130)
        self.add_driven_curve_btn.line.setReadOnly(True)

    def _createRadioB(self):
        """
        选框
        """
        qss = """QRadioButton {
                              font: bold 8pt Microsoft YaHei;
                              color: rgb(248, 244, 237);
                              }
                            """
        self.checkB1 = QRadioButton(u"X")
        self.checkB1.setChecked(True)
        self.checkB2 = QRadioButton(u"Y")
        self.checkB3 = QRadioButton(u"Z")
        self.checkB1.setStyleSheet(qss)
        self.checkB2.setStyleSheet(qss)
        self.checkB3.setStyleSheet(qss)
        self.checkGroup = QButtonGroup()
        self.checkGroup.addButton(self.checkB1, 1)
        self.checkGroup.addButton(self.checkB2, 2)
        self.checkGroup.addButton(self.checkB3, 3)
        self.checkGroup.setExclusive(True)

        self.check_curve_x = QRadioButton(u"X")
        self.check_curve_x.setChecked(True)
        self.check_curve_y = QRadioButton(u"Y")
        self.check_curve_z = QRadioButton(u"Z")
        self.check_curve_x.setStyleSheet(qss)
        self.check_curve_y.setStyleSheet(qss)
        self.check_curve_z.setStyleSheet(qss)
        self.check_curve_group = QButtonGroup()
        self.check_curve_group.addButton(self.check_curve_x, 1)
        self.check_curve_group.addButton(self.check_curve_y, 2)
        self.check_curve_group.addButton(self.check_curve_z, 3)
        self.check_curve_group.setExclusive(True)

    def _createSplitter(self):
        """
        分割线
        """
        self.splitter1 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)
        self.splitter2 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)
        self.splitter3 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)

    def _createCollapsibleBox(self):
        """
        折叠控件
        :return:
        """
        # 绑定设置
        self.rig_collapsible = uiWidget.CollapsibleBox(u"绑定设置")
        self.rig_vbox_layout_m = QVBoxLayout()
        self.rig_hbox_layout1 = QHBoxLayout()
        self.rig_vbox_layout_m.addLayout(self.rig_hbox_layout1)
        self.rig_hbox_layout2 = QHBoxLayout()
        self.rig_vbox_layout_m.addLayout(self.rig_hbox_layout2)

        self.rig_hbox_layout1.addWidget(self.rig_num_joints_lb, 1)
        self.rig_hbox_layout1.addWidget(self.rig_num_joints_le, 3)
        self.rig_hbox_layout2.addWidget(self.rig_num_control_lb, 1)
        self.rig_hbox_layout2.addWidget(self.rig_num_control_le, 3)

        self.rig_vbox_layout_m.addWidget(self.create_rig_btn)

        self.rig_collapsible.setContentLayout(self.rig_vbox_layout_m)

        # 路径控制
        self.path_collapsible = uiWidget.CollapsibleBox(u"路径设置")
        self.path_vbox_layout_m = QVBoxLayout()
        self.path_vbox_layout_m.addWidget(self.add_path_curve_btn)
        self.path_vbox_layout_m.addWidget(self.add_driven_curve_btn)
        self.path_vbox_layout_m.addWidget(self.create_path_btn)

        self.path_collapsible.setContentLayout(self.path_vbox_layout_m)
        # 动画设置
        self.anim_collapsible = uiWidget.CollapsibleBox(u"动画设置")
        self.anim_vbox_layout_m = QVBoxLayout()

        self.anim_grid_layout = QGridLayout()
        self.anim_vbox_layout_m.addLayout(self.anim_grid_layout)
        self.anim_grid_layout.addWidget(self.anim_start_frame_lb, 0, 0)
        self.anim_grid_layout.addWidget(self.anim_start_frame_le, 0, 1)
        self.anim_grid_layout.addWidget(self.anim_end_frame_lb, 1, 0)
        self.anim_grid_layout.addWidget(self.anim_end_frame_le, 1, 1)
        self.anim_grid_layout.addWidget(self.anim_speed_lb, 2, 0)
        self.anim_grid_layout.addWidget(self.anim_speed_le, 2, 1)
        self.anim_grid_layout.addWidget(self.anim_wave_length_lb, 3, 0)
        self.anim_grid_layout.addWidget(self.anim_wave_length_le, 3, 1)
        self.anim_grid_layout.addWidget(self.anim_wave_amplitude_lb, 4, 0)
        self.anim_grid_layout.addWidget(self.anim_wave_amplitude_le, 4, 1)
        self.anim_grid_layout.addWidget(self.anim_wave_rate_lb, 5, 0)
        self.anim_grid_layout.addWidget(self.anim_wave_rate_le, 5, 1)

        self.anim_hbox_layout1 = QHBoxLayout()
        self.anim_vbox_layout_m.addLayout(self.anim_hbox_layout1)
        self.anim_hbox_layout1.addWidget(self.anim_wave_axis)
        self.anim_hbox_layout1.addWidget(self.checkB1)
        self.anim_hbox_layout1.addWidget(self.checkB2)
        self.anim_hbox_layout1.addWidget(self.checkB3)

        self.anim_vbox_layout_m.addWidget(self.create_animation)

        self.anim_collapsible.setContentLayout(self.anim_vbox_layout_m)

    def _create_rig_btn_connect(self):
        """
        self.create_rig_btn的执行
        :return:
        """
        name = self.set_name_le.text()
        ref_curve = self.add_curve_btn.getText()
        joint_num = int(self.rig_num_joints_le.text())
        motionTool.createCurve(name, ref_curve, joint_num)

    def _createConnect(self):
        """
        信号连接
        :return:
        """
        self.add_curve_btn.button.clicked.connect(lambda x: addCurve(self.add_curve_btn))
        self.add_path_curve_btn.button.clicked.connect(lambda x: addCurve(self.add_path_curve_btn))
        self.add_driven_curve_btn.button.clicked.connect(lambda x: addCurve(self.add_driven_curve_btn))
        self.create_rig_btn.clicked.connect(self._create_rig_btn_connect)

    def _createLayout(self):
        """

        :return:
        """
        self.main_layout = QVBoxLayout()
        # 必须加上名字，并且在创建maya widget的时候使用这个名字设置父对象，不然maya widget会找不到父对象
        self.main_layout.setObjectName("MPWmainL")
        self.setLayout(self.main_layout)

        self.hbLayout1 = QHBoxLayout()
        self.main_layout.addLayout(self.hbLayout1)
        self.hbLayout1.addWidget(self.set_name_lb, 1)
        self.hbLayout1.addWidget(self.set_name_le, 3)
        self.main_layout.addWidget(self.add_curve_btn)
        self.curve_hbox_layout = QHBoxLayout()
        self.main_layout.addLayout(self.curve_hbox_layout)
        self.curve_hbox_layout.addWidget(self.set_obj_direction)
        self.curve_hbox_layout.addWidget(self.check_curve_x)
        self.curve_hbox_layout.addWidget(self.check_curve_y)
        self.curve_hbox_layout.addWidget(self.check_curve_z)
        self.main_layout.addWidget(self.splitter1)
        self.main_layout.addWidget(self.rig_collapsible)
        self.main_layout.addWidget(self.splitter2)
        self.main_layout.addWidget(self.path_collapsible)
        self.main_layout.addWidget(self.splitter3)
        self.main_layout.addWidget(self.anim_collapsible)

        self.main_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.Expanding))

        # # 创建maya里的frameLayout布局
        # frame_qss = "QLayout { font: bold 8pt Microsoft YaHei; color: rgb(248, 244, 237); }"
        # # 设置父布局
        # cmds.setParent("MPWmainL")
        # rig_maya_frame = cmds.frameLayout("rigFrameL", w = 230, cll = True, cl = True, l = u"绑定设置")
        # self.rig_pyside_frame = mayaToPyside(rig_maya_frame)
        # self.rig_pyside_frame.setStyleSheet(frame_qss)
        # self.main_layout.addWidget(self.rig_pyside_frame)
        # cmds.setParent("rigFrameL")
        # rig_maya_column = cmds.columnLayout("rigColumnL", rowSpacing = 0)
        # self.rig_pyside_column = mayaToPyside(rig_maya_column)
        # self.rig_pyside_frame.layout().addWidget(self.rig_pyside_column)
