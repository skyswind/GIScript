#coding: utf-8
#基础类，数据源、数据集、工作空间等对象放到这里

import os
import sys
import math
import smBase
#import bin.smu as smu
import smu
smu.Init()

#数据集的基类
class dt:
    def __init__(self, ds, name = u''):
        self.ds = ds
        self.name = name

    #设置数据集投影
    #strPrjFilePath 投影文件完整路径
    def SetProjection(self, strPrjFilePath):
        if smu.SetProjection(self.ds.alias, self.name, strPrjFilePath):
            return True
        return False
    
    #设置栅格数据集范围
    #dtName 数据集名;
    #dLeft 范围left;
    #dTop 范围top;
    #dRight 范围right;
    #dBottom 范围bottom;
    def SetGeoReference(self, dLeft, dTop, dRight, dBottom):
        return smu.SetGeoReference(self.ds.alias, self.name, dLeft, dTop, dRight, dBottom)

    #设置影像或栅格数据集无值
    def SetNoValue(self, dNoValue):
        return smu.SetNoValue(self.ds.alias, self.name, dNoValue)
    
    #设置影像或栅格数据集的裁剪区域；如果数据集不是面数据集或指定SmID不存在，则清空裁剪区域
    #dsName，矢量数据集所在的数据源
    #dtVectorName，裁剪多边形所在的矢量数据集
    #nSmID，取dtVectorName数据集SmID为nSmID的对象做为影像或栅格数据集的裁剪区域
    def SetClipRegion(self, dsName, dtVectorName, nSmID):
        return smu.SetClipRegion(self.ds.alias, self.name, dsName, dtVectorName, nSmID)

    #创建影像金字塔
    def BuildPyramid(self):
        return smu.BuildPyramid(self.ds.alias, self.name)

    #创建影像金字塔层，不含数据
    def BuildPyramidTiersOnly(self):
        return smu.BuildPyramidTiersOnly(self.ds.alias, self.name)

    #根据影像范围更新影像金字塔
    def UpdatePyramid(self, dLeft, dTop, dRight, dBottom):
        return smu.UpdatePyramidByBound(self.ds.alias, self.name, dLeft, dTop, dRight, dBottom)

    #删除金字塔
    def RemovePyramid(self):
        return smu.RemovePyramids(self.ds.alias, self.name)

    #拉伸影像数据集，现仅支持像素格式为无符号8位、RGB、RGBA的多波段影像；拉伸结果为新建数据集
    #strResName 拉伸结果数据集名称;
    def StretchRaster(self, strResName):
        if smu.StretchRaster(self.ds.alias, self.name, strResName):
            return True
        return False

    #为矢量数据集创建空间索引
    #nIndexType 空间索引类型;
    #- 2 R树索引
    #- 3 四叉树索引
    #- 4 图幅索引
    #- 5 分层格网索引
    def BuildSpatialIndex(self, nIndexType):
        return smu.BuildSpatialIndex(self.ds.alias, self.name, nIndexType)

    #重建矢量数据集空间索引
    def ReBuildSpatialIndex(self):
        return smu.ReBuildSpatialIndex(self.ds.alias, self.name)

    #删除矢量数据集空间索引
    def DropSpatialIndex(self):
        return smu.DropSpatialIndex(self.ds.alias, self.name)

    #创建字段索引
    #fieldName 字段名称;
    def BuildFieldIndex(self, fieldName):
        if smu.BuildFieldIndex(self.ds.alias, self.name, fieldName):
            return True
        return False

    #删除字段索引
    #fieldName 字段名称;
    def DropFieldIndex(self, fieldName):
        if smu.DropFieldIndex(self.ds.alias, self.name, fieldName):
            return True
        return False

    #查询矢量数据集，结果保存在指定数据集中
    #dsDstName 结果数据集所在数据源名称;
    #dtDstName 结果数据集名称;
    #filterSQL 查询条件;
    #encType 结果数据集编码类型;取值为:
    #- encBYTE
    #- encWORD
    #- enc3BYTE
    #- encDWORD 复合数据不能用此编码
    #- encDOUBLE
    #- encNONE
    #cursorType 查询游标类型;
    #- Dynamic
    #- Static
    def Query(self, dsDstName, dtDstName, filterSQL, encType, cursorType):
        return smu.Query(self.ds.alias, self.name, dsDstName, dtDstName, filterSQL, encType, cursorType) 

    #计算矢量数据集范围
    def ComputeBounds(self):
        if smu.ComputeBounds(self.ds.alias, self.name):
            return True
        return False

    #从XML中读入投影信息并对矢量数据集进行投影转换
    #strDesDsAlias 目标数据源名称;
    #strNewDtName 目标数据集名称;
    #strXMLPath 投影转换xml文件;
    def ChangeVectorProjection(self, strDesDsAlias, strNewDtName, strXMLPath):
        if smu.ChangeVectorProjection(self.ds.alias, self.name, strDesDsAlias, strNewDtName, strXMLPath):
            return True
        return False

    #从XML中读入投影信息并对影像或栅格数据集进行投影转换
    #strDesDsAlias 目标数据源名称;
    #strNewDtName 目标数据集名称;
    #strXMLPath 投影转换xml文件;
    def ChangeRasterProjection(self, strDesDsAlias, strNewDtName, strXMLPath):
        if smu.ChangeRasterProjection(self.ds.alias, self.name, strDesDsAlias, strNewDtName, strXMLPath):
            return True
        return False



