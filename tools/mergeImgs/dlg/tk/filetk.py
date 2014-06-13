#coding: utf-8
import os
from os.path import walk, join, normpath
from os import getcwd
import string
import re
import time

import wx

#经常要用到的文件夹中文件查找及遍历功能放到这里
#注意：这里用的是正则表达式的通配符，不是Windows的通配符
#比如：要查找文件夹中（包括子目录中）所有的.tif文件，通配符是这样的：".*\.tif"
#匹配字符串结束加/Z，例如：r'.*\.tif/Z'
#这里不区分大小写，匹配代码里最后一个参数：re.I，若把这个参数去掉则区分大小写
class Folder:
    def __init__(self, path = u''):
        self.path = path
        self.reMatch = u''
        self.FileLists = []

    #visit是回调函数，不要直接调用
    def visit(self, arg, dirname, names):
        for file in names:
            files=normpath(join(dirname, file))
            if re.match(self.reMatch,file,re.I):
                self.FileLists.append(files)

    #根据通配符把文件夹中符合要求的文件都查找出来，填充到FileLists中
    def GetFileLists(self):
        self.FileLists = []
        os.path.walk(self.path, self.visit,0)

    #弹出文件夹选择框以选择文件夹
    #需要事先安装好wxPython
    #调用此函数之前需要声明wx.App对象，例如：app = wx.App(False)，只要有这一行，就可以调这个函数了
    def Choose(self):
        dialog = wx.DirDialog(None, u'选择文件夹',style = wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        dialog.SetPath(os.getcwd())

        if dialog.ShowModal() == wx.ID_OK:
            self.path = dialog.GetPath()
        
        dialog.Destroy()
        return self.path

class File:
    #mode共有五种类型
    #r = 只读打开
    #rb = 以二进制方式只读打开
    #w = 可写方式打开
    #wb = 以二进制可写方式打开
    #w+ = 以追加方式打开
    def __init__(self, fileName = u'', mode = 'r'):
        self.fileName = fileName
        self.mode = mode
        self.file = None
        self.bOpen = 0

    #析构函数
    def __del__(self):
        if self.bOpen:
            self.file.close()
            self.file = None
            self.bOpen = 0

    def Choose(self):
        dlg = wx.FileDialog(None, 
                            message=u"打开文件",
                            wildcard=u"PNG(*.png)|*.png" ,
                            style=wx.OPEN
                            )
        if dlg.ShowModal() == wx.ID_OK:
            self.fileName = dlg.GetPath()
            
        dlg.Destroy()
        return self.fileName



    #打开文件
    def Open(self):
         self.file = open(self.fileName, self.mode)
         self.bOpen = 1

    #读取文本文件中的所有行
    def ReadLines(self):
        if not self.bOpen:
            return []
        else:
            return self.file.readlines()

    #从文本文件中读取一行
    def ReadLine(self):
        if not self.bOpen:
            return ''
        else:
            return self.file.readline()

    #向文本文件中写入一行
    def WriteLine(self, str):
        if self.bOpen:
            return self.file.write(str+'\n')

    def Write(self, str):
        if self.bOpen:
            return self.file.write(str)

    def WriteLines(self, str):
        if self.bOpen:
            return self.file.writelines(str)

    #关闭文件
    def Close(self):
        if self.bOpen:
            self.file.close()
            self.file = None
            self.bOpen = 0

    #重命名文件
    def Rename(self, newName):
        if self.bOpen:
            self.file.close()
            os.rename()


def ChooseFolder(strTitle):
    dialog = wx.DirDialog(None, strTitle,style = wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    dialog.SetPath(os.getcwd())
    path = ''
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
        
    dialog.Destroy()
    return path

def ChooseOpenFile(strTitle, wc = u'所有文件(*.*)|*.*'):
    dlg = wx.FileDialog(None, 
                        message=strTitle,
                        wildcard=wc ,
                        style=wx.OPEN
                        )
    fileName = ''
    if dlg.ShowModal() == wx.ID_OK:
        fileName = dlg.GetPath()
            
    dlg.Destroy()
    return fileName

def ChooseSaveFile(strTitle, wc = u'所有文件(*.*)|*.*'):
    dlg = wx.FileDialog(None, 
                        message=strTitle,
                        wildcard=wc ,
                        style=wx.SAVE
                        )
    fileName = u''
    if dlg.ShowModal() == wx.ID_OK:
        fileName = dlg.GetPath()
            
    dlg.Destroy()
    return fileName
