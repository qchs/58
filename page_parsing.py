import requests,pymongo,re
from bs4 import BeautifulSoup

connection = pymongo.MongoClient()
tongcheng = connection['bjtongcheng']
url_list = tongcheng['url_list']
item_info = tongcheng['item_info2']
delete_url = tongcheng['delete_url']




# channel =   'http://bj.58.com/shouji/'
# http://yc.58.com/bijiben/0/pn2/v

def get_links_from(channel,page,who_sell=0):
    url = channel + str(who_sell) + '/' + 'pn%s/'%page
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    have_goods = soup.select('#infolist table tr td.t ')#到了第5页就为空，没有了
    if have_goods:
        # goods_url = soup('a','t',target = '_blank')#infolist > table:nth-child(5) > tbody > tr:nth-child(1) > td.t > a
        goods_url = soup.select('#infolist > table > tr[logr*="ses"] > td.t > a:nth-of-type(1) ')#这样筛出来全部是个人转让
        if goods_url:
            # print('该页有以下内容')
            for each in goods_url:
                u = each.get('href')
                clean_url = u.split('?')[0]
                # print(clean_url)
                url_list.insert_one({'url':clean_url})

            # print(goods_url)
        else:
            print(' %s 没有个人转让内容了。'%url)
            return 'none'
    else:
        print(' %s 没有内容。'%url)
        return 'none'
    print('该页url= %s \n'%url) #http://yc.58.com/taishiji/0/pn10/
    # print(have_goods)

def get_item_info(url):
    # print('下面的内容来自：%s'%url)
    r= requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    delete1 = soup.select('body > script:nth-of-type(4)')[0].text #clickLog('from=58_404');
    delete = soup.select('#404content')
    # print('判断是否被删除')
    # print(delete)
    not_found = re.findall('58_(.*?)\'',delete1)

    # print(not_found)
    # print(delete)
    if delete or not_found:
        print('该页已被删除')
        pass
    else:
        print(url)
        area_div = soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(4) > div.su_con > span a')
        # print('area is %s'%area_div)
        if area_div:
            area = list(map(lambda x:x.text,area_div))
        else:
            area = '不明'

        title = list(soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.mainTitle > h1')[0].stripped_strings)[0]
        post_data = soup.select('li.time')[0].text
        price_div = soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(1) > div.su_con > span')
        if price_div:
            price = list(price_div[0].stripped_strings)[0]
        else :
            price = '未知'
        info ={
            'url':url,
            'title':title,
            'post_data':post_data,
            'price':price,
            'area' :area
        }
        #index_show > h1
        print(info)
        item_info.insert_one(info)


# i = 'http://bj.58.com/shuma/25446932222523x.shtml'
j= 'http://bj.58.com/bijibendiannao/25069359195182x.shtml'
k = 'http://bj.58.com/ershoushebei/25346721210311x.shtml'
y = 'http://bj.58.com/bijibendiannao/25382506676535x.shtml'
c = 'http://bj.58.com/zixingche/25213891728811x.shtml'
b = 'http://bj.58.com/zixingche/25449900427069x.shtml'
noprice = 'http://bj.58.com/ershoushebei/25456190215481x.shtml'
# get_item_info(noprice)