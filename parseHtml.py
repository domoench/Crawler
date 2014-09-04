"""
  A class for parsing and querying an HTML page.
"""

# Library Imports
import requests
from urlparse import urlparse, urljoin
from lxml import etree
import lxml.html
from io import StringIO, BytesIO

# Local Module Imports

class ParseHtml:

  def __init__(self, url_string):
    html_string   = getHtml(url_string)
    parser        = etree.HTMLParser()
    tree          = etree.parse(StringIO(html_string), parser)
    self.root     = tree.getroot()
    self.up       = urlparse(url_string)
    self.base_url = self.up.scheme + '://' + self.up.netloc

    self.links    = []
    self.assets   = []

    # Parse <a> tags for links and assets
    for e in self.root.iter('a'):
      link = urljoin(self.base_url, e.get('href'))
      if link[-4:] == '.pdf':
        self.assets += [link]
      else:
        self.links += [link]

    # Parse <link> tags for assets
    for e in self.root.iter('link'):
      link = urljoin(self.base_url, e.get('href'))
      self.assets += [link]

    # Parse <script> tags for assets
    for e in self.root.iter('script'):
      link = urljoin(self.base_url, e.get('src'))
      self.assets += [link]

    # Parse <img> tags for assets
    for e in self.root.iter('img'):
      link = urljoin(self.base_url, e.get('src'))
      self.assets += [link]


  def getLinks(self):
    return self.links

  def getAssets(self):
    return self.assets

  def sameDomain(self, url_string):
    """
    Return whether the given url string is in this ParseHtml instance's domain.
    """
    up = urlparse(url_string)
    return self.base_url == up.scheme + '://' + up.netloc

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

