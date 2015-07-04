#!/usr/bin/env python  
# -*- coding: utf-8 -*-
#  
# Openwrt Package Grabber  
#  
# Copyright (C) 2014 http://shuyz.com
# modified by jemyzhang@2015.7
#
# Usage:
# for WNDR4300/3700:
# python openwrt_package_grabber.py http://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/nand/packages/ ./packages

import urllib2
import re
import os


def save_packages(url, location):
    location = os.path.abspath(location) + os.path.sep
    if not os.path.exists(location):
        os.makedirs(location)
    print 'fetching package list from ' + url
    content = urllib2.urlopen(url, timeout=15).read()

    print 'packages list ok, analysing...'
    pattern = r'<a href="(.*?)">'
    items = re.findall(pattern, content)

    cnt = 0
    for item in items:
        if item == '../':
            continue
        elif item[-1] == '/':
            save_packages(url + item, location + item)
        else:
            cnt += 1
            item = item.replace('%2b', '+')
            print 'downloading item %d: ' % (cnt) + item
            if os.path.isfile(location + item):
                print 'file exists, ignored.'
            else:
                rfile = urllib2.urlopen(url + item)
                with open(location + item, "wb") as code:
                    code.write(rfile.read())


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print 'Usage: %s [openwrt url] [save location]'
    else:
        save_packages(sys.argv[1], sys.argv[2])
