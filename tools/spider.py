# -*- coding: utf-8 -*-

from subprocess import (
    Popen,
    PIPE
)
from bs4 import (
    BeautifulSoup,
    element
)
import glob
import urllib
import time
import copy


class Crawler(object):
    '''
    generate urls for fetcher to request
    '''
    def __init__(self):
        self.keyword_gen = self._load_keywords()
        self.search_site = 'http://s.taobao.com/search?'

    def _load_keywords(self):
        pattern = '../keywords/*.txt'
        for file_name in glob.glob(pattern):
            with open(file_name) as f:
                for line in f:
                    yield line

    def next(self):
        keyword = self.keyword_gen.next()
        payload = {u'q': keyword.decode('utf8').encode('utf8')}
        url = self.search_site + urllib.urlencode(payload)
        return url

    def __iter__(self):
        return self


class Fetcher(object):
    '''
    get html block of 「掌柜热卖」
    '''
    def __init__(self, url):
        self.url = url
        self._fetch_html()

    def _fetch_html(self):
        p = Popen(['phantomjs', '../js/waitfor.js', self.url], stdout=PIPE)
        self.html = p.communicate()[0]

    def get_html(self):
        return self.html


class Indexer(object):
    '''
    filter title and image url from html block
    get by Fetcher
    '''
    def __init__(self, html):
        self.soup = BeautifulSoup(html)
        self.adlist = []
        self._filter_html()

    def _filter_html(self):
        addict = {}
        [s.extract() for s in self.soup('script')]
        adtags = self.soup.find_all('div', class_='item')
        for tag in adtags:
            for link in tag.contents[0].find_all('img'):
                addict['pic_url'] = link.get('src')
            str_list = self._get_str(tag).split('||')
            addict['title'] = str_list[0]
            self.adlist.append(copy.deepcopy(addict))


    def _get_str(self, tags, level=0):
        if type(tags) == element.NavigableString:
            return tags

        content_str = ''
        for itag in tags.contents:
            mystr = self._get_str(itag, level+1)
            content_str += mystr
            if level == 1 and mystr != '' and mystr != '\n':
                content_str += '||'
        return content_str

    def get_ad_list(self):
        return self.adlist


if __name__ == '__main__':
    c = Crawler()
    for url in c:
        html = Fetcher(url).get_html()
        print Indexer(html).get_ad_list()
