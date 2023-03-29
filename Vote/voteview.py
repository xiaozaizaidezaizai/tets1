# python
# -*- coding: UTF-8 -*-
'''
@Project ：tets1 
@File    ：voteview.py
@IDE     ：PyCharm 
@Author  ：jinwenbo
@Date    ：2023/3/4 15:10 
'''

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QVBoxLayout, QHBoxLayout,
                             QFrame, QMessageBox, QPushButton,
                             QCheckBox,
                             QApplication)
from PyQt5.QtGui import QFont, QIcon

import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from App.util import center
from KeyGen.keyGen import openKey
from Database.vote import getVotenum, getVoteData, updataUsrRecord
from Database.launch import updateTotal


class Voteview(QWidget):
    '''
    usr: 当前用户
    title（str): 活动标题
    data(choice(str), tag(int)): 投票活动数据
    votelimt(int): 一个人最多可以投多少票
    '''
    '''                  用户  标题  数据[选项+素数] 票数  邀请码'''
    def __init__(self, usr, title, data, votelimit=1, captcha=None):
        super().__init__()
        self.usr = usr
        self.votelimit = votelimit
        self.captcha = captcha
        self.initUI(title, data)

    '''布局'''
    def initUI(self, title, data):

        title = QLabel(title)
        title.setFont(QFont('楷体', 20))

        tophbox = QHBoxLayout()
        tophbox.addStretch(1)
        tophbox.addWidget(title)
        tophbox.addStretch(1)

        self.checkBox = []#选项
        self.num = len(data)#选项的数量
        self.createCheckBox(data)#选项和选项框绑定

        midvbox = QVBoxLayout()
        for x in self.checkBox:#将选项依次的加到垂直盒中
            midvbox.addWidget(x)

        midhbox = QHBoxLayout()
        midhbox.addStretch(1)
        midhbox.addLayout(midvbox)#选项加多时伸高
        midhbox.addStretch(1)
        midhbox.setStretchFactor(midhbox, 2)#分裂布局部件可伸缩setStretchFactor

        midFrame = QFrame()#黑色边框
        midFrame.setFrameShape(QFrame.WinPanel)
        midFrame.setLayout(midhbox)

        voteuse = QLabel('当前可投票数: ')
        voteuse.setFont(QFont('楷体', 10))
        self.voteuseLine = QLineEdit()
        self.voteuseLine.setReadOnly(True)#只读限制
        self.getVotenum()#自身类的方法

        downhbox = QHBoxLayout()
        downhbox.addStretch(1)
        downhbox.addWidget(voteuse)
        downhbox.addWidget(self.voteuseLine)
        downhbox.addStretch(1)

        self.confirmButton = QPushButton('投票')
        self.confirmButton.setFont(QFont('黑体', 12))
        self.confirmButton.setIcon(QIcon('../image/ok.png'))
        self.confirmButton.clicked.connect(self.onConfirm)

        bottomhbox = QHBoxLayout()
        bottomhbox.addStretch(1)
        bottomhbox.addWidget(self.confirmButton)
        bottomhbox.addStretch(1)

        totalLayout = QVBoxLayout()
        totalLayout.addLayout(tophbox)
        totalLayout.addWidget(midFrame)
        totalLayout.addLayout(downhbox)
        totalLayout.addLayout(bottomhbox)

        self.setLayout(totalLayout)

        center(self)
        self.resize(450, 300)
        self.setWindowTitle('投票')
        self.setWindowIcon(QIcon('../image/voteview.png'))

    '''将选项和选项框绑定'''
    def createCheckBox(self, data):
        for x in data:
            text = x[0] + '-' + str(x[1])#【选项 + 素数】
            checkBox = QCheckBox(text)#依次将选项加到选项框中
            checkBox.setFont(QFont('宋体', 16))#PyQt5.QtWidgets.QCheckBox
            self.checkBox.append(checkBox)

    '''获取还剩投票的数量'''
    def getVotenum(self):
        if self.captcha is None:
            self.voteuseLine.setText(str(self.votelimit))
        else:
            votenum = getVotenum(self.captcha, self.usr, self.votelimit)#
            self.voteuseLine.setText(str(votenum))
         #   self.voteuseLine.setText(str('3'))

    def onConfirm(self):
        if self.captcha is None:
            QMessageBox.warning(self, 'warning', '这只是一个预览效果', QMessageBox.Yes)
            return
        if int(self.voteuseLine.text()) == 0:
            QMessageBox.information(self, 'soryy', '您的投票次数已经用光', QMessageBox.Yes)
            return None
        cnt = 0#勾选的数量
        m = 1
        for x in self.checkBox:#self.checkBox是元组但里面的值是单个列表框
            if x.isChecked() == True:#判断是否被选中
                cnt = cnt + 1
                if cnt > int(self.voteuseLine.text()):#勾选和剩余投票数比对
                    QMessageBox.warning(self, 'warning', '您的票数不足够, 请重新勾选', QMessageBox.Yes)
                    return None
                text = x.text()#单个选项的文本
                data = text.split('-')#拆分字符串
                m = m * int(data[1])#应该是判断选项的 【 将素数乘 m 】
                print('m=','')
                print(m)
        if cnt == 0:
            QMessageBox.warning(self, 'warning', '您未选择任何选项进行投票', QMessageBox.Yes)
            return None
        QMessageBox.information(self, '提示', '请准备好加载加密公钥', QMessageBox.Yes)
        pubkey = openKey(self, 0)#投票结果公钥加密  ElGamalPublicKey(q, g, h) 【返回一个对象】
        if pubkey == False:
            QMessageBox.information(self, '提示', '您已取消本次加密', QMessageBox.Yes)
            return None
        C = pubkey.encrypt_int(m)#m加密明文 将选取的结果加密
        updateTotal(self.captcha, pubkey, C)#更新记录captcha对应的投票总数
        votenum = int(self.voteuseLine.text()) - cnt
        updataUsrRecord(self.captcha, self.usr, votenum)#更新voterecords表中的某活动用户投票数量
        self.getVotenum()
        QMessageBox.information(self, '提示', '投票成功', QMessageBox.Yes)


if __name__ == "__main__":
    usr = '1'
    title = '学生选举'
    data = [['ss', 2], ['ff', 3], ['zz', 5], ['yy', '7']]
    votelimit = 3
    captcha = '5b12ec5b340cb1220525b96e07183987'
    data = getVoteData(captcha)

    app = QApplication(sys.argv)
    voteview = Voteview(usr=usr, title=title, data=data, votelimit=votelimit, captcha=captcha)
    voteview.show()
    sys.exit(app.exec_())