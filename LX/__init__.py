# python
# -*- coding: UTF-8 -*-
'''
@Project ：tets1
@File    ：__init__.py.py
@IDE     ：PyCharm
@Author  ：jinwenbo
@Date    ：2023/3/21 12:11
'''
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建菜单栏
        menubar = self.menuBar()
        # 创建“文件”菜单
        file_menu = menubar.addMenu('文件')
        # 创建“打开”菜单项
        open_file_action = QAction('打开', self)
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)
        # 创建“退出”菜单项
        exit_action = QAction('退出', self)
        exit_action.triggered.connect(self.exit)
        file_menu.addAction(exit_action)
        # 创建“帮助”菜单
        help_menu = menubar.addMenu('帮助')
        # 创建“关于”菜单项
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

    def open_file(self):
        print('打开文件')
    def exit(self):
        sys.exit()
    def about(self):
        print('关于')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
