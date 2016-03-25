from page_parsing import url_list,item_info
import time

while True:
    count = url_list.count()
    count2 = item_info.count()
    print('现有%d条数据'%count)
    print('现2有%d条数据'%count2)
    time.sleep(5)