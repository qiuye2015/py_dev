from adwsdk.adw_client import AdwClient
from adwsdk import cmm

table_name = 'production/collection/keydata'  # 不是 table_21

# 初始化客户端
adw_client = AdwClient(env='uat-eu', adw_user='leo.fu1', adw_pass='N8LO5K9Q4Q')

sys_data_name_prefix = "fjp_test_"
for num in range(20, 30):
    data_name = sys_data_name_prefix + str(num)
    print(data_name)
    put = cmm.Put(table_name, data_name, 0)
    # meta_dict 中的key即为表的字段名字，value为表的字段值，值的类型需与建表时的字段类型一致
    meta_dict = {'biz_type': 'biz_type6', 'uuid': num, 'date': 10}
    # 设置要写入的 row 字段和值
    put.set_meta_dict(meta_dict)
    # 写入数据到表
    res = adw_client.put(put)
    print(res)


# update_meta = {'biz_type': 'biz_type5'}
# rowkey = '754242b7659f04befe2ac4cfc897b28a'
# where=""
# update = cmm.Update(table_name, rowkey, where="")
# update.set_meta_dict(update_meta)
# update_res = adw_client.update(update)
# print(update_res)
# rowkey = "30e17348f86b297f59f5f6de7ce83ee3"
# get = cmm.Get(table_name, rowkey)
# get_res = adw_client.get(get)
# print(get_res.meta)
#
# delete = cmm.Delete(table_name, rowkey)
# del_res = adw_client.delete(delete)
# print(del_res)
