"""
  A class for parsing and querying an HTML page.
"""

# Library Imports
import requests
from urlparse import urlparse, urljoin, urlunparse
from lxml import etree
from io import StringIO, BytesIO

# Local Module Imports

class ParseHtml:

  def __init__(self, url_string):
    self.links    = set() 
    self.assets   = set() 
    self.root     = None
    self.base_url = None

    # Get the page content over HTTP
    html_string = getHtml(url_string)

    if not html_string:
      return
    else:
      parser        = etree.HTMLParser()
      tree          = etree.parse(StringIO(html_string), parser)
      self.root     = tree.getroot()
      self.base_url = domain(url_string) 

      # Parse <a> tags for links and assets
      for e in self.root.iter('a'):
        link = urljoin(self.base_url, e.get('href'))

        # Strip off URL queries
        if link.find('?') >= 0:
          parts = list(urlparse(link))
          parts[4] = '' 
          link = urlunparse(parts)

        suffix = link[-4:]
        if suffix in ['.pdf', '.zip', '.eps', '.jpg', '.png', '.gif', '.svg']:
          self.assets.add(link)
        else:
          self.links.add(link)

      # Parse <link> tags for assets
      for e in self.root.iter('link'):
        link = urljoin(self.base_url, e.get('href'))
        self.assets.add(link)

      # Parse <script> tags for assets
      for e in self.root.iter('script'):
        src = e.get('src')
        if src:
          link = urljoin(self.base_url, e.get('src'))
          self.assets.add(link)

      # Parse <img> tags for assets
      for e in self.root.iter('img'):
        link = urljoin(self.base_url, e.get('src'))
        self.assets.add(link)

  def isEmpty(self):
    """
    Returns true if this instance failed to retrieve web content during 
    construction.
    """
    return self.root == None

  def getLinks(self):
    return list(self.links)

  def getAssets(self):
    return list(self.assets)

  def getDomain(self):
    return self.base_url

  def sameDomain(self, url_string):
    """
    Return whether the given url string is in this ParseHtml instance's domain.
    """
    up = urlparse(url_string)
    return self.getDomain() == up.scheme + '://' + up.netloc

"""
  Helper Functions
"""

def getHtml(url_string):
  """
  Make an HTTP request to the given url string and return the HTML string.
  """
  r = requests.get(url_string)

  if r.status_code != 200:
    return None 

  return unicode(r.content, 'UTF-8')

def domain(url_string):
  if not url_string:
    return ''
  up = urlparse(url_string)
  return up.scheme + '://' + up.netloc
