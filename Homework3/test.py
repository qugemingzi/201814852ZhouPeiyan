# encoding=utf-# encoding=utf-8
import json
from collections import Counter

DatasetPath = "D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework3\\DataSet\\Tweets.txt"
with open(DatasetPath, "r", errors="replace") as f:
    for line in f:
        js_tweets = line
        print(js_tweets)
        tweets = json.loads(js_tweets)
        for key in tweets:
            if key == "text":
                print(tweets[key])
            elif key == "cluster":
                print("cluster: ", tweets[key])
                num = int(tweets[key])
                print(type(num))

list = [30, 20, 20, 20, 20, 4, 4, 4, 5, 4, 4, 4]
result = Counter(list).most_common(1)
print(type(result))
print(result[0][1])

for i in range(2, 90, 3):
    print(i)
