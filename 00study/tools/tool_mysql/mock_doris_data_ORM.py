from sqlalchemy import create_engine, Column, Integer, String, Float, BigInteger, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from faker import Faker

# 创建数据库连接
engine = create_engine('mysql://root:123456@localhost:13306/test')
# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

# 创建映射基类
Base = declarative_base()


# 定义数据表映射类
class Doris(Base):
    __tablename__ = 'doris_orm'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_name = Column(String(1024), nullable=True)
    rule_version = Column(String(1024), nullable=True)
    artifact_apply_id = Column(String(1024), nullable=False)
    stage = Column(String(100), nullable=False)
    metric_name = Column(String(100), nullable=True)
    metric_cal_time = Column(BigInteger, nullable=True)
    value = Column(Float, nullable=True)
    end_status = Column(SmallInteger, nullable=True)
    device_type = Column(String(100), nullable=True)
    artifact_id = Column(String(1024), nullable=True)


# 删除数据表
Base.metadata.drop_all(engine)
# 创建数据表
Base.metadata.create_all(engine)

# 使用 Faker 生成假数据
fake = Faker()
data = []
for _ in range(100):
    rule_name = fake.text(max_nb_chars=50).replace('\n', ' ')[:50]
    rule_version = f'rules_cn_0_v{fake.random_int(0, 999):03d}.{fake.random_int(0, 99):02d}'
    artifact_apply_id = fake.uuid4()
    stage = fake.random_element(['trial_op', 'formal_op'])
    metric_name = fake.random_element(['push_success_ratio', 'data_return_volume', 'cdm_coredump_cnt'])
    metric_cal_time = fake.random_int(1686246893916, 1694246893916)
    value = None
    if metric_name in ['data_return_volume', 'cdm_coredump_cnt']:
        value = fake.random_int(0, 100)
    elif metric_name == 'push_success_ratio':
        value = fake.random.uniform(0, 1)
    end_status = fake.random_element([0, 1, 2])
    device_type = fake.random_element(['vehicle', 'station'])
    artifact_id = fake.uuid4()

    data.append(
        Doris(
            rule_name=rule_name,
            rule_version=rule_version,
            artifact_apply_id=artifact_apply_id,
            stage=stage,
            metric_name=metric_name,
            metric_cal_time=metric_cal_time,
            value=value,
            end_status=end_status,
            device_type=device_type,
            artifact_id=artifact_id,
        )
    )

# 批量插入数据
session.bulk_save_objects(data)
# 提交事务
session.commit()
# 关闭会话
session.close()
