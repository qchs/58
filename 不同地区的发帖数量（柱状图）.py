
# coding: utf-8

# In[40]:

import pymongo
import charts


# In[18]:

connection = pymongo.MongoClient()
tongcheng = connection['bjtongcheng']
item_info = tongcheng['item_info1']


# In[24]:

item_info.update_many({'area':'不明'},{'$set':{'area':['不明']}})    


# In[26]:

for i in item_info.find().limit(5):
    print(i['area'][0])
    '''
    #{'post_date': '2016.03.28', 
    'old': '-', 'title': '二手车交易，网', 
    'url': 'http://bj.58.com/tiaozao/25398442775728x.shtml', 
    'price': '50000',
    'area': ['通州', '永乐店'],
    '_id': ObjectId('56f8ec0d076afa0d604829b2'), 
    'cate': ['北京58同城', '北京二手市场', '北京其他二手物品', '北京二手杂七杂八']}
    '''
     


# In[27]:

area_all = [i['area'][0] for i in item_info.find()]
print(area_all)


# In[28]:

area_set = set(area_all)
print(area_set)


# In[30]:

area_index = list(area_set)
num = len(area_index)
print(area_index)
print(num)


# In[31]:

times = [area_all.count(i) for i in area_index]
print(times)


# In[32]:

t = area_all.count('西城')
print(t)


# In[33]:

for a,t in zip(area_index,times):
    print(a ,t)


# In[35]:

def data_gen(type):
    for a,t in zip(area_index,times):
        data = {
            'name' : a,
            'data' : [t],
            'type' : type
        }
        yield data


# In[46]:

series = [i for i in data_gen('column')]
print(series)


# In[38]:

options = {
    'title':{'text':'不同地区的发帖数量'}
}


# In[47]:

charts.plot(series,show = 'inline',options = options)


# In[ ]:



