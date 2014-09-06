"""
  A thread to handle outputing crawled page data to the sitemap output file.
"""

# Library Imports
import threading
import Queue
import codecs

class OutputThread(threading.Thread):

  def __init__(self, outqueue):
    self.outqueue = outqueue
    self.outfile  = codecs.open('sitemap.txt', 'w', encoding='utf-8')
    threading.Thread.__init__(self)

  def __del__(self):
    self.outfile.close()
    threading.Thread.__del__(self)

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

    f = self.outfile
    f.write(url + '\n')

    f.write('LINKS:\n')
    for link in links:
      f.write('  ' + link + '\n')

    f.write('ASSETS:\n')
    for asset in assets:
      f.write('  ' + asset + '\n')

    self.outfile.write('\n')
