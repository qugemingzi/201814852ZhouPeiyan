import re

from nltk.corpus import stopwords

print("\'" in "I haven't hehe")
print(any(char.isdigit() for char in "sdcsc2sdvsv"))
print(any(char.isdigit() for char in "sdcscsdvsv"))
print(bool(re.search(r'\d', "sdcsc2sdvsv")))
print(bool(re.search(r'\d', "sdcscsdvsv")))
print(stopwords.words("english"))
print("sdc+s".isalpha())