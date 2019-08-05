import requests
import pymysql
import re
import os

# 盗链地址
referer = 'https://s.taobao.com/search?q=%E9%BC%A0%E6%A0%87'
# firefox用户代理
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'


def getHtmlText(url,user_agent='Mozilla/5.0',Referer=None,proxies=None,params={},num_retries=0,timeout=10):
    """
    使用requests库获取网页内容
    :param url:         url地址
    :param user_agent:  用户代理
    :param Referer:     反盗链地址
    :param proxies:     代理服务器地址
    :param params:      参数
    :return:            网页内容
    """
    try:
        if Referer == None:
            Referer = url
        print("Downloading:"+url)
        # 淘宝搜索页面需要先登录，所以加了一个Cookie字段
        headers = {'User-Agent':user_agent,'Referer':Referer,
                   'Cookie':'cookie2=1c1f2e14138aa14fd0c4308bc1f77b88; t=3ffe11eebafd1e7eafcecf84b0d721a9; _tb_token_=ee736f318ed76; cna=NUCPFW5djwkCAd9oGehy2vId; v=0; isg=BHR0o7hxleEKOwGtw3exGgUXRjLsVElRdDb1uA7VAP-CeRTDNl1oxyo7-XEEmtCP; l=cBErX9sRqUlysLvBBOCahurza77OSIOYYuPzaNbMi_5wr6T1VCQOk7RyEF96VsWdO_8B4KXJ7Lp9-etkZDrRit--g3fP.; unb=2266114269; uc1="cookie15=URm48syIIVrSKA%3D%3D"; uc3=nk2=CtU9xOTis%2BsK8A%3D%3D&lg2=W5iHLLyFOGW7aA%3D%3D&vt3=F8dBy32i56dGy6eBpZU%3D&id2=UUpnjmMcN6Dp%2FQ%3D%3D; csg=a125de90; lgc=istangning; cookie17=UUpnjmMcN6Dp%2FQ%3D%3D; dnk=istangning; skt=7e0a05b3d981ccb1; existShop=MTU2NDkwMDgwNw%3D%3D; uc4=id4=0%40U2gtHyNhFLefR5JTPQglJOJz26x4&nk4=0%40CNTOvrcaht6QpbtNkXXn94wMtuzO; tracknick=istangning; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=g98; _nk_=istangning; cookie1=BYiMeV%2BKfCZGLPFaoiH4LtMrWxkHqqmNponN9Xcyxn4%3D; enc=kM428N5egK7pikGQAYzwnx0%2BX7X1R6K7q38maNlQXhEcIw0VZW6n%2Fmkst0MBGrXhm%2FjovQDWTCDt%2FXBaDOJCJQ%3D%3D; thw=cn; mt=ci=6_1; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0'
                   }
        r = requests.get(url,headers=headers,proxies=proxies,timeout=timeout,params=params)
        # 下载出错就跳到except
        r.raise_for_status()
        # 设置编码为预判编码apparent_encoding或utf-8
        r.encoding = r.apparent_encoding
        return r.text

    except:
        if num_retries == 0:
            print("Downloading Error:"+url)
            return "产生异常"
        else:
            getHtmlText(url=url,user_agent=user_agent,proxies=proxies,params=params,num_retries=num_retries-1,timeout=timeout)


def downloadImage(url,root,user_agent='Mozilla/5.0',Referer=None):
    """
    使用requests库获取图片
    :param url:         图片地址
    :param root:        保存位置
    :param user_agent:  用户代理
    :param Referer:     反盗链地址
    :return:
    """
    try:
        path = root + re.search(r'(/.+\.(jpg|png|gif|bmp|JPG|PNG|GIF|BMP))', url).group(1).split('/')[-1]
        # 如果目录不存在，则先创建目录
        if not os.path.exists(root):
            os.mkdir(root)
        # 如果文件已存在，则跳过
        if not os.path.exists(path):
            if Referer == None:
                Referer = url
            headers = {'User-Agent': user_agent, 'Referer': Referer,
                       'Cookie': 'cna=NUCPFW5djwkCAd9oGehy2vId; sca=b4355d16; tbsa=bf11270a1183a31b61ee3a72_1564904730_23; atpsida=9e0f88fef5e0af95ff0a9cf1_1564904730_24; atpsidas=5d3d709976404de2fb9a677f_1564904730_28; cad=d5GlrwYY8jfFZYu22xX2M4sRj9qIdlQaTz9dWfvXhOs=0001; cap=c032; cnaui=2266114269; aui=2266114269; cdpid=UUpnjmMcN6Dp%252FQ%253D%253D; cmida=1401053355_20190804154530'
                       }
            r = requests.get(url, headers=headers)
            with open(path,'wb') as f:
                f.write(r.content)
                f.close()
        else:
            print(path+"已存在")
    except:
        print("爬取失败")


def parsePage(ilt, html):
    """
    利用正则表达式解析网页内容存入list
    :param ilt:     保存内容的list
    :param html:    下载的网页内容
    :return:
    """
    try:
        # 由于是js动态生成，所有使用正则表达式获取
        plt = re.findall(r'\"view_price\"\:\"([\d\.]*)\"',html)
        tlt = re.findall(r'\"raw_title\"\:\"(.*?)\"',html)
        picUrl = re.findall(r'\"pic_url\"\:\"(.*?)\"',html)
        payNum = re.findall(r'\"view_sales\"\:\"([\d\.]+)(.*?)\"',html)
        for i in range(len(plt)):
            num = float(payNum[i][0])
            if re.search(r'万',payNum[i][1]):
                num *= 10000
            ilt.append([plt[i], tlt[i], 'http:'+picUrl[i], int(num)])

    except:
        print("")


def persistenceGoodsList(ilt):
    """
    持久化爬取的数据
    :param ilt: 保存的list
    :return:
    """
    tplt = "{:4}\t{:8}\t{:10}\t{:100}\t{}"
    print(tplt.format("序号","价格","付款人数","图片地址","商品名称"))
    count = 0
    # mysql数据库连接
    db = pymysql.connect("localhost", "root", "tangning", "jdbc")
    sql = "insert into t_taobao_product(name,price,payNum,picUrl) values(%s,%s,%s,%s)"
    # 获取游标
    cursor = db.cursor()
    for i in ilt:
        count += 1
        try:
            # 下载图片
            downloadImage(i[2],user_agent=user_agent,Referer=referer,root='Image/')
            cursor.execute(sql, (i[1],i[0],i[3],i[2]))
        except:
            print("存入数据库失败："+i[1])
            continue
        print(tplt.format(count,i[0],i[3],i[2],i[1]))
    db.commit()
    db.close()


def main():
    # 淘宝搜索关键字
    goods = '笔记本电脑'
    # 爬取深度
    depth = 10
    start_url = 'https://s.taobao.com/search?q=' + goods
    infoList = []
    for i in range(depth):
        try:
            # 乘44是查看网页确定
            url = start_url + '&s=' + str(44 * i)
            html = getHtmlText(url,user_agent=user_agent,Referer=referer)
            parsePage(infoList, html)
        except:
            continue
    persistenceGoodsList(infoList)

main()