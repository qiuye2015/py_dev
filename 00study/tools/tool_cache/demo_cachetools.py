import threading
import urllib.request
import cachetools
import operator


class CachedPEPs(object):
    def __init__(self, cachesize):
        self.cache = cachetools.LRUCache(maxsize=cachesize)
        self._lock = threading.RLock()

    @cachetools.cachedmethod(operator.attrgetter('cache'),
                             lock=operator.attrgetter('_lock'))
    def get(self, num):
        """Retrieve text of a Python Enhancement Proposal"""
        url = 'http://www.python.org/dev/peps/pep-%04d/' % num
        with urllib.request.urlopen(url) as s:
            return s.read()


peps = CachedPEPs(cachesize=10)
print("PEP #1: %s" % peps.get(1))
