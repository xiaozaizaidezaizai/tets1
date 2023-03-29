# python
# -*- coding: UTF-8 -*-
'''
@Project ：tets1 
@File    ：vote.py
@IDE     ：PyCharm 
@Author  ：jinwenbo
@Date    ：2023/3/4 15:09 
'''

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QVBoxLayout, QHBoxLayout,
                             QMessageBox, QPushButton,
                             QApplication)
from PyQt5.QtGui import QFont, QIcon

import os
from Database.launch import check_captcha, getVoteContent
from Database.vote import getVoteData

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from App.util import center
from Database.launch import check_captcha, getVoteContent
from Database.vote import getVoteData
from Vote.voteview import Voteview


class VoteWindow(QWidget):

    def __init__(self, usr):
        super().__init__()
        self.usr = usr
        self.voteview = None
        self.initUI()

    def initUI(self):

        captcha = QLabel('输入邀请码: ')
        self.captchaInput = QLineEdit()

        tophbox = QHBoxLayout()
        tophbox.addWidget(captcha)
        tophbox.addWidget(self.captchaInput)

        self.confirmButton = QPushButton('进入')
        self.confirmButton.setFont(QFont('黑体', 12))
        self.confirmButton.setIcon(QIcon('../image/enter.png'))
        self.confirmButton.clicked.connect(self.onConfirm)

        downhbox = QHBoxLayout()
        downhbox.addStretch(1)
        downhbox.addWidget(self.confirmButton)
        downhbox.addStretch(1)

        totalLayout = QVBoxLayout()
        totalLayout.addLayout(tophbox)
        totalLayout.addLayout(downhbox)

        self.setLayout(totalLayout)

        center(self)
        self.resize(400, 150)
        self.setWindowTitle('参与投票')
        self.setWindowIcon(QIcon('../image/vote.jpg'))

    def onConfirm(self):

        captcha = self.captchaInput.text()
        if captcha == '':
            QMessageBox.warning(self, 'warning', '请输入邀请码', QMessageBox.Yes)
        else:
            flag = check_captcha(captcha)#按邀请码在 launch 表中进行查询
            if flag == 0:
                QMessageBox.information(self, 'sorry', '后端数据库出了问题', QMessageBox.Yes)
            elif flag == 1:
                QMessageBox.information(self, 'sorry', '该活动不存在, 请确认验证码是否正确', QMessageBox.Yes)
            else:
                data = getVoteContent(captcha)#获取文本中的邀请码
                title, votelimit = data[0], data[1]
                data = getVoteData(captcha)#votedata表中返回captcha记录对应  【选项 + tag】
                '''                         用户    标题  数据[选项+素数] 票数  邀请码'''
                self.voteview = Voteview(self.usr, title, data, votelimit, captcha)#进行投票对象页面
                self.voteview.show()
                self.showMinimized()

            self.captchaInput.clear()


if __name__ == "__main__":
    usr = 'ss'

    app = QApplication(sys.argv)
    voteWindow = VoteWindow(usr)
    voteWindow.show()
    sys.exit(app.exec_())