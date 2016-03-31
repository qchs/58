
# coding: utf-8

# In[2]:

import pymongo
import charts
from datetime import timedelta,date


# In[3]:

connection = pymongo.MongoClient()
tongcheng = connection['bjtongcheng']
item_info = tongcheng['item_info1']


# In[22]:

for i in item_info.find({'post_date':'2016.03.24','area':'海淀'},{'area':1,'post_date':1,'_id':0}).limit(3):
    print(i)


# In[4]:

area_all = [i['area'][0] for i in item_info.find()]
# print(area_all)


# In[5]:

area_set = set(area_all)
# print(area_set)


# In[6]:

areas = list(area_set)
# num = len(areas)
# print(areas)
# print(num)


# In[7]:

# dateT = '2016.03.25'
# for area in areas:
#     a = list(item_info.find({'post_date':dateT,'area':area},{'area':{'$slice':1},'post_date':1,'_id':0}).limit(2))
#     print(a)


# In[7]:

def get_all_dates(date1,date2):
#     start = list(map(lambda x:int(x),date1.split('.')))#[2016, 2, 14]
    s1 = date1.split('.')
    s2 = date2.split('.')#['2016', '02', '14'] ['2016', '03', '25']
#     print(s1,s2)
    start = date(int(s1[0]),int(s1[1]),int(s1[2]))#2016-02-14 2016-03-25
    end = date(int(s2[0]),int(s2[1]),int(s2[2]))
#     sdot = start.strftime('%Y.%m.%d')#2016.02.14
    days = timedelta(days = 1)
    while start <= end:
        yield start.strftime('%Y.%m.%d')
        start = start + days


# In[8]:

date1 = '2016.02.25'
date2 = '2016.03.25'
for i in get_all_dates(date1,date2):
    print(i)


# In[9]:

def get_date_within(date1,date2,areas):
    for area in areas:
        area_post = []
        for date in get_all_dates(date1,date2):
            a = list(item_info.find({'post_date':date,'area':area}))
            each_day_post = len(a)
            area_post.append(each_day_post)
#             print(date,area,each_day_post)
        data={
            'name' : area,
            'data' : area_post,
            'type' :'line'
        }
        yield data
            


# In[10]:

# for i in get_date_within(date1,date2,areas):
#     print(i)


# In[11]:

series = [i for i in get_date_within(date1,date2,areas)]
# print(series)


# In[12]:

options = {
    'chart':{'zoomType':'xy'},
    'title':{'text':'N日内指定区的发帖量的变化曲线'},
    'xAxis':{'categories':[i for i in get_all_dates(date1,date2)]}
    
}
print(options)


# In[21]:

charts.plot(series,options=options,show = 'inline')


# In[ ]:



