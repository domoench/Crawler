# A multi-thread web crawler

## Required Python Dependencies:
* lxml

## To Run:
```
python runCrawler.py -url https://website.com -t 60
```

### Command Line Options:
* -url: Specify the page url to crawl from. It must include the schema.
* -t: Specify the number of crawler threads to run. On my machine, [about 30 to works well](https://cloud.githubusercontent.com/assets/2548712/4173987/45b0de30-3571-11e4-8ff6-42bc8c1445c0.jpg).
