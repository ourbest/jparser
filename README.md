# eparser
A readability parser which can extract title,time,author, content, images from html pages

Install:

    pip install eparser
    （requirement: lxml）

Usage Example:

    import urllib2
    from eparser import PageModel
    html = urllib2.urlopen("http://news.sohu.com/20170512/n492734045.shtml").read().decode('gb18030')
    pm = PageModel(html)
    result = pm.extract()
    
    print "==title=="
    print result['title']
    print "==author=="
    print result['author']
    print "==time=="
    print result['time']
    print "==content=="
    for x in result['content']:
        if x['type'] == 'text':
            print x['data']
        if x['type'] == 'image':
            print "[IMAGE]", x['data']['src']
    
# Demo:

# http://jparser.duapp.com/
