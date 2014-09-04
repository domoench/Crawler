"""
TODO
"""
from parseHtml import ParseHtml, domain

class Crawler:

  def __init__(self, start_url):
    self.data   = {}
    self.start_url = start_url
    self.domain = domain(start_url)

    self.crawl(start_url)

  def crawl(self, url):
    """
    Recursively crawl the tree of webpages rooted at, and in the same domain as,
    the given url.
    
    Args:
      url: The url to start recursively crawling from
      data: The lookup table storing links/assets of previously visited urls
    """
    assert(domain(url) == self.domain)
    if (url not in self.data):
      print 'Crawling ' + url
      p = ParseHtml(url)
      if p.isEmpty():
        return

      links = p.getLinks()
      assets = p.getAssets()
      self.data[url] = (links, assets)

      for link in links:
        if domain(link) == self.domain:
          self.crawl(link)

  def outputSitemap(self):
    """
    TODO
    """
    with open('sitemap.txt', 'w') as outfile:
      for (page_url, resources) in self.data.items():
        outfile.write(page_url + '\n')

        outfile.write('LINKS:\n')
        for link in resources[0]:
          outfile.write('  ' + link + '\n')

        outfile.write('ASSETS:\n')
        for asset in resources[1]:
          outfile.write('  ' + asset + '\n')

        outfile.write('\n')
        """
        print page_url

        print 'LINKS:'
        for link in resources[0]:
          print '  ' + link

        print 'ASSETS:'
        for asset in resources[1]:
          print '  ' + asset

        print '';
        """
