# python
# -*- coding: UTF-8 -*-
'''
@Project ：tets1 
@File    ：launch.py
@IDE     ：PyCharm 
@Author  ：jinwenbo
@Date    ：2023/3/4 15:03 
'''

import sys
from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5 import sip
import os#Python解释器易于扩展，可以使用C语言或C++

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from App.util import center
from HE.util import create_primes
#from Vote.voteview import Voteview
from KeyGen.keyGen import openKey
from Database.util import md5
from Database.launch import insert_launch, del_launch, insert_votedata


class LaunchWindow(QWidget):

    def __init__(self, usr=None):
        super().__init__()
        self.usr = usr#将用户名传到投票页面
        self.initUI()

    def initUI(self):

        title = QLabel('活动标题:')
        title.setFont(QFont('楷体', 15))
        title.setAlignment(Qt.AlignHCenter)#居中
        self.titleInput = QLineEdit()#标题输入框

        tophbox = QHBoxLayout()#水平盒子
        tophbox.addStretch(1)
        tophbox.addWidget(title)#将标题加进去
        tophbox.addWidget(self.titleInput)
        tophbox.addStretch(1)

        choice = QLabel('选项: ')
        choice.setFont(QFont('宋体'))
        self.choiceInput = QLineEdit()

        lefthbox1 = QHBoxLayout()#水平盒子
        lefthbox1.addWidget(choice)
        lefthbox1.addWidget(self.choiceInput)

        self.appendButton = QPushButton('添加')#点击按钮
        self.appendButton.setFont(QFont('黑体'))
        self.appendButton.setIcon(QIcon('../image/vote.jpg'))
        self.appendButton.clicked.connect(self.onAppend)#添加按钮响应函数

        lefthbox2 = QHBoxLayout()#水平盒子将添加按钮此盒子
        lefthbox2.addStretch(1)
        lefthbox2.addWidget(self.appendButton)
        lefthbox2.addStretch(1)

        votelimit = QLabel('个人有效票数: ')
        self.votelimitInput = QLineEdit()
        self.votelimitInput.setPlaceholderText('输入个人票数')
        intValidator = QIntValidator()#设置范围
        intValidator.setRange(1, 2147483647)
        self.votelimitInput.setValidator(intValidator)

        lefthbox3 = QHBoxLayout()
        lefthbox3.addWidget(votelimit)
        lefthbox3.addWidget(self.votelimitInput)

        self.viewButton = QPushButton('预览')
        self.viewButton.setIcon(QIcon('../image/view.png'))
    #    self.viewButton.clicked.connect(self.onView)

        self.saveButton = QPushButton('保存')
        self.saveButton.setIcon(QIcon('../image/save.png'))
        self.saveButton.clicked.connect(self.onSave)

        lefthbox4 = QHBoxLayout()
        lefthbox4.addWidget(self.viewButton)
        lefthbox4.addWidget(self.saveButton)

        leftLayout = QVBoxLayout()#垂直盒子将上面四个都装进来
        leftLayout.addLayout(lefthbox1)
        leftLayout.addLayout(lefthbox2)
        leftLayout.addLayout(lefthbox3)
        leftLayout.addLayout(lefthbox4)

        leftFrame = QFrame()
        leftFrame.setFrameShape(QFrame.WinPanel)#黑色框架
        leftFrame.setLayout(leftLayout)

        self.righLayout = QVBoxLayout()

        self.tabledata = []#建一个列表【存放添加的选项】
        self.rownum = len(self.tabledata)#获取长度 【行数】
        self.showtable = None#类属性变量 【列表窗体】

        self.createTable(self.tabledata)#将列表传给方法createTable【右侧的选项列表】

        downhobx = QHBoxLayout()
        downhobx.addWidget(leftFrame)
        downhobx.addLayout(self.righLayout)
        downhobx.setStretchFactor(leftFrame, 1)#可以伸缩
        downhobx.setStretchFactor(self.righLayout, 1)

        self.captchalbl = QLineEdit()
        self.captchalbl.setText('活动邀请码: ')

        totalLayout = QVBoxLayout()#大盒子
        totalLayout.addLayout(tophbox)
        totalLayout.addLayout(downhobx)
        totalLayout.addWidget(self.captchalbl)

        self.setLayout(totalLayout)#整个投票页面

        center(self)#居中
        self.resize(600, 350)
        self.setWindowTitle('发起投票')
        self.setWindowIcon(QIcon('../image/launch.png'))

    '''获取列表中已有的数据'''
    def getTableData(self):
        data = []
        for i in range(self.rownum):
            tmp = []
            for j in range(self.colnum):
                tmp.append(self.showtable.item(i, 0).text())
            data.append(tmp)
        return data

    '''添加到列表中的事件响应方法'''
    def onAppend(self):
        choice = self.choiceInput.text()#获取选项的文本
        if choice == '':
            QMessageBox.warning(self, 'warning', '选项不能为空', QMessageBox.Yes)
        else:
            if self.rownum:#列表中不空
                self.tabledata = self.getTableData()#调用方法更新候选选的列表属性
            self.tabledata.append([choice])#存入一个列表类型
            self.createTable(self.tabledata)#重新调用创建列表的函数【刷新】
            QMessageBox.information(self, 'ok', '选项添加成功', QMessageBox.Yes)
            self.choiceInput.clear()#清空文本框

    #检查需要输入数据是否完整
    def Check(self):
        if self.rownum == 0:
            QMessageBox.warning(self, 'warning', '您还没有创建任何候选项', QMessageBox.Yes)
            return False
        if self.rownum < 2:
            QMessageBox.warning(self, 'warning', '投票至少需要两个选项', QMessageBox.Yes)
            return False
        title = self.titleInput.text()#获得标题
        if title == '':
            QMessageBox.warning(self, 'warning', '请输入活动标题', QMessageBox.Yes)
            return False
        votelimit = self.votelimitInput.text()
        if votelimit == '':
            QMessageBox.warning(self, 'warning', '有效票数不能为零', QMessageBox.Yes)
            return False
        return True

    '''保存【加密】'''
    def onSave(self):
        if self.Check() == True:
            title = self.titleInput.text()#标题
            votelimit = self.votelimitInput.text()#票数
            votelimit = int(votelimit)#转成整型
            primes = create_primes(self.rownum)#素数列表
            self.tabledata = self.getTableData()#获取列表中已有的数据
            data = []
            for i in range(self.rownum): # 将列表中的数据和素数按行加到data列表
                data.append([self.tabledata[i][0], primes[i]])
            reply = QMessageBox.question(self, '询问', '确认保存?',
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                s = self.usr + title + str(votelimit)
                ''' 用户名+标题+票数 '''
                print(s)
                for i in range(len(data)):
                    s = s + data[i][0] + '-' + str(data[i][1])
                    print('s:',end='')
                    print(s)
                captcha = md5(s)#s串hash处理
                print('邀请码:'+captcha)
                pubkey = openKey(self, 0)#返回密钥分公私
                if pubkey == False:
                    return

                C = pubkey.encrypt_int(1)# 发起投票的保存加密都是对数字1
                C = str(C[0]) + ',' + str(C[1])
                flag = insert_launch(self.usr, title, captcha, votelimit, C)#
                                    #'''  用户   标题，  邀请码       票数   密文  '''
                if flag == 0:
                    QMessageBox.information(self, 'sorry', '后台数据库出了点问题', QMessageBox.Yes)
                elif flag == -1:
                    QMessageBox.warning(self, 'warning', '您已经保存过该活动', QMessageBox.Yes)
                else:
                    for x in data:
                        flag = insert_votedata(captcha, x[0], x[1])
                        if flag == 0:
                            del_launch(captcha)
                            QMessageBox.information(self, 'sorry', '后台数据库出了点问题', QMessageBox.Yes)
                            return
                        elif flag == -1:
                            QMessageBox.warning(self, 'warning', '生成标记不是素数', QMessageBox.Yes)
                    self.captchalbl.setText('投票邀请码: ' + captcha)
                    QMessageBox.information(self, '恭喜', '保存成功', QMessageBox.Yes)

    '''删除列表'''
    def delTable(self):
        if self.showtable is not None:#类属性不为空
            self.righLayout.removeWidget(self.showtable)
            sip.delete(self.showtable)
            self.rownum = 0

    '''创建右侧候选列表'''
    def createTable(self, data):#data类型是两列表
        self.delTable()#先清空列表再进行加载
        self.rownum = len(data)#行属性
        collists = ['候选']
        self.colnum = len(collists)#列属性
        self.showtable = QTableWidget(self.rownum, self.colnum)#列表窗体 几行几列
        self.showtable.setHorizontalHeaderLabels(collists)#水平表头
        for i in range(self.rownum):
            for j in range(self.colnum):
                self.showtable.setItem(i, j, QtWidgets.QTableWidgetItem(str(data[i][j])))
        self.showtable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)#使列表自适应宽度
        self.righLayout.addWidget(self.showtable)#加到布局中

'''
        def onView(self):
        if self.Check() == True:
            title = self.titleInput.text()
            votelimit = self.votelimitInput.text()
            votelimit = int(votelimit)
            primes = create_primes(self.rownum)
            self.tabledata = self.getTableData()
            data = []
            for i in range(self.rownum):
                data.append([self.tabledata[i][0], primes[i]])
            self.voteview = Voteview(self.usr, title, data, votelimit)
            self.voteview.show()
            self.showMinimized()

'''






if __name__ == "__main__":
    usr = '名'

    app = QApplication(sys.argv)
    launchWindow = LaunchWindow(usr)
    launchWindow.show()
    sys.exit(app.exec_())