from kafka import KafkaProducer
import ssl


def newClientWithSSL(servers, topic, user, password):
    # 连接信息
    conf = {
        'bootstrap_servers': servers,  # ["ip1:port1", "ip2:port2", "ip3:port3"]
        'topic_name': topic,
        'sasl_plain_username': user,
        'sasl_plain_password': password
    }

    context = ssl.create_default_context()
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_REQUIRED
    # 证书文件，SSL证书参考“收集连接信息”章节获取
    context.load_verify_locations("phy_ca.crt")

    print('start producer')
    return KafkaProducer(bootstrap_servers=conf['bootstrap_servers'],
                         sasl_mechanism="PLAIN",
                         ssl_context=context,
                         security_protocol='SASL_SSL',
                         sasl_plain_username=conf['sasl_plain_username'],
                         sasl_plain_password=conf['sasl_plain_password'])


def newClient(servers):
    print('start producer')
    return KafkaProducer(bootstrap_servers=servers)


if __name__ == '__main__':
    hosts = ["127.0.0.1:9092"]
    topic_name = "test_py_client"
    # cli = newClientWithSSL(["127.0.0.1:9092"], topic_name, "fjp", "123456")
    cli = newClient(hosts)
    data = bytes("hello kafka!", encoding="utf-8")
    cli.send("test_py_client", data)
    cli.close()
    print('end producer')
