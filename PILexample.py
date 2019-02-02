# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 21:41:30 2019

@author: Administrator
"""

from PIL import Image
import numpy as np
a=np.asarray(Image.open('D:/pytest/a.jpeg').convert('L')).astype('float')
depth=10.
grad=np.gradient(a)               #取图像灰度的梯度值
grad_x,grad_y=grad                #取横纵图像梯度值
grad_x=grad_x*depth/100.
grad_y=grad_y*depth/100.
A=np.sqrt(grad_x**2+grad_y**2+1.)
uni_x=grad_x/A
uni_y=grad_y/A
uni_z=1./A
vec_el=np.pi/2.2                   #光源的俯视角度转化为弧度值
vec_az=np.pi/4.                    #光源的方位角度转化为弧度值
dx=np.cos(vec_el)*np.cos(vec_az)   #光源对x轴的影响
dy=np.cos(vec_el)*np.sin(vec_az)
dz=np.sin(vec_el)
b=255*(dx*uni_x+dy*uni_y+dz*uni_z) #光源归一化
b=b.clip(0,255)
im=Image.fromarray(b.astype('uint8'))    #图像重构
im.save('D:/pytest/aHD.jpg')