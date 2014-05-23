import sys
sys.path.append('..')
from subprocess import (
    Popen,
    PIPE
)
from tools.spider import Crawler

c = Crawler()
for url in c:
    print url
    p = Popen(['phantomjs', '../js/waitfor.js', url], stdout=PIPE)
    print p.communicate()[0]
