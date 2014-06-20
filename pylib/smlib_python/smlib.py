# -*- coding: utf-8 -*-
 
import sys
import string
import os

# 初始化 pylib 环境
def load_smlib():
    """ Initialize GIScript Environment,Load Library.
    """
    smlibpath=os.path.dirname(sys.path[0])
    print "Load Lib: ",smlibpath
    sys.path.append(smlibpath)

    
def version():
    print "GIScript Version 0.0.1"
    print "Copyright, SuperMap Software Inc."
