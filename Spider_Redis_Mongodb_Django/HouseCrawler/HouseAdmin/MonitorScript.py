# -*- coding: utf-8 -*-
#!/usr/bin/python
import time
import os

def multspider(script):
    nowpath = os.path.split(os.path.realpath(__file__))[0] +'/'
    cmdl = "python3.4 %smanage.py runscript %s" % (nowpath,script)
    p = os.popen(cmdl)
def run():
    scriptname = 'LoadInfo'
    multspider(scriptname)
    # scriptname = 'LoadUrl'
    # multspider(scriptname)
if __name__ == "__main__":
    run()



