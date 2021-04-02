import pandas as pd
import random
import math
from tqdm import tqdm


def readDatas():
    path = 'ml-latest-small/ratings.csv'
    odatas = pd.read_csv(path, usecols=[0, 1])
    # 每个用户看了哪些电影
    user_dict = dict()
    for d in odatas.values:
        if d[0] in user_dict:
            user_dict[d[0]].add(d[1])
        else:
            user_dict[d[0]] = {d[1]}
    return user_dict


def readItemDatas():
    path = 'ml-latest-small/ratings.csv'
    odatas = pd.read_csv(path, usecols=[0, 1])
    # 每个电影被哪些用户看了
    item_dict = dict()
    for d in odatas.values:
        if d[1] in item_dict:
            item_dict[d[1]].add(d[0])
        else:
            item_dict[d[1]] = {d[0]}
    return item_dict


def getTrainAndTestSet(dct):
    trainset, testset = dict(), dict()
    for uid in dct:
        one_user_set = dct[uid]
        testset[uid] = set(random.sample(one_user_set, math.ceil(0.2 * len(one_user_set))))
        trainset[uid] = one_user_set - testset[uid]

    return trainset, testset


def cosine(s1, s2, trainset):
    return len(trainset[s1] & trainset[s2]) / (len(trainset[s1]) * len(trainset[s2])) ** 0.5


def knn(trainset, k):
    user_sims = {}
    for u1 in tqdm(trainset):  # user1点击的item集合 tqdm:显示进度
        ulist = []
        for u2 in trainset:  # user2点击的item集合
            if u1 == u2 or len(trainset[u1] & trainset[u2]) == 0: continue

            rate = cosine(u1, u2, trainset)
            ulist.append({'id': u2, 'rate': rate})
        user_sims[u1] = sorted(ulist, key=lambda ulist: ulist['rate'], reverse=True)[:k]
    return user_sims


def get_reco(user_sims, o_set):
    recomedation = dict()
    for u in tqdm(user_sims):
        recomedation[u] = set()
        for sim in user_sims[u]:
            recomedation[u] |= (o_set[sim['id']] - o_set[u])
    return recomedation


def get_reco_by_itemCF(item_sims, o_set):
    recomedation = dict()
    for u in tqdm(o_set):
        recomedation[u] = set()
        for item in o_set[u]:  # 变量用户u点击的各个item
            recomedation[u] |= set(i['id'] for i in item_sims[item]) - o_set[u]
    return recomedation


def precisionAndRecall(pre, test):
    p, r = 0, 0
    for uid in test:
        t = len(pre[uid] & test[uid])
        p += t / (len(pre[uid]) + 1)
        r += t / (len(test[uid]) + 1)
    return p / len(test), r / len(test)


def play():
    odatas = readDatas()

    trset, teset = getTrainAndTestSet(odatas)
    user_sims = knn(trset, 5)
    # print(user_sims[1])
    pre_set = get_reco(user_sims, trset)

    print(pre_set[1])
    print(teset[1])
    p, r = precisionAndRecall(pre_set, teset)

    # ITEM_CF
    item_datas = readItemDatas()
    item_sims = knn(item_datas, 5)
    pre_set_by_itemCF = get_reco_by_itemCF(item_sims, trset)
    pi, ri = precisionAndRecall(pre_set_by_itemCF, teset)

    print(p, r)
    print(pi, ri)


if __name__ == '__main__':
    play()
