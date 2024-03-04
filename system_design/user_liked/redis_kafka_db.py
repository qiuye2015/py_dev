from datetime import datetime

from confluent_kafka import Consumer, KafkaError, Producer
import redis
from redisbloom.client import Client
from sqlalchemy import Column, create_engine, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 初始化 Redis 连接
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# 初始化 Redis Bloom Filter
bloom_filter = Client(host='localhost', port=6379)

# 初始化 Kafka 生产者
kafka_producer = Producer({'bootstrap.servers': 'localhost:9092'})

# 初始化 Kafka 消费者
kafka_consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'user-behavior-group',
    'auto.offset.reset': 'earliest'
})

# 初始化 SQLAlchemy 引擎
db_engine = create_engine('sqlite:///user_data.db')
Base = declarative_base()


# 定义用户行为数据模型
class UserBehavior(Base):
    __tablename__ = 'user_behavior'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    action_type = Column(String, nullable=False)
    liked_item_id = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


# 创建表
Base.metadata.create_all(db_engine)

# 创建会话
Session = sessionmaker(bind=db_engine)
db_session = Session()


# 点赞
def like_item(user_id, liked_item_id):
    # 使用 INCR 保证点赞数一致性
    redis_client.incr(f'likes:{liked_item_id}')

    # 使用 Bloom Filter 记录是否点赞
    bloom_filter.bfAdd(f'likes_bloom:{liked_item_id}', user_id)

    # 发送 Kafka 消息
    kafka_producer.produce('user-behavior-topic', value=f'{{"user_id": "{user_id}", "action": "like", "liked_item_id": "{liked_item_id}"}}')


# 取消点赞
def unlike_item(user_id, liked_item_id):
    # 使用 INCR 保证点赞数一致性
    redis_client.decr(f'likes:{liked_item_id}')

    # 使用 Counting Filter 记录取消点赞
    redis_client.bitfield(f'likes_bitmap:{liked_item_id}', 'DECRBY', 'u4', 1, 'GET', 'u4', 0)

    # 发送 Kafka 消息
    kafka_producer.produce('user-behavior-topic', value=f'{{"user_id": "{user_id}", "action": "unlike", "liked_item_id": "{liked_item_id}"}}')


# 消费 Kafka 消息
def consume_kafka_messages():
    kafka_consumer.subscribe(['user-behavior-topic'])

    while True:
        msg = kafka_consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f'Error: {msg.error()}')
                break

        # 解析消息
        user_behavior_data = eval(msg.value().decode('utf-8'))

        # 保存用户行为数据到关系型数据库
        save_user_behavior_to_db(user_behavior_data)


# 保存用户行为数据到关系型数据库
def save_user_behavior_to_db(user_behavior_data):
    user_behavior = UserBehavior(
        user_id=user_behavior_data['user_id'],
        action_type=user_behavior_data['action'],
        liked_item_id=user_behavior_data.get('liked_item_id')
    )
    db_session.add(user_behavior)
    db_session.commit()


# 示例操作
like_item('user123', 'post456')
unlike_item('user123', 'post456')

# 消费 Kafka 消息
consume_kafka_messages()
