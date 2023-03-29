# -*- coding: utf-8 -*-
'''
# Created on Feb-20-20 15:05
# main.py
# @author: ss
'''

'''
应用窗口主程序
'''
import sys #sys为python的内置模块,提供了很多函数和变量来处理Python运行时环境的不同部分
from PyQt5.Qt import *
import login
import util
from KeyGen.keyGen import KeyGenWindow#将生成密钥类导进
from Launch.launch import LaunchWindow#将发起投票的类导进
from Vote.vote import VoteWindow
from View.view import ViewWindow

#更改的页面没有加这部分
class CenterWidget(QWidget):#传入主程序窗口对象parent进行调用 【自己写的中间模块】

    def __init__(self, parent=None, flags=Qt.WindowFlags()):#Qt.WindowFlags()此枚举类型用于为窗口小部件指定各种窗口系统属性
        '''
        parent为父控件，如果没有，可不指定或设为None。
        flags设置窗口的属性。
        窗口创建后，还可通过setParent()函数来指定父窗口。
        '''
        super().__init__(parent=parent, flags=flags)
        self.initUI(parent)
        self.keyGenWindows = []#密钥列表
        self.launchWindows = []#投票列表
        self.voteWindows = []
        self.viewWindows = []

    def initUI(self, parent):

        keyGenButton = QPushButton('密钥生成', self)#QPushButton用来创建可按压的按钮
        keyGenButton.setIcon(QIcon('../image/keyGen.png'))
        keyGenButton.setStyleSheet("QPushButton{color:black}"
                                   "QPushButton:hover{color:red}")
        keyGenButton.clicked.connect(lambda: self.onkeyGen(parent))

        launchButton = QPushButton('发起投票', self)
        launchButton.setIcon(QIcon('../image/launch.png'))
        launchButton.setStyleSheet("QPushButton{color:black}"
                                   "QPushButton:hover{color:red}")
        launchButton.clicked.connect(lambda: self.onLaunch(parent))

        voteButton = QPushButton('进行投票', self)
        voteButton.setIcon(QIcon('../image/vote.jpg'))
        voteButton.setStyleSheet("QPushButton{color:black}"
                                 "QPushButton:hover{color:red}")
        voteButton.clicked.connect(lambda: self.onVote(parent))

        viewButton = QPushButton('查看投票', self)
        viewButton.setIcon(QIcon('../image/view.png'))
        viewButton.setStyleSheet("QPushButton{color:black}"
                                 "QPushButton:hover{color:red}")
        viewButton.clicked.connect(lambda: self.onView(parent))

        vbox = QVBoxLayout()#垂直盒子
        vbox.addWidget(keyGenButton)#加到盒子里
        vbox.addWidget(launchButton)#将发起加入到布局中
        vbox.addWidget(voteButton)#将进行投票加入到布局中
        vbox.addWidget(viewButton)

        midhobx = QHBoxLayout()#水平盒子
        midhobx.addStretch(1)#占左边位置
        midhobx.addLayout(vbox)#将水平盒子加到垂直盒子中
        midhobx.addStretch(1)

        centerFrame = QFrame(self)#矩形框架对象
        centerFrame.setFrameShape(QFrame.WinPanel)
        centerFrame.setLayout(midhobx)#将垂直盒子加到框架里

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(centerFrame)
        hbox.addStretch(1)
        hbox.setStretchFactor(centerFrame, 30)
        self.setLayout(hbox)#将其加到主页面的布局中

    #生成密钥的方法
    def onkeyGen(self, parent):
        if parent is not None:#父控件不为空
            self.keyGenWindows.append(KeyGenWindow())#每次点击都会产生一个窗体对象  自己创建类的对象 此类继承了大窗体
            print(type(self.keyGenWindows[-1]))#可以生成多个密钥窗体类
            self.keyGenWindows[-1].show()#每次取最后一个窗体对象展示
            parent.showMinimized()#父窗口最小化

     #处理发起投票的方法
    def onLaunch(self, parent):
        if parent is not None:
            self.launchWindows.append(LaunchWindow(parent.usr))#将发起投票对象加入到投票列表中
            self.launchWindows[-1].show()#显示发起投票的页面 【Launch/launch.py】
            parent.showMinimized()

    #进行投票的方法
    def onVote(self, parent):
        if parent is not None:
            self.voteWindows.append(VoteWindow(parent.usr))
            self.voteWindows[-1].show()
            parent.showMinimized()

    #进行计票的方法
    def onView(self, parent):
        if parent is not None:
            self.viewWindows.append(ViewWindow(parent.usr))
            self.viewWindows[-1].show()
            parent.showMinimized()