#数据源基类
class ds:
    def __init__(self, alias=u'ds'):
        self.alias = alias
        self.bOpened = 0
        self.type = u'sceUDB'

    #关闭数据源
    def Close(self):
        smu.CloseDataSource(self.alias)
        self.bOpened = 0

    #创建矢量数据集
    #dtType可选值： Tabular, Point, Line, Region, Text, NetWork, CAD, Point3D, Line3D, Region3D
    #encType可选值： encNONE, encBYTE, encWORD, encDWORD, encDOUBLE
    def CreateVector(self, dtName, dtType, encType):
        if smu.CreateDatasetVector(self.alias, dtName, dtType, encType):
            return True
        return False

    #创建栅格数据集（指定地理范围和分辨率）
    #dtType, 数据集类型，可选值：Image; DEM; GRID 
    #encType，编码（压缩）类型，可选值： encNONE; encDCT; encSGL; encLZW; encCompound
    #pixFormat，像素格式， 可选值：
    #   IPF_MONO; 
    #   IPF_FBIT; 
    #   IPF_UBYTE; 
    #   IPF_BYTE; 
    #   IPF_TBYTE; 
    #   IPF_UTBYTE; 
    #   IPF_RGB; 
    #   IPF_RGBA; 
    #   IPF_TRGB; 
    #   IPF_LONG; 
    #   IPF_ULONG; 
    #   IPF_LONGLONG; 
    #   IPF_FLOAT; 
    #   IPF_DOUBLE;
    #iBlkSize, 影像块大小，可选值：64， 128， 256， 512， 1024， 2048， 4096， 8192
    #dLeft,
    #dTop,
    #dRight, 
    #dBottom,
    #dResX,
    #dResY,
    #nBandCount, 波段数，默认为1
    #例：ds.CreateRaster('RasterDt', 'Image', 'encDCT', 'IPF_RGB', 256, 71.1, 52.7, 133.5, 14.7, 0.000083, 0.000083)
    def CreateRaster(self, dtName, dtType, encType, pixFormat, iBlkSize, dLeft, dTop, dRight, dBottom, dResX, dResY, nBandCount = 1):
        iWidth = int(math.ceil(float(dRight-dLeft)/float(dResX)))
        iHeight = int(math.ceil(float(dTop-dBottom)/float(dResY)))
        dRight = dLeft+iWidth*dResX
        dBottom = dTop-iHeight*dResY
        if smu.CreateDatasetRaster(self.alias, dtName, dtType, encType,pixFormat, iWidth, iHeight, dLeft, dTop, dRight, dBottom, iBlkSize, nBandCount):
            return True
        return False

    #创建栅格数据集（指定地理范围和宽、高）
    #dtType, 数据集类型，可选值：Image; DEM; GRID 
    #encType，编码（压缩）类型，可选值： encNONE; encDCT; encSGL; encLZW; encCompound
    #pixFormat，像素格式， 可选值：
    #   IPF_MONO; 
    #   IPF_FBIT; 
    #   IPF_UBYTE; 
    #   IPF_BYTE; 
    #   IPF_TBYTE; 
    #   IPF_UTBYTE; 
    #   IPF_RGB; 
    #   IPF_RGBA; 
    #   IPF_TRGB; 
    #   IPF_LONG; 
    #   IPF_ULONG; 
    #   IPF_LONGLONG; 
    #   IPF_FLOAT; 
    #   IPF_DOUBLE;
    #iBlkSize, 影像块大小，可选值：64， 128， 256， 512， 1024， 2048， 4096， 8192
    #dLeft,
    #dTop,
    #dRight, 
    #dBottom,
    #iWidth, 栅格数据集宽度，单位：像素
    #iHeight, 栅格数据集高度，单位：像素
    #nBandCount, 波段数，默认为1
    #例：ds.CreateRaster('RasterDt', 'Image', 'encDCT', 'IPF_RGB', 256, 71.1, 52.7, 133.5, 14.7, 70000, 80000)
    def CreateRaster2(self, dtName, dtType, encType, pixFormat, iBlkSize, dLeft, dTop, dRight, dBottom, iWidth, iHeight, nBandCount = 1):
        if smu.CreateDatasetRaster(self.alias, dtName, dtType, encType,pixFormat, iWidth, iHeight, dLeft, dTop, dRight, dBottom, iBlkSize, nBandCount):
            return True
        return False

    #通过模板创建数据集
    #strSrcDtName 源数据集名称;
    #strDesDsAlias 目标数据源名称;
    #strNewDtName 新数据集名称:
    #strEncType 编码类型,取值为:
    #- encDOUBLE
    #- encBYTE
    #- encWORD
    #- enc3BYTE
    #- encDWORD
    #- encNONE
    #- encDCT
    #- encSGL
    #- encLGL
    #- encLZW
    #- encPNG
    #- encCompound
    def CreateDatasetFrom(self, strSrcDtName, strDesDsAlias, strNewDtName, strEncType):
        if smu.CreateDatasetFrom(self.alias, strSrcDtName, strDesDsAlias, strNewDtName, strEncType):
            return True
        return False
    
    #复制数据集
    #strSrcName 原数据集名称
    #strDesAlias 目标数据源别名
    #strDesName 目标数据集名称
    def CopyDataset(self, strSrcName, strDesAlias, strDesName):
        return smu.CopyDataset(self.alias, strSrcName, strDesAlias, strDesName)

    #删除数据集
    #dtName, 数据集名
    def DeleteDataset(self, dtName):
        return smu.DeleteDataset(self.alias, dtName)

    #以追加的方式导入影像数据集
    # dtName, 
    # imgType, 
    # fileName,
    #Sample: 
    def AppendRasterFile(self, dtName, imgType, fileName):
        return smu.AppendRasterFile(self.alias, dtName, imgType, fileName)

    #以追加的方式导入影像数据集
    # dtName, 
    # imgType, 
    # fileName,
    # dColor,
    #Sample: 
    def AppendRasterFileIgnoreValue(self, dtName, imgType, fileName,dColor):
        return smu.AppendRasterFileIgnoreColor(self.alias, dtName, imgType, fileName,dColor)

    #以GRID方式导入栅格数据为新数据集
    #dtName -- 新生成数据集的名字
    #encType -- 新数据集编码类型
    #fileType -- 栅格文件的类型
    #fileName -- 栅格文件的全路径及文件名
    def ImportGrid(self, dtName, encType, fileType, fileName):
        if smu.ImportRasterFile(self.alias, dtName,encType,fileType, fileName,1):
            return True
        return False

    #以Image方式导入栅格数据
    def ImportImage(self, dtName, encType, fileType, fileName):
        #最后一个参数标志是否导入为GRID类型，1 -- Is Grid， 0 -- Is not GRID
        if smu.ImportRasterFile(self.alias, dtName,encType,fileType, fileName,0):
            return True
        return False

    #导入指定矢量文件；导入结果为新建数据集
    #strDtName 结果数据集名称,若生成多个数据集,内部自动加“PLRT”等后缀;
    #strEncType 目标数据编码类型,取值为:
    #- encBYTE
    #- encWORD
    #- enc3BYTE
    #- encDWORD
    #- encDOUBLE
    #- encNONE
    #strType 文件类型, 取值为:
    #- fileAIBinCov
    #- fileE00
    #- fileSHP
    #- fileTAB
    #- fileMIF
    #- fileDGN
    #- fileDWG
    #- fileDXF
    #- fileGML
    #- fileMAPGIS
    #- fileKML
    #- fileKMZ
    #- fileGDBVector
    #strFilePath 文件全路径名;
    #strMode 导入为简单数据集(或复合数据集), 取值为:
    #- GIS
    #- CAD
    def ImportVector(self, strDtName, strEncType, strType, strFilePath, strMode):
        if smu.ImportVectorFile(self.alias, strDtName, strEncType, strType, strFilePath, strMode):
            return True
        return False
        
    #导出为矢量文件
    #strName 矢量数据集名称;
    #strType 文件类型, 取值为:
    #- fileAIBinCov
    #- fileE00
    #- fileSHP
    #- fileTAB
    #- fileMIF
    #- fileDGN
    #- fileDWG
    #- fileDXF
    #- fileGML
    #- fileMAPGIS
    #- fileKML
    #- fileKMZ
    #strFilePath 结果文件全路径名;
    def ExportVector(self, strName, strType, strFilePath):
        if smu.ExportVector(self.alias, strName, strType, strFilePath):
            return True
        return False

    #导出为影像文件
    #strName 影像数据集名称;
    #strType 文件类型, 取值为:
    #- fileTIF
    #- fileIMG
    #- fileBMP
    #- fileJPG
    #- filePNG
    #- fileSIT
    #strFilePath 结果文件全路径名;
    def ExportRaster(self, strName, strType, strFilePath):
        if smu.ExportRaster(self.alias, strName, strType, strFilePath):
            return True
        return False

    #获取数据个数
    def GetDatasetCount(self):
        return smu.GetDatasetCount(self.alias)

    #获取所以数据集的名称
    def GetAllDatasetName(self):
        return smu.GetAllDatasetName(self.alias)

    #根据索引获取数据集名
    def GetDatasetName(self, index):
        return smu.GetDatasetName(self.alias, index)

    #根据数据集名获取数据集类型
    def GetDatasetType(self, dtName):
        return smu.GetDatasetType(self.alias, dtName)

    #根据数据集名获取数据集信息（数据集类型和范围）
    #返回为1X4数组，第一个元素为类型，后四个为范围
    def GetDatasetInfo(self, dtName):
        return smu.GetDatasetInfo(self.alias, dtName)

    #返回Python类对象dt，负责数据集的相关操作
    def GetDataset(self, dtName):
        resDT = dt(self, dtName)
        return resDT

    def GetDataset2(self, index):
        dtName = self.GetDatasetName(self, index)
        resDT = dt(self, dtName)
        return resDT

    #从XML中读入投影信息并对数据集进行投影转换
    #strXMLPath 投影转换xml文件;
    def ChangeProjection(self, strXMLPath):
        if smu.ChangeProjection(self.alias, strXMLPath):
            return True
        return False

