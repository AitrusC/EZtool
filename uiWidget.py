# coding=utf-8
# @FileName      :uiWidget
# @Time          :2023/8/31 22:01
# @Author        :AhrIlI
# @Contact       :906629272@qq.com

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


def setLuminance(rgb, uord, percent):
    """
    将rgb转为yuv改变y值来提高或降低原rgb的明度
    :param rgb: rgb数值
    :param uord: 提高或降低(T or F)
    :param percent: 提高或降低多少(0~1)
    :return:
    """
    r, g, b = rgb
    y = ((66 * r + 129 * g + 25 * b + 128) >> 8) + 16
    u = ((-38 * r - 74 * g + 112 * b + 128) >> 8) + 128
    v = ((112 * r - 94 * g - 18 * b + 128) >> 8) + 128
    outcolor = rgb
    if uord:
        ud_y = round(min(235, y * (1 + percent)))
    else:
        ud_y = round(max(16, y * (1 - percent)))
    ud_y = int(ud_y)
    c = ud_y - 16
    d = u - 128
    e = v - 128
    ud_r = (298 * c + 409 * e + 128) >> 8
    ud_g = (298 * c - 100 * d - 208 * e + 128) >> 8
    ud_b = (298 * c + 516 * d + 128) >> 8
    outcolor = (ud_r, ud_g, ud_b)
    return outcolor


class TadWidget(QWidget):
    u"""
    侧边栏
    """

    def __init__(self):
        super(TadWidget, self).__init__()
        self.setObjectName("TadWidget")
        self.set_size = QSize(50, 50)
        # 整体布局
        self.main_layout = QHBoxLayout(spacing = 0)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.left_widget = QListWidget()
        self.right_widget = QStackedWidget()
        self.main_layout.addWidget(self.left_widget)
        self.main_layout.addWidget(self.right_widget)
        # 去边框
        self.left_widget.setFrameShape(QListWidget.NoFrame)
        # 隐藏滚动条
        self.left_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.left_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.left_widget.setIconSize(QSize(40, 40))

        self.left_widget.currentRowChanged.connect(self.right_widget.setCurrentIndex)

    def addInsertItem(self, left_item, right_item):
        u"""
        :param left_item: 左边的文本栏
        :param right_item: 右边显示的控件
        """
        for i, o in zip(left_item, right_item):
            self.item = QListWidgetItem(self.left_widget)
            self.item.setIcon(i)
            self.item.setSizeHint(self.set_size)
            self.item.setTextAlignment(Qt.AlignCenter)

            self.right_widget.addWidget(o)

    def leftwSize(self, size):
        u"""
        图标大小
        :param size: QSize
        """
        self.set_size = size

    def setStyleSheetLR(self, **kwargs):
        """
        设置样式
        :param lqss:
        :param rqss:
        :return:
        """
        lqss = None
        rqss = None
        for key in kwargs:
            if key == "lqss":
                lqss = kwargs.get(key)
            if key == "rqss":
                rqss = kwargs.get(key)
        if lqss is not None:
            self.left_widget.setStyleSheet(lqss)
        if rqss is not None:
            self.right_widget.setStyleSheet(rqss)


class TextSliderBtnE(QWidget):
    """
    在滑动按钮右侧添加文字
    """

    def __init__(self, **kwargs):
        """
        参数与滑动按钮一致，多添加text,tcolor,参数设置文本与文字颜色(默认rgb(255, 254, 250))
        """
        QWidget.__init__(self)
        # 背景色
        self._grcolor_off = (89, 89, 89)
        self._grcolor_on = (200, 222, 255)
        # 圆的颜色
        self._slidercolor_off = (193, 205, 205)
        self._slidercolor_on = (50, 155, 255)
        # 文字颜色
        self.tcolor = (255, 254, 250)
        for key in kwargs:
            if key == "w":
                self.w = kwargs.get(key)
                continue
            if key == "h":
                self.h = kwargs.get(key)
                continue
            if key == "grcoff":
                self._grcolor_off = (kwargs.get(key)[0], kwargs.get(key)[1], kwargs.get(key)[2])
                continue
            if key == "grcon":
                self._grcolor_on = (kwargs.get(key)[0], kwargs.get(key)[1], kwargs.get(key)[2])
                continue
            if key == "slcoff":
                self._slidercolor_off = (kwargs.get(key)[0], kwargs.get(key)[1], kwargs.get(key)[2])
                continue
            if key == "slcon":
                self._slidercolor_on = (kwargs.get(key)[0], kwargs.get(key)[1], kwargs.get(key)[2])
                continue
            if key == "text":
                self.text = kwargs.get(key)
                continue
            if key == "tcolor":
                self.tcolor = kwargs.get(key)
                continue
        self.btn = SliderBtnE(w = self.w, h = self.h, grcoff = self._grcolor_off, grcon = self._grcolor_on,
                              slcoff = self._slidercolor_off, slcon = self._slidercolor_on)
        self.label = QLabel(self.text)
        self.label.setStyleSheet(
            "color: rgb({0}, {1}, {2}); font: bold 10pt Microsoft YaHei".format(self.tcolor[0], self.tcolor[1],
                                                                                self.tcolor[2]))
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(Qt.AlignVCenter)
        self.main_layout.addWidget(self.btn)
        self.main_layout.addWidget(self.label)


