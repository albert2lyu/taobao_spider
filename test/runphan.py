from subprocess import (
    Popen,
    PIPE
)

url = 'http://s.taobao.com/search?q=%D7%E3%C7%F2'
p = Popen(['phantomjs', '../js/waitfor.js', url], stdout=PIPE)
print p.communicate()[0]
