# -*- coding: utf-8 -*-
 
import sys
import string
import os

#
def load_smlib_ugc():
    """ Initialize GIScript Environment,Load Library UGC.
	smlib_ugc should be changed according to your os
    """
    #smlib_ugc = os.path.dirname(__file__) + "/../lib/7.1/Linux64/ugc_710_64_x64_linux_gcc_Bin/"
    smlib_ugc = "/media/supermap/Application/GeoScript/GIScript/lib/7.1/Linux64/ugc_710_64_x64_linux_gcc_Bin/"
    
    print "smlib_ugc path: ",smlib_ugc
    sys.path.append(smlib_ugc)
    
    
# 初始化 pylib 环境：smu.pyd
def load_smlib():
    """ Initialize GIScript Environment,Load Library smu.pyd.
	smlibpath should be changed according to your os
    """
    smlibpath=os.path.dirname(__file__) + "/bin_version/7.1/Linux64/bin/"
    smupath=smlibpath+"smu.so"
    if os.path.exists(smupath):
        sys.path.append(smlibpath)
        print "smlib set smu path: ",smlibpath
    else:
        print "file not exist: ",smupath

    
def version():
    print "GIScript Version 0.0.1"
    print "Copyright, SuperMap Software Inc."
