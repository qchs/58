
# coding: utf-8

# In[1]:

import charts
import pymongo


# In[2]:

connection = pymongo.MongoClient()
tongcheng = connection['bjtongcheng']
item_info = tongcheng['item_info2']


# In[8]:

for i in item_info.find().limit(1):
    print(i)


# In[10]:

pipeline = [
    {'$match':{'post_date':'2016.02.27'}}
]


# In[13]:

for i in item_info.aggregate(pipeline):
    print(i)


# In[18]:

pipeline2 = [
    {'$match':{'$and':[{'post_date':'2016.02.27'},{'price':'1000 元'}]}}
]


# In[19]:

for i in item_info.aggregate(pipeline2):
    print(i)


# In[42]:

pipeline3 = [
    {'$match':{'$and':[{'post_date':'2016.02.27'}]}},
    {'$group':{'_id':'$price','counts':{'$sum':1}}},
    {'$sort' :{'counts': -1}},
    {'$limit':100}
]#某天发的帖子里，价格的分布图


# In[43]:

for i in item_info.aggregate(pipeline3):
    print(i)


# In[62]:

def data_gen(date):
    pipeline4 = [
        {'$match':{'post_date':date}},
        {'$group':{'_id':'$price','counts':{'$sum':1}}},
        {'$sort' :{'counts': -1}},
        {'$limit':10}
    ]
    for i in item_info.aggregate(pipeline4):
#         print([i['_id'],i['counts']])#['200 元', 59]
        yield [i['_id'],i['counts']]
        
    


# In[ ]:




# In[63]:

data = [i for i in data_gen('2016.03.16')]
# print(data)

series = [{
        'type':'pie',
        'name':'fenbu',
        'data':data
    }]

options = {
    'chart':{'zoomType':'xy'},
    'title':{'text':'price'},
    'subtitle':{'text':'perday'}
}

charts.plot(series,options= options,show = 'inline')


# In[ ]:



