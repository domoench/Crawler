from unittest import main, TestCase

from parseHtml import ParseHtml, getHtml

class TestParseHtml(TestCase):

  def setUp(self):
    self.base_url = 'http://davidmoench.com'
    self.p = ParseHtml(self.base_url) #TODO: Test a locally hosted test site

  def test_getHtml(self):
    # TODO: Is this testable - or is it just testing the requests library and network connection?
    assert False

  def test_ParseHtml(self):
    self.assertEqual(self.p.root.tag, 'html')
    self.assertEqual(5, len(list(self.p.root.iter('a'))))
    self.assertEqual(1, len(list(self.p.root.iter('head'))))
    self.assertEqual(1, len(list(self.p.root.iter('body'))))

  def test_getLinks(self):
    l = ['http://davidmoench.com/projects.php', 'https://github.com/domoench', 
         'http://www.linkedin.com/pub/david-ouyang-moench/5a/3a7/288', 
         'http://davidmoench.com/music.php']
    self.assertEqual(self.p.getLinks(), l)

  def test_sameDomain(self):
    self.assertTrue(self.p.sameDomain('http://davidmoench.com'))
    self.assertTrue(self.p.sameDomain('http://davidmoench.com/music.php'))
    self.assertTrue(self.p.sameDomain('http://davidmoench.com/projects.php'))

    self.assertFalse(self.p.sameDomain('https://google.com'))
    self.assertFalse(self.p.sameDomain('https://github.com/domoench'))

main()
