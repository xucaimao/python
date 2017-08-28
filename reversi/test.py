import random,sys
reverslist=[]
a=[]
for p in range(2):
    for i in range(random.randint(1,5)):
        a.append([random.randint(0,7),random.randint(0,7)])
    print(a)
    reverslist.append(a)
print(len(reverslist))

print(reverslist)

while reverslist:
    reverslist.pop()

print(len(reverslist))

print(reverslist)