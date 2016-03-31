
# coding: utf-8

# In[1]:

import pymongo
import charts


# In[2]:

connection = pymongo.MongoClient()
tongcheng = connection['bjtongcheng']
item_info = tongcheng['item_info1']


# In[3]:

area_all = [i['area'][0] for i in item_info.find()]


# In[4]:

area_set = set(area_all)


# In[5]:

area_index = list(area_set)
num = len(area_index)
print(area_index)
print(num)


# In[35]:

area = area_index[1]


# In[30]:

def get_data(area):
    pipeline=[      
        {'$match':{'area':area}},
        {'$group':{'_id':{'$slice':['$cate',2,1]},'counts':{'$sum':1}}},
        {'$sort':{'counts':-1}},
        {'$limit':3}
            
        ]
    for i in item_info.aggregate(pipeline):
        data = {
            'name':i['_id'][0],
            'data':[i['counts']],
            'type':'column'
        }
        yield data
        
#         print(i)


# In[31]:

for i in get_data(area):
    print(i)


# In[36]:

series = [i for i in get_data(area)]


# In[46]:

options = {
    'title':{'text':area + 'top3大类目和发帖量'},
    'chart':{'zoomType':'xy'},
    'xAxis':{'categories':[i['name'] for i in get_data(area)]}
}
print(options)


# In[47]:

charts.plot(series,options=options,show = 'inline')


# In[ ]:



