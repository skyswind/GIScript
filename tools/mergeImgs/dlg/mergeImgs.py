#coding: utf-8

import  wx
import tk.filetk as tk
import smBase as smBase
import smEngine as smu
import math

class mergeImgs(wx.Frame):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):

        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        panel = wx.Panel(self, -1)

        #===============================================
        #
        ypos = 20
        xpos = 15

        l1 = wx.StaticText(panel, -1, u"选择文件夹")
        l1.SetPosition((xpos,ypos))

        self.t1 = wx.TextCtrl(panel, -1, u"",size=(200,-1))
        self.t1.SetPosition((xpos + 80,ypos - 5))

        btnFolder = wx.Button(panel, -1, u"...",size=(25,-1))
        btnFolder.SetPosition((xpos + 285, ypos - 5))
        self.Bind(wx.EVT_BUTTON, self.OnSelFolder, btnFolder)

        l11 = wx.StaticText(panel, -1, u"通配符")
        l11.SetPosition((xpos + 320,ypos))
        self.t11 = wx.TextCtrl(panel, -1, u".*.tif$",size=(50,-1))
        self.t11.SetPosition((xpos + 370,ypos - 5))

        l12 = wx.StaticText(panel, -1, u"类型")
        l12.SetPosition((xpos + 430,ypos))

        sampleList = ['fileTIF', 'fileIMG','fileBMP', 'fileJPG', 'filePNG'
                      ,'fileGIF', 'fileGRD', 'fileRAW'
                      ,'fileUSGSGRID',  'fileSIT'
                      ,'fileArcinfoGrid', 'fileIDR'
                      ,'fileAIBinCov', 'fileGDBRaster', 'fileEMF'
                      ,'fileWMF', 'fileEPS']
        self.c12 = wx.ComboBox(panel, -1, "",(xpos + 470,ypos - 5),(90,-1),sampleList, wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER)
        #===============================================

        #===============================================
        #
        l2 = wx.StaticText(panel, -1, u"目标数据源")
        l2.SetPosition((15,60))

        self.t2 = wx.TextCtrl(panel, -1, "",size=(450,-1))
        self.t2.SetPosition((95,55))

        btnFile = wx.Button(panel, -1, "...",size=(25,-1))
        btnFile.SetPosition((550, 55))
        self.Bind(wx.EVT_BUTTON, self.OnSelFile, btnFile)
        #===============================================

        #===============================================
        #
        l3 = wx.StaticText(panel, -1, u"目标数据集")
        l3.SetPosition((15,100))

        self.t3 = wx.TextCtrl(panel, -1, "",size=(480,-1))
        self.t3.SetPosition((95,95))
        #===============================================



        #===============================================
        #
        pos = 15
        l4 = wx.StaticText(panel, -1, u"数据集类型")
        l4.SetPosition((pos,140))

        sampleList = ['Image', 'DEM', 'GRID']

        self.c4 = wx.ComboBox(panel, -1, "",(pos + 80,135),(80,-1),sampleList, wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER)
        #===============================================

        #===============================================
        #
        pos = 200
        l5 = wx.StaticText(panel, -1, u"编码类型")
        l5.SetPosition((pos,140))

        sampleList = ['encNone', 'encDCT', 'encLZW']

        self.c5 = wx.ComboBox(panel, -1, "",(pos + 65,135),(90,-1),sampleList, wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER)
        #===============================================
        


        #===============================================
        #
        pos = 380
        l6 = wx.StaticText(panel, -1, u"像素格式")
        l6.SetPosition((pos,140))

        sampleList = ['IPF_MONO', 'IPF_FBIT', 'IPF_UBYTE', 'IPF_BYTE', 'IPF_TBYTE', 'IPF_UTBYTE', 
                      'IPF_RGB', 'IPF_RGBA', 'IPF_TRGB', 'IPF_LONG', 'IPF_ULONG', 'IPF_LONGLONG', 
                      'IPF_FLOAT', 'IPF_DOUBLE']

        self.c6 = wx.ComboBox(panel, -1, "",(pos + 70,135),(105,-1),sampleList, wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER)
        #===============================================

        #===============================================
        #
        l7 = wx.StaticText(panel, -1, u"数据集范围")
        l7.SetPosition((15,180))

        pos = 100
        l71 = wx.StaticText(panel, -1, u"[左]")
        l71.SetPosition((pos,180))
        self.t71 = wx.TextCtrl(panel, -1, "",size=(80,-1))
        self.t71.SetPosition((pos + 30,175))

        pos += 120
        l72 = wx.StaticText(panel, -1, u"[上]")
        l72.SetPosition((pos,180))
        self.t72 = wx.TextCtrl(panel, -1, "",size=(80,-1))
        self.t72.SetPosition((pos + 30,175))

        pos += 120
        l73 = wx.StaticText(panel, -1, u"[右]")
        l73.SetPosition((pos,180))
        self.t73 = wx.TextCtrl(panel, -1, "",size=(80,-1))
        self.t73.SetPosition((pos + 30,175))

        pos += 120
        l74 = wx.StaticText(panel, -1, u"[下]")
        l74.SetPosition((pos,180))
        self.t74 = wx.TextCtrl(panel, -1, "",size=(80,-1))
        self.t74.SetPosition((pos + 30,175))
        #===============================================

        #===============================================
        #
        pos = 15
        ypos = 220
        l8 = wx.StaticText(panel, -1, u"水平分辨率")
        l8.SetPosition((pos,ypos))

        self.t8 = wx.TextCtrl(panel, -1, "",size=(190,-1))
        self.t8.SetPosition((pos + 80,ypos - 5))

        pos+= 280
        l9 = wx.StaticText(panel, -1, u"垂直分辨率")
        l9.SetPosition((pos,ypos))

        self.t9 = wx.TextCtrl(panel, -1, "",size=(190,-1))
        self.t9.SetPosition((pos + 80,ypos - 5))
        #===============================================


        #===============================================
        #
        pos = 15
        ypos = 260
        l8 = wx.StaticText(panel, -1, u"宽度(像素)")
        l8.SetPosition((pos,ypos))

        self.tWidth = wx.TextCtrl(panel, -1, "",size=(190,-1))
        self.tWidth.SetPosition((pos + 80,ypos - 5))

        pos+= 280
        l9 = wx.StaticText(panel, -1, u"高度(像素)")
        l9.SetPosition((pos,ypos))

        self.tHeight = wx.TextCtrl(panel, -1, "",size=(190,-1))
        self.tHeight.SetPosition((pos + 80,ypos - 5))
        #===============================================


        xpos = 60
        ypos = 300
        btnWidth = 150
        btnGetBounds = wx.Button(panel, -1, u"获取范围和分辨率",pos = (xpos, ypos),size=(btnWidth,-1))
        self.Bind(wx.EVT_BUTTON, self.OnGetInfo, btnGetBounds)

   
        xpos+=170
        btnMerge = wx.Button(panel, -1, u"拼接影像",pos = (xpos, ypos),size=(btnWidth,-1))
        self.Bind(wx.EVT_BUTTON, self.OnMerge, btnMerge)

        xpos+=170
        btnClose = wx.Button(panel, -1, u"放弃操作",size=(btnWidth,-1))
        btnClose.SetPosition((xpos, ypos))

        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, btnClose)


        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)


    def OnCloseMe(self, event):
        self.Close(True)

    def OnMerge(self, event):
        uds = smu.uds(self.t2.Value, u'uds')
        uds.Create()
        dtName = self.t3.Value
        fileType = self.c12.Value
        uds.CreateRaster(dtName, self.c4.Value, self.c5.Value, self.c6.Value, 256, 
                         float(self.t71.Value), float(self.t72.Value), float(self.t73.Value), float(self.t74.Value), 
                         float(self.t8.Value), float(self.t9.Value))

        nCount = 0
        for file in self.fl.FileLists:
            print file
            uds.AppendRasterFile(dtName, fileType, file)
            nCount += 1

        uds.Close()
        info = u'拼接成功：共拼接[%d]幅影像' % (nCount)
        wx.MessageBox(info, u'影像拼接', wx.OK)

    #��ȡӰ��ķ�Χ�ͷֱ��ʵ���Ϣ
    def OnGetInfo(self, event):
        if len(self.t1.Value)<1:
            dlg = wx.MessageDialog(self, u'请选择文件夹',
                               u'请选择文件夹',
                               wx.OK | wx.ICON_INFORMATION
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()
            return False

        if len(self.c12.Value)<1:
            dlg = wx.MessageDialog(self, u'请选择文件类型',
                               u'请选择文件类型',
                               wx.OK | wx.ICON_INFORMATION
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()
            return False

        self.fl = tk.Folder(self.t1.Value)
        self.fl.reMatch = self.t11.Value
        self.fl.GetFileLists()

        bInit = True

        for file in self.fl.FileLists:
            info = smBase.GetImgFileInfo(file, self.c12.Value)
            if bInit:
                self.t71.Value = str(info.bounds.left)
                self.t72.Value = str(info.bounds.top)
                self.t73.Value = str(info.bounds.right)
                self.t74.Value = str(info.bounds.bottom)
                self.t8.Value = str(info.resX)
                self.t9.Value = str(info.resY)

                bInit= False
            else:
                if info.bounds.left<float(self.t71.Value):
                    self.t71.Value = str(info.bounds.left)
                if info.bounds.top>float(self.t72.Value):
                    self.t72.Value = str(info.bounds.top)
                if info.bounds.right>float(self.t73.Value):
                    self.t73.Value = str(info.bounds.right)
                if info.bounds.bottom<float(self.t74.Value):
                    self.t74.Value = str(info.bounds.bottom)
                if info.resX<float(self.t8.Value):
                    self.t8.Value = str(info.resX)
                if info.resY<float(self.t9.Value):
                    self.t9.Value = str(info.resY)
        
        width = int(math.ceil((float(self.t73.Value)-float(self.t71.Value))/float(self.t8.Value)))
        Height = int(math.ceil((float(self.t72.Value)-float(self.t74.Value))/float(self.t9.Value)))

        self.tWidth.Value = str(width)
        self.tHeight.Value = str(Height)

    def OnSelFolder(self, event):
        folder = tk.ChooseFolder(u"选择文件夹")
        self.t1.Value = folder

    def OnSelFile(self, event):
        folder = tk.ChooseSaveFile(u"目标数据源",u'UDB数据源(*.udb)|*.udb')
        self.t2.Value = folder

    def OnCloseWindow(self, event):
        self.Destroy()
