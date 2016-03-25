
# coding: utf-8

# In[10]:

import pymongo
import charts
import re


# In[70]:

connection = pymongo.MongoClient()
execl = connection['bjtongcheng']
item_info = execl['item_info2']


# In[43]:

for i in item_info.find().limit(300):
    print(i['url'])


# In[71]:

for i in item_info.find():
    cate = re.findall('com/(.*?)/',i['url'])
  
    item_info.update({'_id':i['_id']},{'$set':{'url':cate}})
for i in item_info.find():
    print(i['url'])


# In[72]:

cate_list = [item['url'][0] for item in item_info.find()]
catelog = list(set(cate_list))
print(catelog)
print(len(catelog))


# In[73]:

post_times = [cate_list.count(i) for i in catelog]
print(post_times)


# In[74]:

def date_gen(type):
    length = 0
    if length <= len(catelog):
        for cates,times in zip(catelog,post_times):
            data = {
                'name':cates,
                'data':[times],
                'type':type
            }
            yield data
#             print(data)
            length += 1
            
series = [i for i in date_gen('column')]
print(series)


# In[75]:

charts.plot(series,show = 'inline',options = dict(title= dict(text = 'aaa')))


# In[ ]:



