"""
  A worker thread class. Each thread continually processes URLs from the 
  crawlqueue and adds the results to the outqueue.
"""

# Library Imports
import threading
import Queue

# Local Module Imports
from parsehtml import ParseHtml, domain

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
    Process jobs on the crawlqueue.
    """
    while True:
      url = self.crawlqueue.get()
      page_data = self.processPage(url)

      # If getting this page's data from the network fails, move on
      if not page_data:
        self.crawlqueue.task_done()
        continue

      # This page's data is ready for printing
      self.outqueue.put(page_data)
  
      # Schedule this page's children for crawling. Only one thread can access
      # the crawled set at a time.
      self.lock.acquire()
      for link in page_data[1]:
        if (link not in self.crawled) and (domain(link) == self.domain):
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
    assert(domain(url) == self.domain)
    p = ParseHtml(url)
    if p.isEmpty():
      return None

    links = p.getLinks()
    assets = p.getAssets()
    return (url, links, assets)
