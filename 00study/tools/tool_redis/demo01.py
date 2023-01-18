import time

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
