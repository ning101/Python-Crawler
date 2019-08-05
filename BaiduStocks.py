from bs4 import BeautifulSoup
import re
import requests
import traceback


def getHtmlText(url,user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
                Referer=None,proxies=None,params={},num_retries=0,timeout=10):
    """
    使用requests库获取网页内容
    :param url:         url地址
    :param user_agent:  用户代理
    :param Referer:     反盗链地址
    :param proxies:     代理服务器地址
    :param params:      参数
    :param num_retries: 重试次数
    :param timeout:     超时时间
    :return:            网页内容
    """
    try:
        if Referer == None:
            Referer = url
        print("Downloading:"+url)
        # 淘宝搜索页面需要先登录，所以加了一个Cookie字段
        headers = {'User-Agent':user_agent,'Referer':Referer}
        r = requests.get(url,headers=headers,proxies=proxies,timeout=timeout,params=params)
        # 下载出错就跳到except
        r.raise_for_status()
        # 设置编码为预判编码apparent_encoding或utf-8
        r.encoding = r.apparent_encoding
        return r.text

    except:
        if num_retries == 0:
            print("Downloading Error:"+url)
            return ""
        else:
            #重试
            getHtmlText(url=url,user_agent=user_agent,proxies=proxies,params=params,num_retries=num_retries-1,timeout=timeout)

def getStockList(lst, stockUrl, deep):
    # 百度股票的搜索接口
    search = 'https://gupiao.baidu.com/api/search/stockquery?from=pc&os_ver=1&cuid=xxx&vv=3.2&format=json&query_content={}&asset=0%2C4%2C14&timestamp=1564918806854'
    for i in range(deep):
        text = getHtmlText(stockUrl.format(i+1))
        f12 = re.findall(r'\"f12\"\:\"([0-9]{6})\"',text)
        f14 = re.findall(r'\"f14\"\:\"(.+?)\"',text)
        for j in range(len(f12)):
            # 根据代码查询百度股票的资源代码
            result = getHtmlText(search.format(f12[j]))
            tag = re.search(r'\"f_code\"\:\"(.+?)\"',result)
            if tag:
                lst.append(tag.group(1))


def getStockInfo(lst, stockUrl, fpath):
    for stock in lst:
        # 组装百度股票的页面
        url = stockUrl + stock + ".html"
        html = getHtmlText(url)
        try:
            if html == "":
                continue
            infoDict = {}
            soup = BeautifulSoup(html, 'html5lib')
            stockInfo = soup.find('div',attrs={'class':'stock-bets'})

            name = stockInfo.find_all('a',attrs={'class':'bets-name'})[0]
            # 更新字典
            infoDict.update({'股票名称':name.text.split()[0]})

            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            for i in range(len(keyList)):
                # 获取键值存入数组
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val

            with open(fpath,'a',encoding='utf-8') as f:
                # 写入文件
                f.write(str(infoDict) + '\n')
        except:
            traceback.print_exc()
            continue

def main():
    # 东方财富网地址
    stock_list_url = 'http://63.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112407783366118504346_1564916139883&pn={}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2&fields=f12,f14'
    # 百度股票地址
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    # 文件位置
    output_file = 'BaiduStockInfo.txt'
    slist = []
    # 搜索深度（东方财富网页数）
    deep = 10
    getStockList(slist, stock_list_url, deep)
    getStockInfo(slist, stock_info_url, output_file)

main()