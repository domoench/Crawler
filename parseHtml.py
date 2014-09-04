"""
  A class for parsing and querying an HTML page.
"""

# Library Imports
import requests
from urlparse import urlparse
from lxml import etree
import lxml.html
from io import StringIO, BytesIO

# Local Module Imports

class ParseHtml:

  def __init__(self, url_string):
    html_string = getHtml(url_string)
    parser      = etree.HTMLParser()
    tree        = etree.parse(StringIO(html_string), parser)
    self.root   = tree.getroot()
    self.up     = urlparse(url_string)

  def getLinks(self):
    html_string = etree.tostring(self.root)
    html = lxml.html.fromstring(html_string)
    html.make_links_absolute(self.up.scheme + '://' + self.up.netloc) #TODO
    links = [l[2] for l in html.iterlinks()]
    return links
    #return list(elem.get('href') for elem in self.root.iter('a'))

  def getResources(self):
    assert False

  def sameDomain(url_string):
    """
    Return whether the given url string is in this ParseHtml instance's domain.
    """
    return self.domain == urlparse(url_string).netloc

"""
  Helper Functions
"""

def getHtml(url_string):
  """
  Make an HTTP request to the given url string and return the HTML string.
  """
  r = requests.get(url_string)

  if r.status_code != 200:
    raise Exception()

  return unicode(r.content, 'UTF-8')

