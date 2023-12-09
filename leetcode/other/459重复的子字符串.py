"""
给定一个非空的字符串 s ，检查是否可以通过由它的一个子串重复多次构成
    输入: s = "abab"
    输出: true
    解释: 可由子串 "ab" 重复两次构成

    输入: s = "aba"
    输出: false

    输入: s = "abcabcabcabc"
    输出: true
    解释: 可由子串 "abc" 重复四次构成。 (或子串 "abcabc" 重复两次构成。)

    1 <= s.length <= 104
    s 由小写英文字母组成

    O(n2) O(n)
"""
# s = input(">>>>: ")
s = "aba"
# s = "abcabcabcabc"
# s = "abab"

for i in range(2, len(s) // 2 + 1):
    lst = s.split(s[:i])
    lst = [item for item in lst if item != ""]  # 这行代码移除列表中的空字符串。这可能发生在原始字符串以子字符串开头或结尾的情况
    if not lst:
        print(f"True,输入可由 {s[:i]} 重复 {int(len(s) / i)} 次组成")
        break
else:
    print("False")
