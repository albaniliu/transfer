
def isBan(yesPrice, curPrice):
  hi = curPrice + 0.01
  print abs((hi - yesPrice) / yesPrice - 0.1)
  print abs((curPrice - yesPrice) / yesPrice - 0.1)
  return abs((hi - yesPrice) / yesPrice - 0.1) > abs((curPrice - yesPrice) / yesPrice - 0.1)

def testList(l):
  l.append(1.0)

def testMap(m):
  m['a'] = 1

print isBan(86.38, 92.14)
myList = []
testList(myList)
print myList
myMap = {}
testMap(myMap)
print myMap
print len(myMap)
