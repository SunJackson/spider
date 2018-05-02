#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy import cmdline

def multspider():
    cmdl = "scrapy crawlall Crawler 1 Crawler:start_urls:Default"
    cmdline.execute(cmdl.split(' '))


if __name__ == "__main__":
    multspider()
