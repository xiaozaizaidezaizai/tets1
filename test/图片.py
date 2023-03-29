# python
# -*- coding: UTF-8 -*-
'''
@Project ：tets1 
@File    ：图片.py
@IDE     ：PyCharm 
@Author  ：jinwenbo
@Date    ：2023/3/2 21:30 
'''
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import numpy as np
import os
import sys
#sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
lena = mpimg.imread('') # 读取和代码处于同一目录下的 lena.png
# 此时 lena 就已经是一个 np.array 了，可以对它进行任意处理
lena.shape #(512, 512, 3)

plt.imshow(lena) # 显示图片

plt.show()