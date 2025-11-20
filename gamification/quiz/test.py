from collections import Counter
from operator import itemgetter
s1 = "aaaaaaaaaaaaaaaaa"
s2 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

c1 = Counter(s1)
c2 = Counter(s2)

# znak ktory powtarza sie najwiecej razy w stringach s1 i s2

char, n = max(dict(c1+c2).items(), key=itemgetter(1))

print(char, n)