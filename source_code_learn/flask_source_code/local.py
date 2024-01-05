import threading


class Local(object):
    def __init__(self):
        object.__setattr__(self, 'storage', {})

    # def __setattr__(self, key, value):
    #     ident = threading.get_ident()
    #     if ident in self.storage:
    #         self.storage[ident][key] = value
    #     else:
    #         self.storage[ident] = {key: value}
    #
    # def __getattr__(self, item):
    #     ident = threading.get_ident()
    #     if ident not in self.storage:
    #         return
    #
    #     return self.storage[ident].get(item)

    def __setattr__(self, key, value):
        ident = threading.get_ident()
        if ident in self.storage:
            self.storage[ident][key].append(value)
        else:
            self.storage[ident] = {key: [value, ]}

    def __getattr__(self, item):
        ident = threading.get_ident()
        if ident not in self.storage:
            return

        return self.storage[ident][item][-1]


local = Local()


def task(arg):
    local.x1 = arg
    print(local.x1)


for i in range(5):
    t = threading.Thread(target=task, args=(i,))
    t.start()

