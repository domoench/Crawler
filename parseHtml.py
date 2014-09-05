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

    #print 'constructing ParseHtml(%s)' % (url_string)

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
        #print 'Unsanitized Child-link: %s' % (e.get('href'))
        link = urljoin(self.base_url, e.get('href'))
        #print 'Sanitized Child-link: %s' % (link)

        # Strip off URL queries and fragments
        parts = list(urlparse(link, allow_fragments=False))
        parts[4] = '' 
        link = urlunparse(parts)
        #print 'Stripped Child-link: %s' % (link)

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
    return list(self.links) #TODO: Why convert to a list?

  def getAssets(self):
    return list(self.assets) #TODO: Why convert to a list?

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

  TODO: Try/catch exceptions shown at https://stackoverflow.com/questions/25146901/python-requests-with-multithreading
        When catching exceptions, handle by outputting error to console and returning none?
  """
  print 'getHtml(%s)' % url_string
  r = requests.get(url_string)

  if r.status_code != 200:
    print 'getHtml(%s) failed. Status code = %s' % (url_string, r.status_code)
    return None 

  return unicode(r.content, 'UTF-8')

def domain(url_string):
  if not url_string:
    return ''
  up = urlparse(url_string)
  return up.scheme + '://' + up.netloc
