import feedparser

def parseFeed():
    url = 'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml'
    parsedFeed = feedparser.parse(url)
    numArticles = 5
    articlesList = [{}]*numArticles

    for i in range(numArticles):
        entry = parsedFeed['entries'][i]
        authors = entry['author']
        title = entry['title']
        description = entry['description']
        dict = {'description': description, 'authors':authors, 'title':title}
        articlesList[i] = dict
    return articlesList
