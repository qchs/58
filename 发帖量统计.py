
# coding: utf-8

# In[1]:

import pymongo
import charts
from datetime import timedelta,date


# In[2]:

connection = pymongo.MongoClient()
tongcheng = connection['bjtongcheng']
item_info = tongcheng['item_info2']


# In[3]:

for i in item_info.find({'post_date':{'$in':['2016.01.14','2016.03.16']}},{'area':{'$slice':1},'_id':0,'price':0,'title':0}).limit(30):
    print(i)


# In[4]:

for i in item_info.find({},{'post_date':1}).limit(30):
#     print(i)#{'post_data': '2016.03.04'},{'post_data': '2016-03-11'}
    
#     print(a)#2016.03.04,2016-03-11
#     dot = i['post_data'].replace('-','.')
#     print(dot)#2016.03.04,2016.03.11
#     item_info.update_one({'_id':i['_id']},{'$set':{'post_data':dot}})
    print(i)


# In[5]:

def get_all_dates(date1,date2):
    the_date = date(int(date1.split('.')[0]),int(date1.split('.')[1]),int(date1.split('.')[2]))
    end_date = date(int(date2.split('.')[0]),int(date2.split('.')[1]),int(date2.split('.')[2]))
    print(the_date,end_date)
    days = timedelta(days = 1)
    while the_date <= end_date:
        yield (the_date.strftime('%Y.%m.%d'))
        the_date = the_date + days
                    
                                                 


# In[6]:

for i in get_all_dates('2016.01.23','2016.03.24'):
    print(i)
    


# In[9]:

def get_data_within(date1,date2,areas):
    for area in areas:
        area_day_post=[]
        for date in get_all_dates(date1,date2):
            a = list(item_info.find({'post_date':date,'area':area}))
            count = len(a)
#             print(date,area,count)
            area_day_post.append(count)
        data = {
            'name':area,
            'data':area_day_post,
            'type':'line'
        }
        yield data


# In[10]:

for i in get_data_within('2016.02.10','2016.03.24',['朝阳','海淀','不明']):
    print(i)


# In[14]:

dates = [i for i in get_all_dates('2016.03.10','2016.03.24')]
print(dates)
options = {
    'chart':{'zoomType':'xy'},
    'title':{'text':'发帖量统计'},
    'subtitle':{'text':'可视化统计图表'},
    'xAxis':{'categories':dates},
    'yAxis':{'title':{'text':'数量'}}
}
series = [i for i in get_data_within('2016.03.10','2016.03.24',['朝阳','海淀','不明','通州','丰台'])]
print(series) #[{'date': [2, 10, 51, 61, 12, 49, 44, 30, 1, 89, 43, 61, 2, 124, 1], 'type': 'line', 'name': '不明'}]
# series = [
# #     {'data': [220, 217, 259, 266, 322, 287, 309, 307, 346, 440, 488, 641, 649], 'type': 'line', 'name': '朝阳'},
# #     {'data': [137, 146, 154, 156, 176, 183, 171, 217, 239, 284, 288, 397, 395], 'type': 'line', 'name': '海淀'},
#     {'data': [58, 54, 74, 57, 82, 84, 93, 79, 114, 113, 133, 151, 201], 'type': 'line', 'name': '通州'}
#     ]
charts.plot(series,options = options,show = 'inline')


# In[ ]:



