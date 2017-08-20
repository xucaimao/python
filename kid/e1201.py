names=[]
print("Enter 5 names:")
for i in range(5):
    names.append(input())

print("The names are",end=" ")
for na in names:
    print(na,end=" ")
print()

names.sort()
print("After sorted,The names are",end=" ")
for na in names:
    print(na,end=" ")
print()

