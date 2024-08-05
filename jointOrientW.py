# -*- coding: UTF-8 -*-
# @FileName      : jointOrientW
# @Time          : 2024-07-31
# @Author        : LJF
# @Contact       : 906629272@qq.com
"""
骨骼方向设置面板
"""

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from . import uiWidget
from . import jointF


class JointOrientUI(QWidget):
    """
    骨骼方向设置UI
    """

    def __init__(self):
        QWidget.__init__(self)
        self.setObjectName("JointOrientWindow")

        self._createLabel()
        self._createRadioB()
        self._createPushButton()
        self._createSplitter()
        self._createLineEdit()
        self._createConnect()
        self._createLayout()

    def _createLabel(self):
        """
        说明标签
        :return:
        """
        qss = "QLabel { color: rgb(248, 244, 237); font: bold 10pt Microsoft YaHei; }"
        self.primary_axis = QLabel(u"主轴:")
        self.secondary_axis = QLabel(u"次轴:")
        self.secondary_axis_world = QLabel(u"次轴世界方向:")
        self.tweak_axis = QLabel(u"偏移旋转:")
        self.primary_axis.setStyleSheet(qss)
        self.secondary_axis.setStyleSheet(qss)
        self.secondary_axis_world.setStyleSheet(qss)
        self.tweak_axis.setStyleSheet(qss)
        # gif
        # self.gif_label = QLabel()
        # gif_movie = QMovie(__file__ + "/../res/images/important.gif", parent = self.gif_label)
        # gif_movie.setScaledSize(self.gif_label.size())
        # self.gif_label.setMovie(gif_movie)
        # gif_movie.start()

    def _createLineEdit(self):
        """
        输入框
        :return:
        """
        qss = """QLineEdit {
                              font: bold 8pt Microsoft YaHei;
                              color: rgb(248, 244, 237);
                              }
                            """
        self.tweak_line_x = QLineEdit()
        self.tweak_line_y = QLineEdit()
        self.tweak_line_z = QLineEdit()
        self.tweak_line_x.setText("0.0")
        self.tweak_line_y.setText("0.0")
        self.tweak_line_z.setText("0.0")
        self.tweak_line_x.setStyleSheet(qss)
        self.tweak_line_y.setStyleSheet(qss)
        self.tweak_line_z.setStyleSheet(qss)
        # 限制输入小数点后一位
        double_validator = QDoubleValidator(0.0, 2147483647.0, 1)
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        self.tweak_line_x.setValidator(double_validator)
        self.tweak_line_y.setValidator(double_validator)
        self.tweak_line_z.setValidator(double_validator)

    def _createRadioB(self):
        """
        复选框
        """
        qss = """QRadioButton {
                              font: bold 8pt Microsoft YaHei;
                              color: rgb(248, 244, 237);
                              }
                            """
        qss2 = """QCheckBox {
                              font: bold 8pt Microsoft YaHei;
                              color: rgb(248, 244, 237);
                              }
                            """
        # 子对象轴向显示
        self.display_axis_children = QCheckBox(u"包括子对象")
        self.display_axis_children.setStyleSheet(qss2)
        # 主轴
        self.primary_axis_x = QRadioButton(u"X")
        self.primary_axis_x.setChecked(True)
        self.primary_axis_y = QRadioButton(u"Y")
        self.primary_axis_z = QRadioButton(u"Z")
        self.primary_axis_revers = QCheckBox(u"反向")
        self.primary_axis_x.setStyleSheet(qss)
        self.primary_axis_y.setStyleSheet(qss)
        self.primary_axis_z.setStyleSheet(qss)
        self.primary_axis_revers.setStyleSheet(qss2)
        self.primary_axis_check_group = QButtonGroup()
        self.primary_axis_check_group.addButton(self.primary_axis_x, 0)
        self.primary_axis_check_group.addButton(self.primary_axis_y, 1)
        self.primary_axis_check_group.addButton(self.primary_axis_z, 2)
        self.primary_axis_check_group.setExclusive(True)
        # 次轴
        self.secondary_axis_x = QRadioButton(u"X")
        self.secondary_axis_y = QRadioButton(u"Y")
        self.secondary_axis_y.setChecked(True)
        self.secondary_axis_z = QRadioButton(u"Z")
        self.secondary_axis_revers = QCheckBox(u"反向")
        self.secondary_axis_x.setStyleSheet(qss)
        self.secondary_axis_y.setStyleSheet(qss)
        self.secondary_axis_z.setStyleSheet(qss)
        self.secondary_axis_revers.setStyleSheet(qss2)
        self.secondary_axis_check_group = QButtonGroup()
        self.secondary_axis_check_group.addButton(self.secondary_axis_x, 0)
        self.secondary_axis_check_group.addButton(self.secondary_axis_y, 1)
        self.secondary_axis_check_group.addButton(self.secondary_axis_z, 2)
        self.secondary_axis_check_group.setExclusive(True)
        # 次轴世界方向
        self.secondary_axis_world_x = QRadioButton(u"X")
        self.secondary_axis_world_y = QRadioButton(u"Y")
        self.secondary_axis_world_y.setChecked(True)
        self.secondary_axis_world_z = QRadioButton(u"Z")
        self.secondary_axis_world_revers = QCheckBox(u"反向")
        self.secondary_axis_world_x.setStyleSheet(qss)
        self.secondary_axis_world_y.setStyleSheet(qss)
        self.secondary_axis_world_z.setStyleSheet(qss)
        self.secondary_axis_world_revers.setStyleSheet(qss2)
        self.secondary_axis_world_check_group = QButtonGroup()
        self.secondary_axis_world_check_group.addButton(self.secondary_axis_world_x, 0)
        self.secondary_axis_world_check_group.addButton(self.secondary_axis_world_y, 1)
        self.secondary_axis_world_check_group.addButton(self.secondary_axis_world_z, 2)
        self.secondary_axis_world_check_group.setExclusive(True)
        # 确定子对象是否一起修改
        self.children_joint_orient = QCheckBox(u"包括子对象")
        self.children_joint_orient.setChecked(True)
        self.children_joint_orient.setStyleSheet(qss2)
        # 确定子对象是否一起旋转偏移
        self.children_tweak_axis = QCheckBox(u"包括子对象")
        self.children_tweak_axis.setStyleSheet(qss2)
        # 确定子对象轴向归零
        self.children_orient_to_zero = QCheckBox(u"包括子对象")
        self.children_orient_to_zero.setStyleSheet(qss2)

    def _createPushButton(self):
        """
        创建按钮
        :return:
        """
        # 加载按钮的qss
        with open(__file__ + "/../res/qss/QPushButtonA.qss", "r") as f:
            qss = f.read()
        # 显示轴向
        self.display_axis_btn_s = QPushButton(u"局部轴向显示")
        self.display_axis_btn_s.setFixedHeight(35)
        self.display_axis_btn_s.setStyleSheet(qss)
        # 隐藏轴向
        self.display_axis_btn_h = QPushButton(u"局部轴向隐藏")
        self.display_axis_btn_h.setFixedHeight(35)
        self.display_axis_btn_h.setStyleSheet(qss)
        # 修改方向
        self.set_joint_orient = QPushButton(u"修改方向")
        self.set_joint_orient.setFixedHeight(35)
        self.set_joint_orient.setStyleSheet(qss)
        # 偏移增加
        self.tweak_orient_p = QPushButton(u"+")
        self.tweak_orient_p.setFixedHeight(35)
        self.tweak_orient_p.setStyleSheet(qss)
        # 偏移减少
        self.tweak_orient_s = QPushButton(u"-")
        self.tweak_orient_s.setFixedHeight(35)
        self.tweak_orient_s.setStyleSheet(qss)
        # 轴向归零
        self.set_orient_to_zero = QPushButton(u"方向偏移归零")
        self.set_orient_to_zero.setFixedHeight(35)
        self.set_orient_to_zero.setStyleSheet(qss)

    def _createSplitter(self):
        """
        分割线
        """
        self.splitter1 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)
        self.splitter2 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)
        self.splitter3 = uiWidget.Splitter(rgb = (54, 52, 61), w = self.width(), h = 10)

    def _createConnect(self):
        """
        信号连接
        :return:
        """
        self.display_axis_btn_s.clicked.connect(lambda x: self._jointAxisDisplayConnect(True))
        self.display_axis_btn_h.clicked.connect(lambda x: self._jointAxisDisplayConnect(False))
        self.set_joint_orient.clicked.connect(self._setJointOrientConnect)
        self.tweak_orient_p.clicked.connect(lambda x: self._setOffsetOrient(1))
        self.tweak_orient_s.clicked.connect(lambda x: self._setOffsetOrient(-1))
        self.set_orient_to_zero.clicked.connect(self._setJointOrientToZero)

    def _jointAxisDisplayConnect(self, sorh):
        """
        显示骨骼局部轴向
        :param sorh: True显示,False隐藏
        :return:
        """
        children = self.display_axis_children.checkState()
        jointF.setJointAxisDisplay(sorh, children)

    def _setJointOrientConnect(self):
        """
        设置骨骼轴向
        :return:
        """
        jointF.setJointOrient(children = self.children_joint_orient.checkState(),
                              aim_axis = self.primary_axis_check_group.checkedId(),
                              aim_rev = self.primary_axis_revers.checkState(),
                              up_axis = self.secondary_axis_check_group.checkedId(),
                              up_rev = self.secondary_axis_revers.checkState(),
                              world_axis = self.secondary_axis_world_check_group.checkedId(),
                              world_rev = self.secondary_axis_world_revers.checkState())

    def _setJointOrientToZero(self):
        """
        将骨骼的轴向值归零（与父级方向保持一致）
        :return:
        """
        jointF.setJointOrientToZero(self.children_orient_to_zero.checkState())

    def _setOffsetOrient(self, pors):
        """
        设置偏移
        :param pors: fl 加还是减
        :return:
        """
        value = [float(self.tweak_line_x.text()), float(self.tweak_line_y.text()), float(self.tweak_line_z.text())]
        value = [v * pors for v in value]
        jointF.setOffsetOrient(value, self.children_tweak_axis.checkState())

    def _createLayout(self):
        """
        创建布局
        :return:
        """
        self.main_layout = QVBoxLayout()
        self.main_layout.setObjectName("JOMLayout")
        self.setLayout(self.main_layout)

        self.display_layout = QHBoxLayout()
        self.main_layout.addLayout(self.display_layout)
        self.display_layout.addWidget(self.display_axis_btn_s, 3)
        self.display_layout.addWidget(self.display_axis_btn_h, 3)
        self.display_layout.addWidget(self.display_axis_children, 1)
        self.main_layout.addWidget(self.splitter1)

        self.axis_check_layout = QGridLayout()
        self.main_layout.addLayout(self.axis_check_layout)
        self.axis_check_layout.addWidget(self.primary_axis, 0, 0)
        self.axis_check_layout.addWidget(self.primary_axis_x, 0, 1)
        self.axis_check_layout.addWidget(self.primary_axis_y, 0, 2)
        self.axis_check_layout.addWidget(self.primary_axis_z, 0, 3)
        self.axis_check_layout.addWidget(self.primary_axis_revers, 0, 4)
        self.axis_check_layout.addWidget(self.secondary_axis, 1, 0)
        self.axis_check_layout.addWidget(self.secondary_axis_x, 1, 1)
        self.axis_check_layout.addWidget(self.secondary_axis_y, 1, 2)
        self.axis_check_layout.addWidget(self.secondary_axis_z, 1, 3)
        self.axis_check_layout.addWidget(self.secondary_axis_revers, 1, 4)
        self.axis_check_layout.addWidget(self.secondary_axis_world, 2, 0)
        self.axis_check_layout.addWidget(self.secondary_axis_world_x, 2, 1)
        self.axis_check_layout.addWidget(self.secondary_axis_world_y, 2, 2)
        self.axis_check_layout.addWidget(self.secondary_axis_world_z, 2, 3)
        self.axis_check_layout.addWidget(self.secondary_axis_world_revers, 2, 4)

        self.main_layout.addWidget(self.children_joint_orient)
        self.main_layout.setAlignment(self.children_joint_orient, Qt.AlignHCenter)
        self.main_layout.addWidget(self.set_joint_orient)
        self.main_layout.addWidget(self.splitter2)

        self.tweak_layout = QHBoxLayout()
        self.main_layout.addLayout(self.tweak_layout)
        self.tweak_layout.addWidget(self.tweak_axis, 2)
        self.tweak_layout.addWidget(self.tweak_line_x, 2)
        self.tweak_layout.addWidget(self.tweak_line_y, 2)
        self.tweak_layout.addWidget(self.tweak_line_z, 2)
        self.tweak_layout.addWidget(self.children_tweak_axis, 3)
        self.tweak_layout.setAlignment(self.tweak_axis, Qt.AlignHCenter)
        self.tweak_layout.setAlignment(self.tweak_line_x, Qt.AlignHCenter)
        self.tweak_layout.setAlignment(self.tweak_line_y, Qt.AlignHCenter)
        self.tweak_layout.setAlignment(self.tweak_line_z, Qt.AlignHCenter)
        self.tweak_layout.setAlignment(self.children_tweak_axis, Qt.AlignHCenter)
        self.tweak_layout2 = QHBoxLayout()
        self.main_layout.addLayout(self.tweak_layout2)
        self.tweak_layout2.addWidget(self.tweak_orient_p)
        self.tweak_layout2.addWidget(self.tweak_orient_s)
        self.set_orient_layout = QHBoxLayout()
        self.main_layout.addLayout(self.set_orient_layout)
        self.set_orient_layout.addWidget(self.set_orient_to_zero, 4)
        self.set_orient_layout.addWidget(self.children_orient_to_zero, 1)
        self.main_layout.addWidget(self.splitter3)
        # self.main_layout.addWidget(self.gif_label)
        # self.main_layout.setAlignment(self.gif_label, Qt.AlignHCenter)

        # 布局末端添加一个空项，将所有子部件往上挤
        self.main_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.Expanding))
