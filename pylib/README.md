
下载lib库，解压到文件夹 smbin（eg:smbin/smu.pyd）
Linux平台环境变量 LD_LIBRARY_PATH 添加 smbin 目录
	eg：export LD_LIBRARY_PATH=/home/map/GIScript/pylib/smbin:$LD_LIBRARY_PATH

执行 python ./test/testOpenUDBDS.py

注意事项
	1、Python建议使用2.7.3
    2、用 7.1 版本导入的UDB栅格数据在旧版本中无法操作。


