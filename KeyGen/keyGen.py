# python
# -*- coding: UTF-8 -*-
'''
@Project ：tets1 
@File    ：keyGen.py
@IDE     ：PyCharm 
@Author  ：jinwenbo
@Date    ：2023/3/4 15:02 
'''

import sys #sys模块包含了与Python解释器和它的环境有关的函数
from PyQt5.Qt import *
import os #ython解释器易于扩展，可以使用C语言或C++

#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
#from HE.MHE import keyGen, save_key, load_key
from App.util import center
from HE.ElGamal import keyGen, save_key, load_key
from SM2.sm2 import SM2_Key

#这是生成密钥的窗体的类
class KeyGenWindow(QWidget):#继承

    def __init__(self):
        super().__init__()
        self.initUI()

    #生成密钥的窗体
    def initUI(self):

        keysize = QLabel('密钥长度: ')
        self.keysizeInput = QLineEdit() #是一个单行文本输入框
        self.keysizeInput.setPlaceholderText('1024')#背景文字的实现）
   #     intValidator = QIntValidator()
   #     intValidator.setRange(512, 2147483647)
   #     self.keysizeInput.setValidator(intValidator)

        self.confirmButton = QPushButton('生成')
        self.confirmButton.setFont(QFont('黑体'))
        self.confirmButton.setIcon(QIcon('../image/confirm.png'))
        self.confirmButton.clicked.connect(self.onConfirm)

        tophox = QHBoxLayout()
        tophox.addWidget(keysize)
        tophox.addWidget(self.keysizeInput)

        downhox = QHBoxLayout()
        downhox.addStretch(1)
        downhox.addWidget(self.confirmButton)
        downhox.addStretch(1)

        totalLayout = QVBoxLayout()
        totalLayout.addLayout(tophox)
        totalLayout.addLayout(downhox)

        self.setLayout(totalLayout)

        center(self)
        self.resize(325, 150)
        self.setWindowTitle('密钥生成')
        self.setWindowIcon(QIcon('../image/keyGen.png'))

    # 保存公私钥的方法
    def savekey(self, key, filename='', mode=0):
        '''
        mode 0 公钥 / 1 私钥
        '''
        filename = QFileDialog.getSaveFileName(self, '选择保存路径','../key/'+filename, "Text Files(*.txt)")
        '''打开文件资源管理器，获得你需要保存的文件名。（注意：它不会帮你创建文件，只返回一个元组）
        元组第一项为你的文件路径（包括你给的文件名），第二项为该文件的类型。'''
        print(filename)
        if len(filename[0]):#路径名
         #   ok = save_key(key, filename[0])
            try:
                with open(filename[0], 'w') as f:  # wb以二进制写模式打开 (参见 w )
                    f.write(key)#写入文件
            except Exception as e:
                raise ValueError(str(e))
            return True
        return False

    #在密钥的窗体内点击按钮事件回应
    def onConfirm(self):
        keysize = self.keysizeInput.displayText()
        print('值：'+keysize)
        if keysize =='':
            QMessageBox.warning(self, 'warning', '密钥长度不能为零', QMessageBox.Yes|QMessageBox.No)
            return
        keysize = int(keysize)
        if keysize == 0:
            QMessageBox.warning(self, 'warning', '密钥长度不能为零', QMessageBox.Yes)
        else:
            if keysize < 128:
                print('长度：',end='')
                print(keysize)
                r=QMessageBox.warning(self, '提醒', '密钥长度低于128不太适合安全加密', QMessageBox.Yes|QMessageBox.No)
                if r != QMessageBox.Yes:
                    return
            (pubkey, privkey)=SM2_Key() #生成的公私钥
            print(pubkey, privkey)
            QMessageBox.information(self, '保存', '准备开始保存公钥', QMessageBox.Yes)
            filename = 'public_key.txt'
            if self.savekey(pubkey, filename, 0) == True:
                rPu=QMessageBox.information(self, 'congratulation', '公钥保存成功', QMessageBox.Yes|QMessageBox.No)
                if rPu != QMessageBox.Yes:
                    return
                QMessageBox.information(self, 'save', '准备开始保存私钥', QMessageBox.Yes)
                filename = 'private_key.txt'
                if self.savekey(privkey, filename, 1) == True:
                    QMessageBox.information(self, 'congratulation', '私钥保存成功', QMessageBox.Yes)
            '''
            (pubkey, privkey) = keyGen(keysize)
            QMessageBox.information(self, 'save', '准备开始保存公钥', QMessageBox.Yes)
            filename = 'public_key.txt'
            if self.savekey(pubkey, filename, 0) == True:
                QMessageBox.information(self, 'congratulation', '公钥保存成功', QMessageBox.Yes)
                QMessageBox.information(self, 'save', '准备开始保存私钥', QMessageBox.Yes)
                filename = 'private_key.txt'
                if self.savekey(privkey, filename, 1) == True:
                    QMessageBox.information(self, 'congratulation', '私钥保存成功', QMessageBox.Yes)
            '''


#加载密钥路径
def openKey(widget, mode=0): #弹出窗口让用户选择文件的静态方法
    '''
    # 功能：打开密钥
    # 接受参数：
    widget: 可视化组件
    mode(0, 1): 0代表加载公钥, 1代表加载的是私钥
    # 返回参数：
    如果有选择文件返回对应的公钥类或者私钥类
    否则返回False
    '''
    '''filename是元组 绝对路径+选择的后缀名'''
    filename = QFileDialog.getOpenFileName(widget, 'Open Key File', '../key', '(*.txt)')
    if filename[0]:
        return load_key(filename[0], mode)
    return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    keyGenWindow = KeyGenWindow()
    keyGenWindow.show()
   # print(openKey(keyGenWindow))
    sys.exit(app.exec_())