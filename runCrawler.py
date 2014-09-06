"""
  Main driver. 
"""

# Library Imports
import argparse
import threading
import Queue
from datetime import datetime

# Local Module Imports
from crawlthread import CrawlThread
from outputthread import OutputThread
from parseHtml import domain

def main():
  # Parse command line args
  parser = argparse.ArgumentParser(prog='crawler',
             description='A web crawler to generate a sitemap of all pages ' +
                         'and their resources')
  parser.add_argument('-url', help='URL to crawl from', required=True)
  parser.add_argument('-t', help='Number of crawler threads', type=int, 
                      default=15)
  args = parser.parse_args()
  start_url    = args.url
  num_crawlers = args.t

  print 'Crawling Beginning.'
  start_time = datetime.now()

  crawlqueue = Queue.Queue()
  outqueue   = Queue.Queue()
  lock       = threading.Lock()
  crawled    = set()

  d = domain(start_url)

  # Start Crawler threads
  print 'Spawning %d crawler threads.' % num_crawlers
  for i in range(num_crawlers):
    t = CrawlThread(d, crawlqueue, outqueue, lock, crawled)
    t.setDaemon(True)
    t.start()

  # Start sitemap output thread
  t = OutputThread(outqueue)
  t.setDaemon(True)
  t.start()

  crawlqueue.put(start_url)

  crawlqueue.join()
  outqueue.join()

  dt = datetime.now() - start_time
  print 'Crawling finished. Time elapsed: ', dt 
  #ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
  #print str(num_crawlers) + ' ' + str(ms)

if __name__ == '__main__':
  main()
