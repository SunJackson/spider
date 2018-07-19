#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy import cmdline
import multiprocessing
import time

def multspider():
    cmdl =  "scrapy crawlall ShanghaiCrawler 40 ShanghaiCrawlers:start_urls:Default"
    cmdline.execute(cmdl.split(' '))

if __name__ == "__main__":
    multspider()
  
