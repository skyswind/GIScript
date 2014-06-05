一、根目录sm说明
Python类库根目录
sm	
	将组件包Bin下的文件拷贝到此文件夹下
	--bin	
	    __init__.py			bin作为python包，需加上此文件
	界面类
	--dlg	
		mergeImgs.py
		testMergeImg.py		影像文件拼接界面
	测试类
	--test	
		testData.py
		testMergeImage.py
		testOthers.py
		testTk.py
	常用工具类
	--tk	s
		basetk.py
		filetk.py
		imgtk.py
	pySuperMap.sln	Python Visual Studion 2012 解决方案
	smBase.py		基础类，提供一些基础类和基本功能
	smData.py		空间数据引擎基类，提供对数据源、数据集的相关操作
	smEngine.py		空间数据引擎类型封装
	smIO.py			数据处理类
注意：需要将所使用的组件包Bin下的所以文件拷贝到sm/bin下
	
三、sm 路径说明
sm文件夹默认是需要放在Python可执行程序的同级目录下，这样不用设置任何环境变量，即可直接使用SuperMap Python;
如果不放在Python安装目录下，则此时需要将sm文件夹所在的路径加入环境变量中；
环境变量添加可使用下两种方法的一种：
1、将sm文件夹所在路径加入到PYTHONPATH环境变量中；
2、将sm文件夹所在路径加入到Python安装目录下后缀名为.pth的文件中，一行一个路径；如果没有后缀名为.pth的文件，则新建个即可；
3、Windows、Linux都建议使用PYTHONPATH环境变量，比较方便；

二、Windows Python 环境配置
1、将下载的SuperMap Python库文件夹sm拷贝到Python可执行程序的同级目录下；比如：C:\Python27
2、将SuperMap组件拷贝到sm/bin目录下

三、Visual Studio 2012 环境配置（Windows）
1、下载安装 wxPython，默认安装在所使用的Python安装程序lib文件夹下的site-packages中（Windows、Linux中site-packages文件夹所在位置不同）；
2、如将wxPython安装在其它目录下，则需将安装目录加入Python环境变量；
3、下载安装 PTVS 2.0 VS 2012.msi插件 
4、之后就可直接打开pySuperMap.sln解决方案，进行相应功能的开发

四、Linux配置说明
1、将Python类库sm文件夹路径加入PYTHONPATH环境变量或将其放在Python可执行程序的同级目录下；
2、SuperMap Python使用的Python版本为2.7.3；如果Linux默认不是该版本，则需要将安装的2.7.3版本的Python加入系统环境变量Path中；
3、配置wxPython
(1)下载wxPython3.0.0源码
(2)进入解压目录，编译wxwidgets; 依次执行./configure  make make install即可，也可指定安装路径；
(3)编译wxPython；执行
   python setup.py build_ext --inplace WX_CONFIG=/usr/local/bin/wx-config
   （其中python为2.7.3版本；/usr/local/为wxwidgets默认安装路径）
(4)将wxPython源码下的lib路径加入系统LD_LIBRARY_PATH环境变量中；此lib路径也可是安装的wxwidgets路径下的lib;
(5)将wxPython源码下的wxPython路径加入PYTHONPATH环境变量中；
(6)例如，Linux下需要如下进行设置环境变量：
   sm类库文件夹、wxPython源码wxPython-src-3.0.0.0、Python安装文件夹(python273)均放在/home/analyst用户目录下

   #sm类库、编译后源码下的wxPython
   export PYTHONPATH=/home/analyst:/home/analyst/wxPython-src-3.0.0.0/wxPython
   #SuperMap组件包的bin
   export OBJECTS_LIB=/home/analyst/sm/bin
   #编译的wxwidgets的lib
   export WX_LIB=/home/analyst/wxPython-src-3.0.0.0/lib
   #Python可执行程序路径，2.7.3版本；如果系统默认为此版本，则无需进行设置
   export PYTHON_BIN=/home/analyst/python273/bin
   export PATH=$PYTHON_BIN:/usr/sbin:$PATH
   export LD_LIBRARY_PATH=/usr/lib64:/lib64:/usr/libexe:/usr/lib:/lib:/usr/local/lib:$OBJECTS_LIB/:$WX_LIB:$LD_LIBRARY_PATH
(7)以上设置完成后；直接执行 python /home/analyst/sm/dlg/testMergeImg.py 即可启动“拼接影像文件”对话框





