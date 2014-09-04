"""
  TODO
"""

# Library Imports
import lxml.html
from lxml import etree
from io import StringIO, BytesIO

# Local Module Imports
from parseHtml import ParseHtml, getHtml

def main():
  p = ParseHtml('http://davidmoench.com/fmri-viz.php')
  print 'links', p.getLinks()
  print 'assets', p.getAssets()

if __name__ == '__main__':
  main()
