
# coding: utf-8

# In[19]:

import pymongo
import charts
import re


# In[25]:

connection = pymongo.MongoClient()
execl = connection['bjtongcheng']
item_info = execl['item_info3']


# In[27]:

for i in item_info.find().limit(300):
#     print(i)
    print(i['url'])
    cate = re.findall('com/(.*?)/',i['url'])#list
    print('cate is %s'%cate)


# In[33]:

for i in item_info.find():
    cate = re.findall('com/(.*?)/',i['url'])[0] #str
    print('cate is %s'%cate)
  
    item_info.update({'_id':i['_id']},{'$set':{'url':cate}})
    
    
# for i in item_info.find(): #这两个不能在同一个块里执行，不然，更改后再执行更改，就要报错
#     print(i['url'])  #str
    


# In[36]:

cate_list = [item['url'] for item in item_info.find()]
# print(cate_list)
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



