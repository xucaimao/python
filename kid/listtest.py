la=[]
for i in range(10):
    la.append(i)
print(la)

for i in range(10):
    t=la.pop(0)
    la.append(t)
    print(la)