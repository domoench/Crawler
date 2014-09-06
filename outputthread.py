"""
  A thread to handle outputing crawled page data to the sitemap output file.
"""

# Library Imports
import threading
import Queue

class OutputThread(threading.Thread):

  def __init__(self, outqueue, w):
    """
    Args:
      outqueue: A Queue of crawled page data jobs ready for output
      w: A File object to write output to
    """
    self.outqueue = outqueue
    self.w = w 
    threading.Thread.__init__(self)

  def run(self):
    while True:
      page_data = self.outqueue.get()
      self.writeData(page_data)
      self.outqueue.task_done()

  def writeData(self, page_data):
    """
    Output the links and static assets associated with a single crawled page. 

    Args:
      page_data: A tuple of info about a crawled page: (url, links, assets)
    """
    url    = page_data[0]
    links  = page_data[1]
    assets = page_data[2]

    w = self.w
    w.write(url + '\n')

    w.write('LINKS:\n')
    for link in links:
      w.write('  ' + link + '\n')

    w.write('ASSETS:\n')
    for asset in assets:
      w.write('  ' + asset + '\n')

    w.write('\n')
