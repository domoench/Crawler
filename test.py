from unittest import main, TestCase

from parseHtml import ParseHtml, getHtml

class TestParseHtml(TestCase):

  def setUp(self):
    self.p = ParseHtml('http://davidmoench.com')

  def test_getHtml(self):
    # TODO: Is this testable - or is it just testing the requests library and network connection?
    assert False

  def test_ParseHtml(self):
    self.assertEqual(self.p.root.tag, 'html')
    self.assertEqual(5, len(list(self.p.root.iter('a'))))
    self.assertEqual(1, len(list(self.p.root.iter('head'))))
    self.assertEqual(1, len(list(self.p.root.iter('body'))))

  def test_getLinks(self):
    l = ['projects.php', 'https://github.com/domoench', 'resume.pdf', 
         'http://www.linkedin.com/pub/david-ouyang-moench/5a/3a7/288', 
         'music.php']
    self.assertEqual(self.p.getLinks(), l)

main()
