# python
# -*- coding: UTF-8 -*-
'''
@Project ：tets1 
@File    ：mian.py
@IDE     ：PyCharm 
@Author  ：jinwenbo
@Date    ：2023/3/2 17:00 
'''
from PyQt5.QtWidgets import QApplication
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
from PyQt5.Qt import *
if __name__ == "__main__":

    app = QApplication(sys.argv)#创建一个程序
    print(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
    window = QWidget()#用户界面的原子
    window.resize(500,500)
    window.show()
    sys.exit(app.exec_())#开始执行程序，并进入消息循环，整个程序不退出