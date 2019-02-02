# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 21:41:30 2019

@author: Administrator
"""

from PIL import Image
import numpy as np
im=np.array(Image.open("D:/pytest/a.jpeg").convert('L'))

b=255*(im/255)**2
newim=Image.fromarray(b.astype('uint8'))
newim.save("D:/pytest/a4.jpg")