# -*- coding: UTF-8 -*-

class Control(object):
    u"""
    :param kwargs: 修改控制器的参数
    :param kwargs: -t -transform string/Control 控制器
    :param kwargs: -n -name string 名字
    :param kwargs: -p -parent string/node 父对象
    :param kwargs: -s -shape data/name 形态
    :param kwargs: -c -color int 颜色
    :param kwargs: -r -radius float 半径
    :param kwargs: -ro -rotate [float, float,float] 旋转
    :param kwargs: -o -offset [float, float,float] 偏移
    :param kwargs: -l -locked [str, ...] 锁定属性
    :param kwargs: -ou -outputs [str, str] 输出属性
    """

    def __init__(self, *args, **kwargs):
        self.uuid = None
        keys = [("t", "transform"), ("n", "name"), ("p", "parent"), ("s", "shape"), ("c", "color"), ("r", "radius"),
                ("ro", "rotate"), ("o", "offset"), ("l", "locked"), ("ou", "outputs")]
        for index, (short, long) in enumerate(keys):
            # 依次获取长参，短参, 索引参
            arg = kwargs.get(long, kwargs.get(short, args[index] if index < len(args) else None))
            if arg is not None:
                # 若获取参数不为None, 则获取通过长参名称获取函数，并传入arg运行
                # getattr(self, "set_"+long)(arg)
                print(arg)


ctrl1 = Control("nurbsCircle1")

