"""
  A class for parsing and querying an HTML page.
"""

# Library Imports
import requests
from urlparse import urlparse, urljoin, urlunparse
from lxml import etree
import codecs

class ParseHtml:

  def __init__(self, url):
    """ 
    If retrieving and parsing data from the given URL fails for any reason, the
    constructor is aborted leaving self.root == None. This can be checked with
    isEmpty().

    A 'link' is a link to a crawlable page.
    An 'asset' is a link to a non-crawlable static asset: images, js, css, etc. 
    """

    self.links  = set() 
    self.assets = set() 
    self.root   = None
    self.domain = None

    # Get the page content from the network 
    html_string = getHtml(url)

    if not html_string:
      return

    else:
      try:
        html_bytes   = codecs.encode(html_string, 'utf-8', 'xmlcharrefreplace')
        self.root    = etree.HTML(html_bytes)
        if self.root == None:
          return 
      except Exception as e:
        print 'Exception: ', e
        self.root = None
        return
      self.domain = domain(url) 

      # Parse <a> tags for links and assets
      for e in self.root.iter('a'):
        link = urljoin(url, e.get('href'))

        # Check if url is valid
        u = urlparse(link, allow_fragments=False)
        if not validURL(link):
          continue

        # Strip URL queries 
        parts = list(u)
        parts[4] = '' 
        link = urlunparse(parts)

        # Determine if this <a> tag points to a parse-able link, or a static asset
        linked_asset_types = ('.pdf', '.zip', '.eps', '.jpg', '.png', '.gif', 
                              '.svg', '.qtl')
        link_type = link[-4:]
        if link_type in linked_asset_types:
          self.assets.add(link)
        else:
          self.links.add(link)

      # Parse <link> tags for assets
      for e in self.root.iter('link'):
        link = urljoin(url, e.get('href'))
        self.assets.add(link)

      # Parse <script> tags for assets
      for e in self.root.iter('script'):
        src = e.get('src')
        if src:
          link = urljoin(url, e.get('src'))
          self.assets.add(link)

      # Parse <img> tags for assets
      for e in self.root.iter('img'):
        link = urljoin(url, e.get('src'))
        self.assets.add(link)

  def isEmpty(self):
    """
    Returns True if this instance failed to retrieve web content during 
    construction.
    """
    return self.root == None

  def getLinks(self):
    return self.links

  def getAssets(self):
    return self.assets

  def getDomain(self):
    return self.domain

  def sameDomain(self, url):
    """
    Return whether the given url string is in this ParseHtml instance's domain.
    """
    up = urlparse(url)
    return self.getDomain() == up.scheme + '://' + up.netloc

"""
  Helper Functions
"""

def getHtml(url):
  """
  Make an HTTP request to the given url string and return the HTML string.
  """
  try:
    resp = requests.get(url)
    if resp.status_code != 200:
      result = None
    else:
      result = resp.text
      assert type(result) is unicode

  except Exception as e:
    print 'Exception: ', e 
    return None

  return result

def domain(url):
  if not url:
    return ''
  up = urlparse(url)
  return up.scheme + '://' + up.netloc

def validURL(url):
  u = urlparse(url, allow_fragments=False)
  return (u.scheme != '' and u.netloc != '')
