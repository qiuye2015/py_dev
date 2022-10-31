# from kafka import KafkaConsumer
#
# # consumer = kafka.KafkaConsumer(topic,
# #                                auto_offset_reset='earliest',
# #                                enable_auto_commit=False,
# #                                group_id=group,
# #                                sasl_plain_username=user,
# #                                sasl_plain_password=password,
# #                                sasl_mechanism='SCRAM-SHA-512',
# #                                security_protocol='SASL_PLAINTEXT',
# #                                bootstrap_servers=brokers)
# topic = "test"
# group_id = "group2"
# bootstrap_servers = ['localhost:9092']
# consumer = KafkaConsumer(topic, group_id=group_id, bootstrap_servers=bootstrap_servers)
#
# topics = consumer.topics()
# print("topics", topics)
# partitions = consumer.partitions_for_topic(topic)
# print("partitions", partitions)
#
# for msg in consumer:
#     print("msg: ", msg)
#     for m in msg.headers:
#         if m[0] == "ps":  # partition sequence
#             print(int(m[1].decode()))
#         elif m[0] == "ShardId":
#             print(str(m[1].decode()))
#         else:
#             print("else", msg.headers)
#
# # ConsumerRecord(
# # topic='test',
# # partition=0,
# # offset=3,
# # timestamp=1666185736086,
# # timestamp_type=0,
# # key=None,
# # value=b'ttt',
# # headers=[],
# # checksum=None,
# # serialized_key_size=-1,
# # serialized_value_size=3,
# # serialized_header_size=-1
# # )

from kafka import KafkaConsumer
import ssl


def newClientWithSSL(topic_name, servers, group_id, user, password):
    context = ssl.create_default_context()
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_REQUIRED
    # 证书文件，SSL证书参考“收集连接信息”章节获取
    context.load_verify_locations("phy_ca.crt")

    print('start consumer')
    return KafkaConsumer(topic_name,
                         bootstrap_servers=servers,
                         group_id=group_id,
                         sasl_mechanism="PLAIN",
                         ssl_context=context,
                         security_protocol='SASL_SSL',
                         sasl_plain_username=user,
                         sasl_plain_password=password)


def newClient(topic_name, servers, group_id):
    return KafkaConsumer(topic_name,
                         bootstrap_servers=servers,
                         group_id=group_id)


if __name__ == '__main__':
    hosts = ["127.0.0.1:9092"]
    topicName = "test_py_client"
    cli = newClient(topicName, hosts, "group_test_1")
    for message in cli:
        print("%s:%d:%d: key=%s value=%s" % (
            message.topic, message.partition, message.offset, message.key, message.value))

    print('end consumer')
