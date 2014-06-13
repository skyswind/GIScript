#coding: gb2312

import os
import wx
import tk.filetk as tk

app = wx.App(False)

folder = tk.ChooseSaveFile('保存文件')

print folder


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