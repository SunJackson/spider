#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy import cmdline

def multspider():
    cmdl = "scrapy crawlall Crawler 10"
    cmdline.execute(cmdl.split(' '))


if __name__ == "__main__":
    multspider()
