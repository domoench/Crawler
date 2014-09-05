"""
  A class for parsing and querying an HTML page.
"""

# Library Imports
import requests
from urlparse import urlparse, urljoin, urlunparse
from lxml import etree
from io import StringIO, BytesIO
import codecs

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
      try:
        html_bytes = codecs.encode(html_string, 'utf-8', 'xmlcharrefreplace')
        self.root  = etree.HTML(html_bytes)
      except Exception as e:
        print 'ERROR: ', e
      self.base_url = domain(url_string) 

      # Parse <a> tags for links and assets
      for e in self.root.iter('a'):
      #for e in self.root.xpath('//a'):
        #print 'Unsanitized Child-link: %s' % (e.get('href'))
        link = urljoin(url_string, e.get('href'))
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
      #for e in self.root.xpath('//link'):
        link = urljoin(url_string, e.get('href'))
        self.assets.add(link)

      # Parse <script> tags for assets
      for e in self.root.iter('script'):
      #for e in self.root.xpath('//script'):
        src = e.get('src')
        if src:
          link = urljoin(url_string, e.get('src'))
          self.assets.add(link)

      # Parse <img> tags for assets
      for e in self.root.iter('img'):
      #for e in self.root.xpath('img'):
        link = urljoin(url_string, e.get('src'))
        self.assets.add(link)

  def isEmpty(self):
    """
    Returns true if this instance failed to retrieve web content during 
    construction.
    """
    return self.root == None

  def getLinks(self):
    return self.links

  def getAssets(self):
    return self.assets

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
  try:
    resp = requests.get(url_string)
    if resp.status_code != 200:
      print 'getHtml(%s) failed. Status code = %s' % (url_string,resp.status_code)
      result = None
    else:
      result = resp.text
      assert type(result) is unicode

  except Exception as e:
    print 'EXCEPTION: ', e 
    return None

  return result

def domain(url_string):
  if not url_string:
    return ''
  up = urlparse(url_string)
  return up.scheme + '://' + up.netloc
