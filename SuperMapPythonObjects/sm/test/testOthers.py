#coding: gb2312

import os
import wx
import sm.tk.filetk as tk

app = wx.App(False)

folder = tk.ChooseSaveFile('保存文件')

print folder