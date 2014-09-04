"""
  TODO
"""

# Library Imports
import lxml.html
from lxml import etree
from io import StringIO, BytesIO

# Local Module Imports
from parseHtml import ParseHtml, getHtml
from crawler import Crawler

def main():
  c = Crawler('http://davidmoench.com')
  #c = Crawler('http://digitalocean.com')
  c.outputSitemap()

if __name__ == '__main__':
  main()
