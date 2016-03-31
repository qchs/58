
# coding: utf-8

# In[1]:

import pymongo
import charts


# In[2]:

connection = pymongo.MongoClient()
tongcheng = connection['bjtongcheng']
item_info = tongcheng['item_info1']


# In[4]:

for i in item_info.find().limit(3):
    print(i['cate'][2])


# In[5]:

cate_all = [i['cate'][2] for i in item_info.find()]
print(cate_all)


# In[6]:

cate_set = set(cate_all)
print(cate_set)


# In[7]:

cate_index = list(cate_set)
num = len(cate_index)
print(cate_index,num)


# In[8]:

times = [cate_all.count(i) for i in cate_index ]
print(times)


# In[9]:

def data_gen(type):
    for c,t in zip(cate_index,times):
        data = {
            'name':c,
            'data':[t],
            'type':type
        }
        yield data


# In[10]:

series = [i for i in data_gen('column')]
print(series)


# In[12]:

options = {
    'title':{'text':'不同类目的发帖数量'}
}


# In[13]:

charts.plot(series,show = 'inline',options = options)


# In[ ]:



