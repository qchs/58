from multiprocessing import Pool
from channel_extract import channel_list
from page_parsing import get_links_from ,url_list,get_item_info,item_info


def get_all_links_from(channel):
    for i in range(1,101):
        info = get_links_from(channel,i)
        if info == 'none':
            break

if __name__ =='__main__':
    # get_all_links_from( 'http://bj.58.com/bijiben/')
    all_channels = channel_list.split()
    pool = Pool()
    # pool.map(get_all_links_from,all_channels)
    print('url_list.count is :%s'%url_list.count())#88280

    all = set([item['url'] for item in url_list.find()])
    len1=len(all)
    print('set url_list count is:%s'%len1)
    done =  set([item['url'] for item in item_info.find()])#可省掉list.append(data)这一步
    len2 = len(done)
    print('set item_info count is:%s'%len2)

    set_undone = all - done
    len3= len(set_undone)
    print('still need to insert count is:%s'%len3)
    pool.map(get_item_info,set_undone)