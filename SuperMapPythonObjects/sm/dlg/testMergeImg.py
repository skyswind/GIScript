#coding: utf-8

import mergeImgs as frm
import wx
app = wx.App(False)

win = frm.mergeImgs(None, -1, u"拼接影像文件", size=(600, 400),
                  style = wx.DEFAULT_FRAME_STYLE)
win.Show(True)
app.MainLoop()

