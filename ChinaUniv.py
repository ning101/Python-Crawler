from test import getHtmlText
from bs4 import BeautifulSoup
import bs4


def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, 'html5lib')
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            ulist.append([tds[0].string, tds[1].string, tds[2].string])

def printUnivList(ulist, num):
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}"
    print(tplt.format("排名","学校名称","总分",chr(12288)))
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0],u[1],u[2],chr(12288)))

def main():
    uinfo = []
    url = "http://www.zuihaodaxue.com/zuihaodaxuepaiming2019.html"
    html = getHtmlText(url)
    fillUnivList(uinfo, html)
    printUnivList(uinfo, len(uinfo))

main()