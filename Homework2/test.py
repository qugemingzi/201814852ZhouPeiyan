# encoding=utf-8
from collections import Counter

x = {'apple': 1, 'banana': 2}
y = {'banana': 10, 'pear': 11}
print(sum(x.values()))
z = {}
z["a"] = Counter(x)
z["b"] = Counter(y)
print(z)
z["c"] = z["a"] + z["b"]
print(sum(z["c"].values()))
print(z + "!")
print(2 ** 5)