class MainWindow(QMainWindow):#提供了一个主应用程序窗口，可以添加多个部件
    def __init__(self,usr=None):
        super().__init__()
        self.usr=usr#用户名
        self.loginWindow = None
        self.initUI()

    def initUI(self):
        # 中心布局
        zJ = CenterWidget(self)
      #  self.setCentralWidget(zJ)#创建对象 将自身作为参数传入
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        # 菜单栏设置
        menu = self.menuBar()
     #   menu1 = menu.addMenu('账号')
        zB =  menu.addMenu('准备')
        tP = menu.addMenu('投票')
        jP = menu.addMenu('计票')
        yP = menu.addMenu('验票')



        rG=zB.addMenu('注册')
        rG.addAction("选民")
        rG.addAction("候选人")
        zB.addAction('生成选票（密钥）')
        zB.addAction('投票主题')
        zB.triggered.connect(self.zhunBei)

   #     tp.addAction(actionSavePicture)
        tP.addAction('开始投票')
        tP.triggered.connect(self.touPiao)
     #   self.chaKan()

        jP.addAction('进行计票')
        jP.triggered.connect(self.jiPiao)

        yP.addAction('验票检查')
        yP.triggered.connect(self.yanPiao)

        signoutAct = QAction('注销', self)#QAction类提供了一个可以同时出现在菜单和工具条上的抽象用户界面操作
        signoutAct.triggered.connect(self.onSignout)
   #     menu1.addAction(signoutAct)#将其添加到菜单中

        exitAct = QAction('退出', self)
        exitAct.triggered.connect(self.onExit)
   #     menu1.addAction(exitAct)


        # 整体布局
        self.resize(700, 450)
        util.center(self)#居中
        self.setFont(QFont("楷体", 13))
        self.setWindowTitle('电子投票系统')
        self.setWindowIcon(QIcon('../image/user.png'))

        self.bottomlbl = QLabel()#标签 用户右下角显示
        self.bottomlbl.setFont(QFont("楷体"))
        self.statusBar().addPermanentWidget(self.bottomlbl)#将标签加入到底部状态栏
        self.showbottom()



    # 设置底部状态栏, 显示当前登录的用户
    def showbottom(self):
        if self.usr is not None:
            s = "欢迎你: " + self.usr
            self.bottomlbl.setText(s)

        # 注销重新登录
    def onSignout(self):#重新登录
        if self.loginWindow is not None:
            self.close()
            self.loginWindow.show()

    def onExit(self):#退出
        self.close()

    def zhunBei(self,q):#准备
        if q.text() == '注册':
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '后续实现')
            msg_box.exec_()
            print("后续实现")
        if q.text() == "投票主题":
            sub = LaunchWindow(self.usr)
            self.mdi.addSubWindow(sub)
            sub.show()
            self.mdi.tileSubWindows()
        if q.text() == "生成选票（密钥）":
            print('生成密钥')
            sub=KeyGenWindow()
            self.mdi.addSubWindow(sub)
            sub.show()
            self.mdi.tileSubWindows()

    def touPiao(self,q):
        if q.text() == "开始投票":
            v=VoteWindow(self.usr)
            self.mdi.addSubWindow(v)
            v.show()
            self.mdi.tileSubWindows()
    def jiPiao(self):
        v2=ViewWindow(self.usr)
        self.mdi.addSubWindow(v2)
        v2.show()
        self.mdi.tileSubWindows()
    def yanPiao(self):
        msg_box = QMessageBox(QMessageBox.Information, '提示', '验票后续实现')
        msg_box.exec_()
        print("验票后续实现")


if __name__ == "__main__":
    
    app = QApplication(sys.argv)#开启一个应用程序
    '''
    loginWindow = login.LoginWindow()#创建一个窗体
    mainWindow = MainWindow()  # 创建对象变量mianWindow
    mainWindow.loginWindow=loginWindow#将登录页面对象赋值给主页面变量
    loginWindow.mainWindow=mainWindow#将主页面对象赋值给登录对象变量
    loginWindow.show()
    '''
    loginWindow = login.LoginWindow()  #类 创建一个窗体
    mainWindow=MainWindow('1')
    mainWindow.loginWindow = loginWindow
    mainWindow.showbottom()  # 在主页面底部显示用户名
    mainWindow.show()

    sys.exit(app.exec_())#消息循环