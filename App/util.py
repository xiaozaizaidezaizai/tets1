# python
# -*- coding: UTF-8 -*-
'''
@Project ：tets1 
@File    ：util.py
@IDE     ：PyCharm 
@Author  ：jinwenbo
@Date    ：2023/3/2 16:51 
'''
from PyQt5.QtWidgets import QDesktopWidget


def center(model):
    '''
    实现窗口居中
    '''
    qr = model.frameGeometry()  # 获得主窗口所在的框架。
    cp = QDesktopWidget().availableGeometry().center()  # 获取显示器的分辨率，然后得到屏幕中间点的位置。
    qr.moveCenter(cp)  # 然后把主窗口框架的中心点放置到屏幕的中心位置。
    model.move(qr.topLeft())  # 然后通过move函数把主窗口的左上角移动到其框架的左上角，这样就把窗口居中了

