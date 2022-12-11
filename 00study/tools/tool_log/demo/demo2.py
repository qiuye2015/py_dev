# Logger与Handler的级别
# logger是第一级过滤，然后才能到handler，
# 我们可以给logger和handler同时设置level，如果将logger等级设为debug，handler设为info，
# 那么handler对象的输出不会包含debug级别的日志，因为debug < info
# 验证
import logging


form = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                         datefmt='%Y-%m-%d %H:%M:%S %p',)

ch = logging.StreamHandler()

ch.setFormatter(form)
ch.setLevel(10)
# ch.setLevel(20)

l1 = logging.getLogger('root')
# l1.setLevel(20)
l1.setLevel(10)
l1.addHandler(ch)

l1.debug('l1 debug')
