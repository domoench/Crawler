"""
  Main driver. 
"""

# Library Imports
import argparse
import threading
import codecs
import Queue
from datetime import datetime

# Local Module Imports
from crawlthread import CrawlThread
from outputthread import OutputThread
from parsehtml import domain

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
  d = domain(start_url)

  crawlqueue = Queue.Queue()
  outqueue   = Queue.Queue()
  lock       = threading.Lock()
  crawled    = set()

  # Start Crawler threads
  print 'Spawning %d crawler threads.' % num_crawlers
  for i in range(num_crawlers):
    t = CrawlThread(d, crawlqueue, outqueue, lock, crawled)
    t.setDaemon(True)
    t.start()

  # Start sitemap output thread
  f = codecs.open('sitemap.txt', 'w', encoding='utf-8')
  t = OutputThread(outqueue, f)
  t.setDaemon(True)
  t.start()

  # Kick off the crawling
  crawlqueue.put(start_url)

  # Wait for completion
  crawlqueue.join()
  outqueue.join()
  f.close()

  dt = datetime.now() - start_time
  print 'Crawling finished. Time elapsed: ', dt 

if __name__ == '__main__':
  main()
