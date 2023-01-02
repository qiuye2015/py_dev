# import json
#
# # a = {'context': {'ugi': '{"user":"fei.su","pass":"AY8MKXM9KS"}',
# #                  'reason': '第三次EU数据清理\r\n* 全clip静止数据(除es7/es8 以外所有EU数据):7108\r\n* ava_status=1 入库不全数据集(保留20221115以前数据,按毛敏要求, 没算上PSAP数据): 6471\r\n* EU2CN剩余所有数据删除(保留20221208及之后的数据):63216\t\r\n',
# #                  'region': 'cn', 'op_type': 'delete', 'data_type': 'offline', 'request_id': '1671955202085',
# #                  'task_rowkey': 'eb773c290939f03c04496337b8aa8d29', 'workflow_creator': 'fei.su',
# #                  'to_del_start_time': 1672299890000, 'workflow_created_time': 1671955203683,
# #                  'workflow_cost_center_id': '8110030000', 'task_id': 'b7abe800-5f67-43e5-84f9-1c9455db996f'},
# #      'biz_code': '', 'status': 'success', 'current_node_name': '结束', 'flow_instance_node_name': '结束',
# #      'previous_node_name': '结束', 'last_status_flow_instance_node_name': '结束',
# #      'flow_instance_id': 'PRDSHJQLRW-2022122516574-4706'}
#
# a = {'context': {'ugi': '{"user":"leo.fu1","pass":"BHB83ICUGM"}', 'reason': 'test send pipeline update status',
#                  'region': 'cn', 'op_type': 'delete', 'data_type': 'offline', 'request_id': '1671972633095',
#                  'task_rowkey': 'b6584e1334980e766a297b823b61aaf6', 'workflow_creator': 'leo.fu1',
#                  'to_del_start_time': 1672231734000, 'workflow_created_time': 1671972634582,
#                  'workflow_cost_center_id': '1100320200', 'task_id': 'e7b1568e-8652-41d5-83f2-570c9075b307'},
#      'biz_code': '', 'status': 'success', 'current_node_name': '结束', 'flow_instance_node_name': '结束',
#      'previous_node_name': '结束', 'last_status_flow_instance_node_name': '结束',
#      'flow_instance_id': 'DSHJQLRW-2022122520883-2806'}
# b = json.dumps(a)
# print(b)
import os

lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]  # lst可为空，最后返回值也为空
num = 4  # 定义每组包含的元素个数
for i in range(0, len(lst), num):
    tmp = lst[i:i + num]
    for j in range(0, num, 2):
        for a in tmp[j:j + 2]:
            print(a, end=' ')
        print("")

    print("---")
