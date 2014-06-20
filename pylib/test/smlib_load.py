# -*- coding: utf-8 -*-
 
import sys
import string
import os

#Init GIScript environment.
def smlib_init():
    """ Initialize GIScript Environment,Load Library.
    """
    smlib_path=os.path.dirname(sys.path[0]+"/../smlib_python/")
    print "smlib path: ", smlib_path
    sys.path.append(smlib_path)

if __name__=='__main__':
    smlib_init()
    
    import smlib
    smlib.version()
    sys.exit()

