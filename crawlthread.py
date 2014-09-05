"""
TODO
"""
# Library Imports
import threading
import Queue

# Local Module Imports
from parseHtml import ParseHtml, domain

class CrawlThread(threading.Thread):

  def __init__(self, domain, crawlqueue, outqueue, lock, crawled):
    """
    Args:
      domain: The domain to which we are confining our crawling
      crawlqueue: Queue of URLs to be parsed for links and assets
      outqueue: Queue of parsed data ready for output to sitemap text file
      lock: Lock ensuring mutual exclusion of crawled
      crawled: A set of URLs that have already been crawled
    """
    self.domain     = domain
    self.crawlqueue = crawlqueue
    self.outqueue   = outqueue
    self.lock       = lock
    self.crawled    = crawled

    threading.Thread.__init__(self)

  def run(self):
    """
    Crawl!
    """
    while True:
      url = self.crawlqueue.get()
      #print 'Removed %s from the crawlqueue' % url
      page_data = self.processPage(url)
      if not page_data:
        self.crawlqueue.task_done()
        continue

      # This page's data is ready for printing
      #print 'Adding %s to outqueue' % url
      self.outqueue.put(page_data)
  
      # Schedule this page's children for crawling 
      self.lock.acquire()
      #print 'Aquired lock to recurse on %s' % url
      for link in page_data[1]:
        if (link not in self.crawled) and (domain(link) == self.domain):
          #print 'Adding %s to crawlqueue' % link
          self.crawlqueue.put(link)
          self.crawled.add(link)
      self.lock.release()

      self.crawlqueue.task_done()

  def processPage(self, url):
    """
    Return the links and assets found at this url.
    
    Args:
      url: The url to recursively crawl 
    Return:
      A tuple of the form (url, list of link strings, list of asset path strings)
      None if there was an issue processing this page
    """
    #print 'crawlthread.processPage(%s)' % (url)
    assert(domain(url) == self.domain)
    p = ParseHtml(url)
    if p.isEmpty():
      return None

    links = p.getLinks()
    assets = p.getAssets()
    return (url, links, assets)
