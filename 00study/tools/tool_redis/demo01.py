import redis

r = redis.Redis(host='localhost', port=6379, db=0)
# res = r.set('foo', 'bar')
# print(res)
# res = r.get('foo')
# print(res)


# pipe = r.pipeline()
# pipe.set('foo', 5)
# pipe.execute()

res = r.sadd("fjp-set", "1", "3")
print(res)
#
# res = r.scard("fjp-set")
#
# print(res)
# res = r.expire("fjp-set", 10)
# print(res)
# time.sleep(1)
res = r.scard("fjp-set")
print(res)


def scan_keys(redis, match):
    """Iterate over matching keys."""
    prev_cursor = None
    while True:
        cursor, keys = redis.scan(prev_cursor, match=match)
        for key in keys:
            yield key
        if cursor is None:
            break
        if cursor == prev_cursor:
            raise Exception(f"Redis scan stuck on cursor {cursor}")
        prev_cursor = cursor

# for key in scan_keys(redis,match_pattern)