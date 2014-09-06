from unittest import main, TestCase
import threading
import Queue

from parseHtml import ParseHtml, getHtml, domain, validURL
from crawlthread import CrawlThread

class TestParseHtml(TestCase):

  def setUp(self):
    self.domain = 'http://davidmoench.com'
    self.p = ParseHtml(self.domain) #TODO: Test a locally hosted test site

  def test_getHtml(self):
    self.assertEqual(getHtml('http://davidmoench.com/non-existant-page'), None)

  def test_constructor(self):
    self.assertEqual(self.p.root.tag, 'html')
    self.assertEqual(self.p.domain, self.domain)
    self.assertEqual(4, len(self.p.links))
    self.assertEqual(8, len(self.p.assets))
    self.assertEqual(1, len(list(self.p.root.iter('head'))))
    self.assertEqual(1, len(list(self.p.root.iter('body'))))
    self.assertFalse(self.p.isEmpty())

  def test_isEmpty(self):
    p2 = ParseHtml('http://davidmoench.com/non-existant-page')
    self.assertEqual(p2.root, None)
    self.assertEqual(p2.domain, None)
    self.assertEqual(0, len(p2.links))
    self.assertEqual(0, len(p2.assets))

    self.assertTrue(p2.isEmpty())

  def test_getLinks(self):
    e = set(['http://davidmoench.com/projects.php', 
          'https://github.com/domoench', 
          'http://www.linkedin.com/pub/david-ouyang-moench/5a/3a7/288', 
          'http://davidmoench.com/music.php'])
    a = self.p.getLinks() 
    self.assertEqual(e, a)

  def test_getAssets(self):
    e = set(['http://fonts.googleapis.com/css?family=Ubuntu:300,400',
      'https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js',
      'http://davidmoench.com/css/style.css',
      'http://davidmoench.com/identicon.ico',
      'http://davidmoench.com/js/bootstrap.js',
      'http://davidmoench.com/resume.pdf',
      'http://davidmoench.com/fancybox/source/jquery.fancybox.css?v=2.1.4',
      'http://davidmoench.com/fancybox/source/jquery.fancybox.pack.js?v=2.1.4'])
    a = self.p.getAssets() 
    self.assertEqual(e, a)

  def test_getDomain(self):
    self.assertEqual(self.p.getDomain(), 'http://davidmoench.com')

  def test_sameDomain(self):
    self.assertTrue(self.p.sameDomain('http://davidmoench.com'))
    self.assertTrue(self.p.sameDomain('http://davidmoench.com/music.php'))
    self.assertTrue(self.p.sameDomain('http://davidmoench.com/projects.php'))

    self.assertFalse(self.p.sameDomain('http://subdomain.davidmoench.com/projects.php'))
    self.assertFalse(self.p.sameDomain('subdomain.davidmoench.com/projects.php'))

    self.assertFalse(self.p.sameDomain('https://google.com'))
    self.assertFalse(self.p.sameDomain('https://github.com/domoench'))
    self.assertFalse(self.p.sameDomain(''))

  def test_domain(self):
    self.assertEqual(domain('https://google.com'), 'https://google.com')
    self.assertEqual(domain('http://davidmoench.com/projects.php'), 'http://davidmoench.com')
    self.assertEqual(domain('http://sub.davidmoench.com'), 'http://sub.davidmoench.com')
    self.assertNotEqual(domain('http://sub.davidmoench.com'), domain('http://davidmoench.com'))
    self.assertEqual(domain(''), '')

  def test_validURL(self):
    self.assertTrue(validURL('https://google.com'))
    self.assertTrue(validURL('https://google.com'))
    self.assertTrue(validURL('https://www.googleadservices.com/pagead/conversion/1010666955/?value=0&label=g5d3CM2C9QIQy5v24QM&guid=ON&script=0'))
    self.assertFalse(validURL(''))
    self.assertFalse(validURL('javascript:void(0);'))
    self.assertFalse(validURL('http:/google.com'))

class TestCrawlThread(TestCase):

  def setUp(self):
    self.domain = 'http://davidmoench.com'

  def test_processPage(self):
    crawlqueue = Queue.Queue()
    outqueue   = Queue.Queue()
    lock       = threading.Lock()
    crawled    = set()
    c = CrawlThread(self.domain, crawlqueue, outqueue, lock, crawled)
    result = c.processPage('http://davidmoench.com')
    url    = result[0]
    links  = result[1]
    assets = result[2]

    self.assertEqual(url, self.domain)

    l = set(['http://davidmoench.com/projects.php', 
          'https://github.com/domoench', 
          'http://www.linkedin.com/pub/david-ouyang-moench/5a/3a7/288', 
          'http://davidmoench.com/music.php'])
    self.assertEqual(links, l)

    a = set(['http://fonts.googleapis.com/css?family=Ubuntu:300,400',
      'https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js',
      'http://davidmoench.com/css/style.css',
      'http://davidmoench.com/identicon.ico',
      'http://davidmoench.com/js/bootstrap.js',
      'http://davidmoench.com/resume.pdf',
      'http://davidmoench.com/fancybox/source/jquery.fancybox.css?v=2.1.4',
      'http://davidmoench.com/fancybox/source/jquery.fancybox.pack.js?v=2.1.4'])
    self.assertEqual(assets, a)

main()
