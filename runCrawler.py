"""
  TODO
"""

# Library Imports
import lxml.html
from io import StringIO, BytesIO

# Local Module Imports
from parseHtml import ParseHtml, getHtml

def main():
  #html_string = getHtml('http://localhost/davidmoench.com')
  p = ParseHtml('http://nytimes.com')
  print p.getLinks()
  """
  html = lxml.html.fromstring(html_string)
  html.make_links_absolute('http://davidmoench.com')
  links = [l[2] for l in html.iterlinks()]
  print links
  """

if __name__ == '__main__':
  main()
