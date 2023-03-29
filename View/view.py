# python
# -*- coding: UTF-8 -*-
'''
@Project ：tets1 
@File    ：view.py
@IDE     ：PyCharm 
@Author  ：jinwenbo
@Date    ：2023/3/4 15:12 
'''
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                        QGridLayout, QVBoxLayout, QHBoxLayout,
                        QFrame, QMessageBox, QPushButton,
                        QTextEdit,
                        QTableWidget,
                        QRadioButton,
                        QApplication)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtGui import QIntValidator
from PyQt5 import sip

import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from App.util import center
from KeyGen.keyGen import openKey
from Database.view import getVoteActivities, delVoteActivity, showVoteResult, drawResult
from Database.launch import getTotal


class ViewWindow(QWidget):

    def __init__(self, usr):
        super().__init__()
        self.usr = usr
        self.initUI()

    def initUI(self):#初始化

        self.showtable = None #展示列表
        self.radioButtons = []  #表中竖方向的按钮
        self.rownum = 0   #行数
        self.colnum = 2   #列数

        self.cenerLayout = QVBoxLayout()
        self.createTable(getVoteActivities(self.usr)) #功能：从launch表中返回usr的 标题和邀请码 【元组里面是二元组类型】

        self.showButton = QPushButton('查看结果')
        self.showButton.setFont(QFont('微软雅黑'))
        self.showButton.setIcon(QIcon('../image/search.png'))
        self.showButton.clicked.connect(self.onShow)

        self.delButton = QPushButton('删除活动')
        self.delButton.setFont(QFont('微软雅黑'))
        self.delButton.setIcon(QIcon('../image/delete.jpg'))
        self.delButton.clicked.connect(self.onDel)

        downhbox = QHBoxLayout()
        downhbox.addStretch(1)
        downhbox.addWidget(self.showButton)
        downhbox.addWidget(self.delButton)
        downhbox.addStretch(1)

        totalLayout = QVBoxLayout()
        totalLayout.addLayout(self.cenerLayout)#横表头
        totalLayout.addLayout(downhbox)#两按钮
        totalLayout.setStretchFactor(self.cenerLayout, 3)#可伸缩
        totalLayout.setStretchFactor(downhbox, 1)

        self.setLayout(totalLayout)

        center(self)
        self.resize(600, 270)
        self.setWindowTitle('投票查看')
        self.setWindowIcon(QIcon('../image/view.png'))

    '''重新加载时 将数据清空后 重新从数据库加载数据'''
    def delTable(self):
        if self.rownum:
            self.cenerLayout.removeWidget(self.showtable)
            sip.delete(self.showtable)
            self.rownum = 0

    '''处理【 标题和邀请码 】  重新从数据库加载数据'''
    def createTable(self, data):
        self.delTable()
        self.rownum = len(data)#计算行数
        collists = ['', '活动名称', '邀请码']#列名
        self.colnum = len(collists)#三列
        self.showtable = QTableWidget(self.rownum, self.colnum) #表格控件 确定几行几列
        self.showtable.setHorizontalHeaderLabels(collists) #设置 横表头
        self.radioButtons = [] #竖向表头
        for i in range(self.rownum):
            self.radioButtons.append(QRadioButton())#增加按钮
            self.showtable.setCellWidget(i, 0, self.radioButtons[i])#放在第几行第几列 放什么
            for j in range(1, self.colnum):
                self.showtable.setItem(i, j, QtWidgets.QTableWidgetItem(data[i][j - 1]))
        self.showtable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)#表示均匀拉直表头
        self.showtable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)#表格不可编辑
        self.cenerLayout.addWidget(self.showtable)#将表格加入到布局中

    def onShow(self):
        for i in range(self.rownum): #循环检查
            if self.radioButtons[i].isChecked() == True: #响应被点击的竖向按钮
                QMessageBox.information(self, '提示', '请准备加载解密的私钥', QMessageBox.Yes)
                prikey = openKey(self, 1)#加载私钥
                if prikey == False:
                    print("错误的密钥")
                    return
                captcha = self.showtable.item(i, 2).text()#获取选中的第二列数据邀请码
                total = getTotal(captcha)
                res = showVoteResult(captcha, total, prikey)#邀请码 total 私钥
                drawResult(res)

    def onDel(self):
        for i in range(self.rownum):
            if self.radioButtons[i].isChecked() == True:
                reply = QMessageBox.question(self, '警告', '您确认删除该活动?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    captcha = self.showtable.item(i, 2).text() #获取文本中的邀请码
                    delVoteActivity(captcha) #从三个表中都删除此数据
                    self.createTable(getVoteActivities(self.usr))
                return


if __name__ == "__main__":
    usr = '1'

    app = QApplication(sys.argv)
    viewWindow = ViewWindow(usr)
    viewWindow.show()
    sys.exit(app.exec_())
