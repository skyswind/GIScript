

一、目录结构

   ---- pyLib 			基于SuperMap Python接口的Python Objects
   |	-- smBase.py		基础类，提供一些基础类和基本功能
   |	-- smData.py		空间数据引擎基类，提供对数据源、数据集的相关操作
   |	-- smEngine.py		空间数据引擎类型封装


二、lib 环境配置
   1、从 lib 文件夹下载对应平台的压缩包，解压；
   2、将解压后的 smy.pyd 所在路径设置到Python环境变量
      环境变量添加可使用以下方法的一种：
	1）将路径加入到PYTHONPATH环境变量中；
	2）将路径加入到Python安装目录下后缀名为.pth的文件中，一行一个路径；如果没有后缀名为.pth的文件，则新建个即可；
	3）Python脚本中指定 sys.path.append()

三、SuperMap Python 对 Unicode 的支持
    建议 Python 脚本中指定默认字符集为utf-8，方法如下：
    ......
	reload(sys)
    sys.setdefaultencoding("utf-8")
	......

    可参见 pyLib\test\AppendRasterFile.py

四、注意事项
    用 7.1 版本导入的UDB栅格数据在旧版本中无法操作。


