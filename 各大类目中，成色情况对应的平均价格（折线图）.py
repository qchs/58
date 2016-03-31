
# coding: utf-8

# In[47]:

import pymongo
import charts


# In[48]:

connection = pymongo.MongoClient()
tongcheng = connection['bjtongcheng']
item_info = tongcheng['price1']


# In[68]:

for i in item_info.find({'price':{'$in':['未知','面议']}},{'price':1,'_id':1}):
#     item_info.update_one({'_id':i['_id']},{'$set':{'price':-1}})
    print(i)


# In[88]:

for i in item_info.find({'price':{'$ne':-1}},{'price':1,'_id':1}):    
    yuan = i['price'][-1]
    if yuan  == '元':
        print(i)
        print(i['price'][:-1])
        item_info.update_one({'_id':i['_id']},{'$set':{'price':i['price'][:-1]}})
    


# In[92]:

for i in item_info.find({},{'price':1,'_id':1}):    
    item_info.update_one({'_id':i['_id']},{'$set':{'price':int(i['price'])}})
    print(i)


# In[93]:

for i in item_info.find({},{'price':1,'_id':1}).limit(300):    
    print(i)


# In[103]:

pipeline_cate =[
    {'$group':{'_id':{'$slice':['$cate',2,1]},'count':{'$sum':1}}}
]

cate_index =[i['_id'][0] for  i in item_info.aggregate(pipeline_cate)]
print(cate_index)
print(len(cate_index))
        
  


# In[240]:

for i in item_info.find({'cate':'北京二手手机'},{'old':1,'_id':0,'price':1}).limit(300):    
    print(i)


# In[77]:




# In[ ]:




# In[104]:




# In[236]:




# In[217]:

def get_data(cate): #复制一个数据库，把里面的成色为'-',和价格为'面议'的都删掉，并且把价格的值由字符串转化为整数
    pipeline = [
        {'$project':{
                '_id':1,                
                'price':1,
#                 'cate':{'$slice':['$cate',2,1]},
                'cate':1,
                'old':1,
                'h_old':{
                    '$cond' :{ 'if' :{'$gt' :['$old','-']}, 'then': 1 ,'else':0 }
                },              
               
            }
                             
        },    
        {'$match':{'$and':[{'cate':cate},{'h_old':1},{'price':{'$gt':0}}]}},       
        {'$group':{'_id':'$old','counts':{'$sum':1},'sums':{'$sum':'$price'},'avg':{'$avg':'$price'}}},#,'avg':{'$avg':'$price)'}
        {'$sort':{'avg':-1}},
        {'$limit':500}
    ]
    
    for  i in item_info.aggregate(pipeline):
#         print(i)
#         data = {
#             'name':i['_id'],
#             'data':[i['avg']],
#             'type':'line'
#         }
        yield [i['_id'],[i['avg']]]


# In[204]:

for cate in cate_index:
    get_data(cate)
    print(cate +'.............................................................................')


# In[241]:


cate = cate_index[-3]
data = get_data(cate)
for i in data:    
    print(i)
    
series = [{
        'name':'价格',
        'data':[i[1] for i in get_data(cate)],
        'type':'line'
    }]
print(series)


# In[242]:

options = {
    'chart':{'zoomType':'xy'},
    'title':{'text':cate +'中，成色情况对应的平均价格'},
    'xAxis':{'categories':[i[0] for i in get_data(cate)]}
}


# In[243]:

charts.plot(series,options=options,show = 'inline')


# In[ ]:



