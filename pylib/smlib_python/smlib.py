# -*- coding: utf-8 -*-
 
import sys
import string
import os

# 初始化 pylib 环境：smu.pyd
def load_smlib():
    """ Initialize GIScript Environment,Load Library smu.pyd.
	smlibpath should be changed according to your os
    """
    smlibpath=os.path.dirname(__file__) + "/bin_version/7.1/Linux64/"
    smupath=smlibpath+"/bin/smu.so"
    if os.path.exists(smupath):
        sys.path.append(smlibpath)
        print "smlib set smu path: ",smlibpath
    else:
        print "file not exist",smupath

    
def version():
    print "GIScript Version 0.0.1"
    print "Copyright, SuperMap Software Inc."
