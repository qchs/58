from bs4 import BeautifulSoup
import requests,time,re,pymongo


def GetSoup(url):
    web = requests.get(url)
    soup = BeautifulSoup(web.text,'lxml')
    return soup

def OnePageUrls(url):
    soup = GetSoup(url)
    goods = soup.select('#infolist > table tr[logr*="defaultrank"] > .t > .t')
    # infolist	选择 id="infolist" 的所有元素
    # infolist > table	选择父元素为 <#infolist> 元素的所有 <table> 元素。
    # table tr	选择 <table> 元素内部的所有 <tr> 元素。
    # tr[logr]	选择tr元素中带有 logr 属性所有元素。
    # tr[logr*="defaultrank"]	选择其 logr 属性中包含 "defaulttrank" 子串的每个 <tr> 元素。 商家的logr里面是没有defaulttrank这串字符的
    # .t	选择 class="t" 的所有元素。
    print(len(goods))
    # print(goods)
    urls =[]
    for g in goods:
        title = g.get_text()
        url = g.get('href')
        urls.append(url)
        # print(title,url)
    return urls

def GetView(url):
    id = re.findall('diannao/(.*?)x.shtml',url)[0]
    vurl = 'http://jst1.58.com/counter?infoid=%s'%id
    # print(vurl)
    vsoup = GetSoup(vurl)
    # print(vsoup)
    # total = vsoup.get_text()
    # print(total)
    view = re.findall('Counter58.total=(.*?)</p>',str(vsoup))[0]
    return  view

def Info(url):
    soup = GetSoup(url)
    view = GetView(url)
    cate = soup.select(' .crb_i ')[1].get_text()
    # .crb_i	选择 class="crb_i" 的所有元素。
    title = soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.mainTitle > h1')[0].get_text()
    time = soup.select('#index_show > ul.mtit_con_left.fl > li.time')[0].get_text()
    price = soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(1) > div.su_con > span')[0].get_text()+'元'
    new =list( soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(2) > div.su_con > span')[0].stripped_strings)[0]
    # loca = list(soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(3) > div.su_con  span')[0].stripped_strings)
    isloca = soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(3) > div.su_con  span')
    if isloca:
        location = list(soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(3) > div.su_con  span')[0].stripped_strings)
    else:
        location = 'none'

    data={
        '类目':cate,
        '标题':title,
        '发帖时间':time,
        '价格':price,
        '成色':new,
        '区域':location,
        '浏览量':view
    }
    # print(data)
    return data



first_url = 'http://bj.58.com/pbdn/0/pn4/'


urls = OnePageUrls(first_url)
data=[]
for url in urls:
    # print(url)
    sort=Info(url)
    data.append(sort)
    time.sleep(1)

print(data)

new = pymongo.MongoClient()
datadb = new.wuba
col = datadb.zhuanrang

col.insert(data)