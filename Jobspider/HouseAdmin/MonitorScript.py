# -*- coding: utf-8 -*-
#!/usr/bin/python
from scrapy import cmdline
import multiprocessing
import time
from scripts import LoadUrl
import os
def multspider(script):
    nowpath = os.path.split(os.path.realpath(__file__))[0] +'/'
    cmdl = "python %smanage.py runscript %s" % (nowpath,script)
    p = os.popen(cmdl)
    print(p.read())
def run():

    scriptname = 'LoadInfo'
    multspider(scriptname)

if __name__ == "__main__":
    run()


