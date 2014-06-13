#coding: utf-8
import os
import smEngine as sm
import smBase as smBase


#测试基础功能，不需要使用数据源、数据集类对象
#测试影像信息获取；
#info = smBase.GetImgFileInfo(u'/home/analyst/chenwei/S_Band_16bit_超图/ASTGTM_N39E091P_超图.img', u'fileIMG')
info = smBase.GetImgFileInfo(u'/home/analyst/chenwei/tif/sc_超图.tif', u'fileTIF')
info.dump()
#fileType = smBase.GetFileTypeByFileName(u'G:\\Data\\raster\\tif\\sc_17_0326_超图.tif')

#测试是否使用FME
#smBase.SetUseFME(1)


#测试数据源、数据集类
#测试UDB引擎
fileName = u"G:\\Data\\raster\\test超图.udb"
#创建UDB数据源类对象
#uds = sm.uds(fileName)
#uds.Open()
#uds.DeleteDataset(u"testVector")
#uds.CreateVector(u"testVector", u"Line", u"encNONE")
#得到数据集类对象
#dt = uds.GetDataset(u"Ocean_Label")

#测试导入导出
#uds.ExportVector(u"Ocean_Label", u"fileSHP", ur"G:\aaa.shp")
#uds.ExportRaster(u"T24bit1_超图", u"fileIMG", ur"G:\rrr.img")
#uds.ImportVector(u"newImport", u"encNONE", u"fileSHP", ur"G:\aaa.shp", u"GIS")
#uds.ImportImage('imptest', 'encDCT', 'fileIMG', r'G:\Data\raster\全国影像00121.img')

#测试字段索引
#dt.BuildFieldIndex(u"SmID")
#dt.DropFieldIndex(u"SmID")

#测试数据集、数据源投影转换
#dt = uds.GetDataset(u"Ocean_Label")
#dt.ChangeVectorProjection(uds.alias, u"prjVector", ur"G:\prj.xml")
#dt = uds.GetDataset(u"T1")
#dt.ChangeRasterProjection(uds.alias, u"prjRaster", ur"G:\prj84.xml")
#uds.ChangeProjection(ur"G:\prj84.xml")

#测试数据集投影设置
#smBase.GetProjection(u"fileIMG", ur"G:\Data\raster\河北省SPOT正射影像\275-265jz.img", ur"G:\prj.xml")
#dt = uds.GetDataset(u"R")
#dt.SetProjection(u"G:\\prj.xml")

#测试一些常用功能
#得到需要操作的数据集
#dt = uds.GetDataset(u"T1")
#影像拉伸
#dt.StretchRaster(u"T2")
#重新计算范围
#print dt.ComputeBounds();
#根据模板创建数据集
#uds.CreateDatasetFrom(dt.name, uds.alias, u"newCre", u"encNONE")
#查询
#dt.Query(uds.alias, u"queryRes", u"SmID < 100", u"encNONE", u"Static")
#设置裁剪区域
#dt.SetClipRegion(uds.alias, u"R", 2)
#数据集复制
#uds.CopyDataset(name, uds.alias, u"newdt_1")
#删除数据集
#uds.DeleteDataset(name)

#测试影像金字塔
#dt.RemovePyramid()
#dt.BuildPyramidTiersOnly()
#dt.UpdatePyramid(20253071, 4679009, 20343421, 4643329)

#测试遍历数据源中的数据集
#for name in uds.GetAllDatasetName():
    #print name
    #res = uds.GetDatasetInfo(name);
    #print res[0][0]

#测试完毕，关闭数据源
#uds.Close()

#测试Oracle引擎
#oracleds = sm.oracleds('map', 'map1', 'map');
##oracleds.Create();
#oracleds.Open()
##oracleds.ImportImage('imptest', 'encDCT', 'fileIMG', r'G:\Data\raster\全国影像00121.img')
##for name in oracleds.DtNames:
##    print name
#oracleds.Close()

#测试SQL Server引擎
#sqlds = sm.sqlds('192.168.114.43', 'map2', 'sa', 'supermap');
##sqlds.Create();
#sqlds.Open()
##sqlds.ImportImage('imptest', 'encDCT', 'fileIMG', r'G:\Data\raster\全国影像00121.img')
#for name in sqlds.DtNames:
#    print name
#sqlds.Close()

#测试PostgreSQL引擎
#pgds = sm.pgds('192.168.120.204', 'map2', 'map', 'map');
##pgds.Create();
#pgds.Open()
##pgds.ImportImage('imptest', 'encDCT', 'fileIMG', r'G:\Data\raster\全国影像00121.img')
#for name in pgds.DtNames:
#    print name
#pgds.Close()

#测试DB2引擎
#db2ds = sm.db2ds('map10', 'db2admin', 'map')
##db2ds.Create()
#db2ds.Open()
##db2ds.ImportImage('imptest', 'encDCT', 'fileIMG', r'G:\Data\raster\全国影像00121.img')
#for name in db2ds.DtNames:
#    print name
#db2ds.Close()

#测试Oracle Spatial引擎
#osp = sm.oraclespatialds('map', 'osp3', 'osp')
##osp.Create()
#osp.Open()
##osp.ImportImage('imptest', 'encDCT', 'fileIMG', r'G:\Data\raster\全国影像00121.img')
#for name in osp.DtNames:
#    print name
#osp.Close()
