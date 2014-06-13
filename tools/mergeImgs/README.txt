影像拼接界面工具（wxPython + SuperMapPython）

运行脚本 testMergeImg.py


一、Visual Studio 2012 环境配置（Windows）
1、下载安装 wxPython，默认安装在所使用的Python安装程序lib文件夹下的site-packages中（Windows、Linux中site-packages文件夹所在位置不同）；
2、如将wxPython安装在其它目录下，则需将安装目录加入Python环境变量；
3、下载安装 PTVS 2.0 VS 2012.msi插件 
4、之后就可直接打开pySuperMap.sln解决方案，进行相应功能的开发

二、Linux配置说明
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





