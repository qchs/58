
# coding: utf-8

# In[3]:

import pymongo
import charts


# In[2]:

connection = pymongo.MongoClient()
tongcheng = connection['bjtongcheng']
item_info = tongcheng['item_info1']


# In[20]:

date1 = '2016.03.15'
pipeline = [
    {'$match':{'post_date':date1}},
    {'$group':{'_id':{'$slice':['$cate',2,1]},'counts':{'$sum':1}}},
    {'$sort':{'counts':-1}},
    {'$limit':10}
]


# In[23]:

for i in item_info.aggregate(pipeline):
    print(i)
    print(i['_id'][0],i['counts'])


# In[26]:

def get_data(date):
    pipeline = [               
        {'$match':{'post_date':date1}},
        {'$group':{'_id':{'$slice':['$cate',2,1]},'counts':{'$sum':1}}},
        {'$sort':{'counts':-1}},
        {'$limit':10}
    ]
    for i in item_info.aggregate(pipeline):
       yield i['_id'][0],i['counts']


# In[27]:

for i in get_data(date1):
    print(i)


# In[36]:

series = [{
        'type':'pie',
        'name':'发帖量',
        'data': [i for i in get_data(date1) ]
    }]


# In[34]:

options = {
    'title':{'text':'某一天内，各类目的发帖量（饼状图）'}
}


# In[37]:

charts.plot(series,options=options,show = 'inline')


# In[ ]:



