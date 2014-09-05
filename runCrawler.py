"""
  TODO
"""

# Library Imports
import threading
import Queue
from datetime import datetime

# Local Module Imports
from crawlthread import CrawlThread
from outputthread import OutputThread
from parseHtml import domain

def main():
  print 'Crawling Beginning.'
  start_time = datetime.now()

  crawlqueue = Queue.Queue()
  outqueue   = Queue.Queue()
  lock       = threading.Lock()
  crawled    = set()

  start_url = 'http://www.hiddenjunk.net'
  d = domain(start_url)

  # Start Crawler threads
  NUM_WORKERS = 5
  for i in range(NUM_WORKERS):
    t = CrawlThread(d, crawlqueue, outqueue, lock, crawled)
    t.setDaemon(True)
    t.start()

  # Start sitemap output thread
  t = OutputThread(outqueue)
  t.setDaemon(True)
  t.start()

  crawlqueue.put(start_url)

  # TODO: How to terminate. Wait for a while then join the threads and queues?
  crawlqueue.join()
  outqueue.join()
  print 'Crawling Finished. Time Elapsed: ', datetime.now() - start_time

if __name__ == '__main__':
  main()
