import pandas

n = 432
val = range(0, n)
val = pandas.DataFrame(val)
m = 1
p = []

for v in val:
    p.append(100*m/(n+1))
    print(m)
    m += 1

y = 250

y3 = val[val > y].min()
y4 = val[val < y].max()

indexP = pandas.Index(val[0])

print(val.iloc(y3))

print(y3)
print(y4)

