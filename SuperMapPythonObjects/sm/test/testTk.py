#coding: gb2312

import os
import sm.tk.filetk as tk
import wx


app = wx.App(False)

"""
fld = tk.Folder(os.getcwd())

path = fld.Choose()
print path
print fld.path
"""

f = tk.File()
path = f.Choose()
print path
print f.fileName
