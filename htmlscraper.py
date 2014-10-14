#!/usr/bin/env python

#
# This function uses Splinter to scrape a given page's HTML, and
# writes out the HTML to a specified file.
#
# Dane Fichter - 10/11/14

import sys
import codecs
from splinter import Browser

def main():

  if len(sys.argv) != 3:
    print "USAGE: python htmlscraper.py <URL> <OUTPUT FILE>"
    sys.exit(1)

  #load up the desired page and save the html#
  with Browser() as browser:
    url = sys.argv[1]
    filename = sys.argv[2]
    browser.visit(url)
    html_string = browser.html
    f = codecs.open(filename, encoding="utf-8", mode="w")
    f.write(html_string)
    f.close()


if __name__ == '__main__':
  main()
