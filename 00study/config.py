import json
import os


class Config(object):
    KFK_BROKER = os.getenv('KFK_BROKER') or "127.0.0.1:9092"
    KFK_GROUP_ID = os.getenv('KFK_GROUP_ID') or "test_topic"
    KFK_CONFIG = json.loads(os.getenv('KFK_CONFIG')) if os.getenv('KFK_CONFIG') else \
        {
            'bootstrap_servers': [KFK_BROKER],
            'group_id': KFK_GROUP_ID,
            'enable_auto_commit': False,
            # max.poll.interval.ms,指定consumer两次poll的最大时间间隔（默认5分钟）,
            # 如果超过了该间隔consumer client会主动向coordinator发起LeaveGroup请求，触发rebalance；
            # 然后consumer重新发送JoinGroup请求
            'max_poll_interval_ms': 10 * 1000,
            # group coordinator检测consumer发生崩溃所需的时间。
            'session_timeout_ms': 10 * 1000,
            # 周期性地向group coordinator发送 heartbeat
            'heartbeat_interval_ms': 1000
        }

    @classmethod
    def get(cls, key, default=None):
        return getattr(cls, key, default)

    @classmethod
    def get_int(cls, key, default=0) -> int:
        r = getattr(cls, key, "0")
        if r.isdigit():
            return int(r)
        if r == "":
            return default
        raise Exception(f"{key}'s value {r} invalid")

    @classmethod
    def get_bool(cls, key, default=False) -> bool:
        r = getattr(cls, key, "false")
        if r == "":
            return default
        return r == "true"
