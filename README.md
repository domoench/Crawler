A multi-thread web crawler. Developed for compatibility with Python 2.7.8.

### Required Python Dependencies (that need explicit installation):
* lxml

### To Run:
```
python runCrawler.py -url https://website.com -t 30
```

Command Line Options:
* -url: Specify the page url to crawl from. It must include the schema.
* -t: Specify the number of crawler threads to run. On my machine, [about 30 works well](https://cloud.githubusercontent.com/assets/2548712/4173987/45b0de30-3571-11e4-8ff6-42bc8c1445c0.jpg).

### To Test:
```
python test.py
```
