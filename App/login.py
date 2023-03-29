#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：tets1
@File    ：register.py
@IDE     ：PyCharm
@Author  ：jinwenbo
@Date    ：2023/3/2
'''
import sys
from PyQt5.Qt import *
import util
import main
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..')) #当前python程序所在目录的父目录的绝对路径加入到环境变量PYTHON_PATH中
from Database.util import Data_Login  #PYTHON_PATH是python的搜索路径，再引入模块时就可以从父目录中搜索得到了

class LoginWindow(QWidget):#继承Qwidget类【所有控件类的父类】

    def __init__(self):#方法的初始化
        super().__init__()#调用父类的构造函数
        self.mainWindow = None#主页面对象属性
        self.registerWindow = None#属性
        self.initUI()#调用自身方法

    def initUI(self):#初始化面板


        logomap = QPixmap('../image/signin.png')#加载图片
        logolbl = QLabel(self)#创建标签
        logolbl.setPixmap(logomap)#将图片加到标签的位置
        logolbl.setScaledContents(True)  # 图片自适应标签大小

        title = QLabel('电子投票系统',self)#标题
        title.setAlignment(Qt.AlignCenter)#水平居中
        title.setFont(QFont("楷体", 20))#字体设置


        user = QLabel('账号: ')#只有在本方法中能用此变量
        pwd = QLabel('密码: ')

        self.userInput = QLineEdit()#对象 QLineEdit是一个单行文本输入框。
        self.userInput.setPlaceholderText('请输入用户名')

        self.pwdInput = QLineEdit()
        self.pwdInput.setPlaceholderText('请输入密码')
        self.pwdInput.setEchoMode(QLineEdit.Password)  # 密码不以明文显示

        self.loginButton = QPushButton('登录', self)
        self.loginButton.setIcon(QIcon('../image/start.png'))
        self.loginButton.setFont(QFont('楷体'))
        self.loginButton.clicked.connect(self.onLogin)#点击事件被onLogin方法处理

        self.registerButton = QPushButton('注册', self)
        self.registerButton.setFont(QFont('楷体'))
        self.registerButton.setIcon(QIcon('../image/register.png'))#在按钮中嵌入图片
        self.registerButton.clicked.connect(self.onRegister)#点击事件被onRegister方法处理

        rightcenterLayout = QGridLayout()#网格布局
        rightcenterLayout.addWidget(user, 0, 0, 1, 1)#用户名输入框 第0行，第0列开始，占1行1列
        rightcenterLayout.addWidget(pwd, 1, 0, 1, 1)
        rightcenterLayout.addWidget(self.userInput, 0, 1, 1, 3)#文本输入框 第0行第1列开始，占1行3列
        rightcenterLayout.addWidget(self.pwdInput, 1, 1, 1, 3)

        rightcenterFrame = QFrame()#是一个基类。可以选择使用，主要是用来控制边框样式。
        rightcenterFrame.setFrameShape(QFrame.WinPanel)#创建一个黑色边框
        rightcenterFrame.setLayout(rightcenterLayout)#将网格布局对象变量加入到里面

        rightdownLayout = QHBoxLayout()#采用QHBoxLayout盒子类，按照从左到右的顺序来添加控件
        rightdownLayout.addWidget(self.loginButton)#将按钮添加到此组件中
        rightdownLayout.addWidget(self.registerButton)#两按钮水平放置

        rightLayout = QVBoxLayout()#垂直装盒子
        rightLayout.addWidget(title)#标题
        rightLayout.addWidget(rightcenterFrame)#边框
        rightLayout.addLayout(rightdownLayout)#两按钮

        totalLayut = QHBoxLayout()
        totalLayut.addWidget(logolbl)#各个标签和窗体的排布
        totalLayut.addLayout(rightLayout)#将图片标签和垂直装的盒子并列

        self.setLayout(totalLayut)#将大盒子装到窗体中
        self.resize(600, 240)#窗体大小
        util.center(self)#util就是为了实现窗体居中
        self.setFont(QFont('楷体', 15))
        self.setWindowTitle('登录')
        self.setWindowIcon(QIcon('../image/car.png'))

    def onLogin(self):#登录

        usr = self.userInput.text()#获取文本框中的信息
        pwd = self.pwdInput.text()


        if usr == '':
            QMessageBox.warning(self, 'warning', '用户名不能为空', QMessageBox.Yes)#弹窗提示 QMessageBox.Yes按其退出
        elif pwd == '':
            QMessageBox.warning(self, 'warning', '请输入密码', QMessageBox.Yes)
        else:
            flag = Data_Login(usr, pwd)#这个login是Database包中util中的方法，就是在查找数据库
            if flag == 1:
                if self.mainWindow is not None:
                    self.close()#登录页面关闭
                    self.mainWindow.usr = usr#用户名传过去
                    self.mainWindow.showbottom()#在主页面底部显示用户名
                    self.mainWindow.show()
            elif flag == 0:
                QMessageBox.information(self, 'sorry', '数据库程序出了点bug', QMessageBox.Yes)#弹窗提示
            elif flag == -1:
                QMessageBox.warning(self, 'warning', '用户不存在, 请先注册', QMessageBox.Yes)
            else:
                QMessageBox.warning(self, 'warning', '密码错误', QMessageBox.Yes)

        self.userInput.clear()
        self.pwdInput.clear()

    def onRegister(self):
        if self.registerWindow is not None:
            self.userInput.clear()
            self.pwdInput.clear()
            self.close()
            self.registerWindow.show()


if __name__ == "__main__":#测试对本页面
    app = QApplication(sys.argv)
    LoginWindow = LoginWindow()
    '''
    mainWindow = main.MainWindow()
    mainWindow.loginWindow = LoginWindow
    LoginWindow.mainWindow = mainWindow
    '''
    LoginWindow.show()
    sys.exit(app.exec_())
