def base62encode(n):
    lst = []
    s = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    while n > 0:
        y = n % 62
        lst.append(s[y])
        n = n // 62

    return "".join(lst[::-1])


if __name__ == '__main__':
    print(base62encode(1))  # 1
    print(base62encode(61))  # z
    print(base62encode(62))  # 10
    print(base62encode(185))  # 2z
