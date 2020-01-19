#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 16:35:38 2020

@author: jackson
"""
#import numpy as np
#array = np.genfromtxt("/home/jackson/Desktop/test_2.xlsx")
'''
import pandas as pd
a = pd.read_excel("/home/jackson/Desktop/test_2.xlsx")
print(type(a))
print(a)
'''
import numpy as np
print(np.genfromtxt('/home/jackson/Desktop/Crow/Sample_Input_Data.csv', dtype=float, delimiter=',', names=True))
