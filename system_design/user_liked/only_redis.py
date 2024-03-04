import time

import redis

# 初始化 Redis 连接
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


# 点赞/取消点赞
def like_item(user_id, like_type, liked_item_key):
    # 获取当前时间戳
    timestamp = time.time()

    # 构建点赞记录的唯一标识
    like_id = f'{like_type}:{user_id}'

    # 检查用户是否已经点赞
    is_liked = redis_client.zscore(liked_item_key, like_id)

    if is_liked is not None:
        # 用户已经点赞，执行取消点赞操作
        redis_client.zrem(liked_item_key, like_id)
        print(f'用户 {user_id} 取消了对 {liked_item_key} 的点赞')
    else:
        # 用户未点赞，执行点赞操作
        redis_client.zadd(liked_item_key, {like_id: timestamp})
        print(f'用户 {user_id} 点赞了 {liked_item_key}')


# 查询点赞数
def get_like_count(liked_item_key):
    like_count = redis_client.zcard(liked_item_key)
    print(f'{liked_item_key} 的点赞数为: {like_count}')


# 查询是否点赞
def is_user_liked(user_id, like_type, liked_item_key):
    like_id = f'{like_type}:{user_id}'
    is_liked = redis_client.zscore(liked_item_key, like_id)
    if is_liked is not None:
        print(f'用户 {user_id} 已经点赞了 {liked_item_key}')
    else:
        print(f'用户 {user_id} 未点赞 {liked_item_key}')


# 查询点赞历史
def get_like_history(liked_item_key):
    # 获取当前时间戳
    current_timestamp = time.time()

    # 查询点赞历史，按照时间降序排列
    like_history = redis_client.zrangebyscore(liked_item_key, 0, current_timestamp, withscores=True)

    if like_history:
        print(f'{liked_item_key} 的点赞历史:')
        for like_id, timestamp in like_history:
            like_type, user_id = like_id.decode('utf-8').split(':', 1)
            print(f'\t用户 {user_id} 在 {timestamp} 点赞了 {like_type} {liked_item_key}')
    else:
        print(f'{liked_item_key} 暂无点赞历史')


def main():
    # 定义点赞主体的唯一键
    liked_item_key = 'post:123'  # 以帖子ID为例

    # 定义用户ID和点赞类型
    user_id = 'user:456'
    like_type = 'post_like'

    # 示例操作
    like_item(user_id, like_type, liked_item_key)
    get_like_count(liked_item_key)
    is_user_liked(user_id, like_type, liked_item_key)
    get_like_history(liked_item_key)


if __name__ == '__main__':
    print("")
    main()
