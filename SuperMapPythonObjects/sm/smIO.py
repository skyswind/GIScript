#coding: utf-8
#DataProcessing
#数据处理的方法放到这个文件里

import smEngine as py
import sm.tk.filetk as tk

class DataPump:
    def __init__(self):
        self.bOK = 0

    #Sample: ImportGrids('D:\\Data\\SRTM', '.*.tif', 'D:\\Data\\UDB', 'encLZW', 'fileTIF')
    def ImportGrids(self, srcPath, reMatch, destPath, encType, fileType):
        #获取文件夹中要导入的文件的列表，结果在fl.FileLists中
        fl = tk.Folder(srcPath)
        fl.reMatch = reMatch
        fl.GetFileLists()

        #逐项处理
        for file in fl.FileLists:
            #定义UDB数据源
            nds = py.uds(destPath+'\\'+file[-14:-4]+'.udb', 'udbAlias');
            nds.Create()
            nds.ImportGrid(file[-14:-4],encType, fileType, file)
            nds.Close()