class SliderBtnE(QAbstractButton):
    u"""
    滑动按钮
    """
    toggled = Signal(bool)

    def __init__(self, **kwargs):
        u"""

        :param w: 宽
        :param h: 高
        :param grcoff : 关闭状态下背景的颜色(默认rgb(89, 89, 89))
        :param grcon : 打开状态下背景的颜色(默认rgb(200, 222, 255))
        :param slcoff : 关闭状态下按钮的颜色(默认rgb(193, 205, 205))
        :param slcon : 打开状态下按钮的颜色(默认rgb(50, 155, 255))
        """
        QAbstractButton.__init__(self)
        # 背景色
        self._grcolor_off = QColor(89, 89, 89)
        self._grcolor_on = QColor(200, 222, 255)
        # 圆的颜色
        self._slidercolor_off = QColor(193, 205, 205)
        self._slidercolor_on = QColor(50, 155, 255)
        for key in kwargs:
            if key == "w":
                self.w = kwargs.get(key)
                continue
            if key == "h":
                self.h = kwargs.get(key)
                continue
            if key == "grcoff":
                if kwargs.get(key) is None:
                    continue
                self._grcolor_off = QColor(kwargs.get(key)[0], kwargs.get(key)[1], kwargs.get(key)[2])
                continue
            if key == "grcon":
                if kwargs.get(key) is None:
                    continue
                self._grcolor_on = QColor(kwargs.get(key)[0], kwargs.get(key)[1], kwargs.get(key)[2])
                continue
            if key == "slcoff":
                if kwargs.get(key) is None:
                    continue
                self._slidercolor_off = QColor(kwargs.get(key)[0], kwargs.get(key)[1], kwargs.get(key)[2])
                continue
            if key == "slcon":
                if kwargs.get(key) is None:
                    continue
                self._slidercolor_on = QColor(kwargs.get(key)[0], kwargs.get(key)[1], kwargs.get(key)[2])
                continue
        # 关于在布局中布显示的问题，设置下面这个属性固定按键大小，或重写sizeHint方法
        self.setFixedSize(self.w, self.h)
        # self.resize(50, 25)
        self._checked = False
        # 内部圆直径
        self._innerDiameter = self.height() * 0.75
        # 内部圆与背景的边距
        self._innerMargin = (self.height() - self._innerDiameter) / 2
        # x坐标的偏移值
        self._offset = self._innerMargin
        # 定时器
        self._time_id = None

    def sizeHint(self):
        # 重写sizeHint方法
        return QSize(self.w, self.h)

    def paintEvent(self, event):
        pain = QPainter()
        pain.begin(self)
        pain.setPen(Qt.NoPen)
        # 抗锯齿
        pain.setRenderHint(QPainter.Antialiasing)
        # 颜色状态
        if self._checked:
            grcolor = self._grcolor_on
            slidercolor = self._slidercolor_on
        else:
            grcolor = self._grcolor_off
            slidercolor = self._slidercolor_off
        # 画个圆角矩形
        pain.setBrush(QBrush(grcolor))
        pain.drawRoundedRect(self.rect(), self.height() / 2, self.height() / 2)
        # 画个圆
        pain.setBrush(QBrush(slidercolor))
        pain.drawEllipse(QRectF(self._offset, self._innerMargin, self._innerDiameter, self._innerDiameter))

        pain.end()

    def timerEvent(self, event):
        if self._checked:
            self._offset += 1
            if self._offset > (self.width() - self._innerDiameter - self._innerMargin):
                self.killTimer(self._time_id)
        else:
            self._offset -= 1
            if self._offset < self._innerMargin:
                self.killTimer(self._time_id)
        self.update()

    def killTimer(self, time_id):
        QAbstractButton.killTimer(self, time_id)
        self._time_id = None

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._checked = not self._checked
            self.toggled.emit(self._checked)
            if self._time_id:
                self.killTimer(self._time_id)
            self._time_id = self.startTimer(5)

    def setChecked(self, torf):
        """
        改变按钮状态
        :param torf: bool
        :return:
        """
        QAbstractButton.setChecked(self, torf)
        if self._checked != torf:
            self._checked = torf
            self.toggled.emit(self._checked)
            if self._time_id:
                self.killTimer(self._time_id)
            self._time_id = self.startTimer(5)

    def getChecked(self):
        u"""
        获取按钮状态,默认False
        :return:
        """
        return self._checked


