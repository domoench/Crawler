from unittest import main, TestCase

from parseHtml import ParseHtml, getHtml, domain

class TestParseHtml(TestCase):

  def setUp(self):
    self.base_url = 'http://davidmoench.com'
    self.p = ParseHtml(self.base_url) #TODO: Test a locally hosted test site

  def test_getHtml(self):
    self.assertEqual(getHtml('http://davidmoench.com/non-existant-page'), None)
    pass 

  def test_domain(self):
    self.assertEqual(domain('https://google.com'), 'https://google.com')
    self.assertEqual(domain('http://davidmoench.com/projects.php'), 'http://davidmoench.com')
    self.assertEqual(domain(''), '')

  def test_constructor_1(self):
    self.assertEqual(self.p.root.tag, 'html')
    self.assertEqual(self.p.base_url, self.base_url)
    self.assertEqual(4, len(self.p.links))
    self.assertEqual(8, len(self.p.assets))
    self.assertEqual(1, len(list(self.p.root.iter('head'))))
    self.assertEqual(1, len(list(self.p.root.iter('body'))))
    self.assertFalse(self.p.isEmpty())

  def test_isEmpty(self):
    p2 = ParseHtml('http://davidmoench.com/non-existant-page')
    self.assertEqual(p2.root, None)
    self.assertEqual(p2.base_url, None)
    self.assertEqual(0, len(p2.links))
    self.assertEqual(0, len(p2.assets))

    self.assertTrue(p2.isEmpty())

  def test_getLinks(self):
    s = set(['http://davidmoench.com/projects.php', 'https://github.com/domoench', 
         'http://www.linkedin.com/pub/david-ouyang-moench/5a/3a7/288', 
         'http://davidmoench.com/music.php'])
    l = self.p.getLinks() 
    for link in l:
      self.assertTrue(link in s)

  def test_getAssets(self):
    s = set(['http://fonts.googleapis.com/css?family=Ubuntu:300,400',
             'https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js',
             'http://davidmoench.com/css/style.css',
             'http://davidmoench.com/identicon.ico',
             'http://davidmoench.com/js/bootstrap.js',
             'http://davidmoench.com/resume.pdf',
             'http://davidmoench.com/fancybox/source/jquery.fancybox.css?v=2.1.4',
             'http://davidmoench.com/fancybox/source/jquery.fancybox.pack.js?v=2.1.4'])
    a = self.p.getAssets() 
    for asset in a:
      self.assertTrue(asset in s)

  def test_sameDomain(self):
    self.assertTrue(self.p.sameDomain('http://davidmoench.com'))
    # self.assertTrue(self.p.sameDomain('davidmoench.com')) #TODO: Should this be ok?
    self.assertTrue(self.p.sameDomain('http://davidmoench.com/music.php'))
    self.assertTrue(self.p.sameDomain('http://davidmoench.com/projects.php'))

    self.assertFalse(self.p.sameDomain('http://subdomain.davidmoench.com/projects.php'))
    self.assertFalse(self.p.sameDomain('subdomain.davidmoench.com/projects.php'))

    self.assertFalse(self.p.sameDomain('https://google.com'))
    self.assertFalse(self.p.sameDomain('https://github.com/domoench'))
    self.assertFalse(self.p.sameDomain(''))

main()
