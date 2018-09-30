#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy import cmdline


def multspider():
    cmdl = "scrapy crawlall IpCrawler 200 IpCrawler"
    cmdline.execute(cmdl.split(' '))


if __name__ == "__main__":
    multspider()