class RoundBtn(QAbstractButton):
    u"""
    圆形按钮
    """
    NORMAL, HOVER, PRESS = range(3)
    clicked = Signal()

    def __init__(self, radius = None, grcolor = None):
        u"""

        :param radius: 半径
        :param grcolor: 颜色(RGB)
        :param parent:
        """
        super(RoundBtn, self).__init__()
        self.rgb_v = grcolor
        self._state = self.NORMAL
        self._radius = radius
        self.setFixedSize(self._radius, self._radius)

    def sizeHint(self):
        return QSize(self._radius, self._radius)

    def set_state(self, enum):
        """
        获取控件事件更新窗体
        :param enum:
        :return:
        """
        self._state = enum
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.set_state(self.PRESS)

    def mouseReleaseEvent(self, event):
        if self.rect().contains(event.pos()):
            self.set_state(self.HOVER)
        else:
            self.set_state(self.NORMAL)
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    def enterEvent(self, event):
        self.set_state(self.HOVER)
        super(RoundBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        self.set_state(self.NORMAL)
        super(RoundBtn, self).leaveEvent(event)

    def paintEvent(self, event):
        # 设置颜色
        background_color = QColor(self.rgb_v[0], self.rgb_v[1], self.rgb_v[2])
        if self._state == self.HOVER:
            background_color = setLuminance(self.rgb_v, True, 0.25)
            background_color = QColor(background_color[0], background_color[1], background_color[2])
        elif self._state == self.PRESS:
            background_color = setLuminance(self.rgb_v, True, 0.50)
            background_color = QColor(background_color[0], background_color[1], background_color[2])
        # 画
        pain = QPainter()
        pain.begin(self)
        pain.setPen(Qt.NoPen)
        # 抗锯齿
        pain.setRenderHint(QPainter.Antialiasing)
        # 画个圆
        pain.setBrush(QBrush(background_color))
        pain.drawEllipse(QRectF(QPoint(0, 0), QSizeF(self.width(), self.height())))

        pain.end()


class Splitter(QWidget):
    u"""
    --------XXXXXXX--------
    类似这样的分割线,如果没有设置文字就是纯直线
    """

    def __init__(self, **kwargs):
        u"""
        :param text: 设置中间显示的文字
        :param w: 分割线总体宽度
        :param h: 分割线总体高度(和其他部件的间距)
        :param rgb: 颜色(默认rgb(226, 225, 228))
        """
        super(Splitter, self).__init__()
        self.rgb = "rgb(226, 225, 228)"
        self.text = None

        for key in kwargs:
            if key == "text":
                self.text = kwargs.get(key)
                continue
            if key == "w":
                self.w = kwargs.get(key)
                continue
            if key == "h":
                self.h = kwargs.get(key)
                continue
            if key == "rgb":
                self.rgb = "rgb({0}, {1}, {2})".format(kwargs.get(
                    key)[0], kwargs.get(key)[1], kwargs.get(key)[2])
                continue
        # 设置分割线与其他部件的间隔
        self.resize(self.w, self.h)
        self.setMinimumHeight(5)

        self._createLabel(self.text)
        self._addSplitter()
        self._createLayouts()

    def _createLabel(self, text):
        """
        设置中间显示的文字
        :param text:
        :return:
        """
        self.text_label = QLabel()
        self.text_label.setText(text)
        self.text_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.text_label.setStyleSheet("color: rgb(248, 244, 237); font: bold 10pt Microsoft YaHei;")
        self.setMinimumHeight(self.h)

    def _addSplitter(self):
        """
        添加分割线
        :return:
        """
        splitter_style = """QFrame {{
                            border: 0px solid {0};
                            border-radius: 10px;
                            background-color: {1};
                            }}
                            """.format(self.rgb, self.rgb)
        self.first_line = QFrame()
        self.first_line.setFrameStyle(QFrame.HLine)
        self.first_line.setFrameShadow(QFrame.Plain)
        self.first_line.setStyleSheet(splitter_style)
        if self.text is not None:
            self.second_line = QFrame()
            self.second_line.setFrameStyle(QFrame.HLine)
            self.second_line.setFrameShadow(QFrame.Plain)
            self.second_line.setStyleSheet(splitter_style)

    def _createLayouts(self):
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignVCenter)

        self.main_layout.addWidget(self.first_line)
        if self.text is not None:
            self.main_layout.addWidget(self.text_label)
            self.main_layout.addWidget(self.second_line)


class LineEditPBtn(QWidget):
    """
    文字 文本框 按钮
    点击按钮将所选物体的名字加载到文本框
    """

    def __init__(self, label, width = 60):
        """

        :param label: 前面显示的文字
        :param width: 前缀与按钮宽度，默认60
        """
        super(LineEditPBtn, self).__init__()
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        buttonQss = """QPushButton {
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
        line_style_sheet = """QLineEdit {
                              font: bold 8pt Microsoft YaHei;
                              color: rgb(248, 244, 237);
                              }
                            """
        self.prefix = QLabel(label)
        self.line = QLineEdit()
        self.button = QPushButton(u"添加")

        self.button.setStyleSheet(buttonQss)
        self.prefix.setStyleSheet("color: rgb(248, 244, 237); font: bold 10pt Microsoft YaHei;")
        self.line.setStyleSheet(line_style_sheet)

        self.main_layout.addWidget(self.prefix)
        self.main_layout.addWidget(self.line)
        self.main_layout.addWidget(self.button)

        self.prefix.setFixedWidth(width)
        self.button.setFixedWidth(width)

    def getText(self):
        """
        获取名称
        """
        return self.line.text()


if __name__ == "__main__":
    pass
