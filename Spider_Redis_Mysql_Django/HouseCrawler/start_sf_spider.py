#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy import cmdline
import time


def multspider():
    cmdl = "scrapy crawlall SFCrawler 3 SFCrawlers:start_urls:Default"
    cmdline.execute(cmdl.split(' '))


if __name__ == "__main__":
    multspider()
