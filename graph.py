#Умову задавати в EXCEEDANCE_VALUE
#Шлях до файлу в FILE_PATH
import matplotlib
import matplotlib.pyplot
import pandas

FILE_PATH = "Final Template.csv"
EXCEEDANCE_VALUE = 500              #умова перевищення витрат

data = pandas.read_csv(FILE_PATH, sep=";", encoding = "ISO-8859-1")

data["Date"] = pandas.to_datetime(data["Date"], format="%d/%m/%Y")

#print(data["Date"].dt.year)

#Отримуємо щомісячні середні значення
montlyDischarge = pandas.DataFrame({"Date": [], "Discharge": []})       #значення середніх місячних витрат

for y in data["Date"].dt.year.unique():
    yearData = data.loc[data["Date"].dt.year == y, :] #отримуємо слайс року
    #print(y)
    for m in yearData["Date"].dt.month.unique():
        monthData = yearData.loc[yearData["Date"].dt.month == m, :] #тепер слайс місяця
        sum = 0
        N = 0
        for d in monthData["Date"].dt.day:
            value = monthData.loc[monthData["Date"].dt.day == d, "Discharge"]
            sum += float(value.iloc[0])
            N += 1
        montlyDischarge.loc[len(montlyDischarge.index)] = [str(m) + "/" + str(y), sum/N]

m = 1                               #змінна рангів записів
n = len(montlyDischarge)            #кількість записів
p = []                              #ймовірності

#Рахуємо ймовірності       
m = 1
#print(montlyDischarge)
for val in montlyDischarge["Discharge"]:
    p.append(100*m/(n+1))
    m += 1

#Малюємо графік при exceedance_value = 500
montlyDischarge = montlyDischarge.sort_values("Discharge", ascending=False, ignore_index=True) #сортуємо за спаданням

matplotlib.pyplot.plot(p, montlyDischarge["Discharge"])
matplotlib.pyplot.legend(['Щомісячні витрати води, м³/с'], fontsize=14) 
matplotlib.pyplot.tick_params(labelsize=14)

x1 = 0
x2 = 100

y = EXCEEDANCE_VALUE

y3 = montlyDischarge["Discharge"][montlyDischarge["Discharge"] > EXCEEDANCE_VALUE].min()
y4 = montlyDischarge["Discharge"][montlyDischarge["Discharge"] < EXCEEDANCE_VALUE].max()

x3 = p[montlyDischarge["Discharge"].index[montlyDischarge["Discharge"] == y3].to_list()[0]]
x4 = p[montlyDischarge["Discharge"].index[montlyDischarge["Discharge"] == y4].to_list()[0]]

#print(x3)
#print(x4)

#print(y3)
#print(y4)

p1 = ((x1*y-y*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y-y)*(x3-x4))
p2 = ((x1*y-y*x2)*(y3-y4)-(y-y)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y-y)*(x3-x4))

#print(p1, p2)

matplotlib.pyplot.hlines(y = EXCEEDANCE_VALUE, xmin = 0, xmax = p1, color = 'r', linestyle = 'dashed')
matplotlib.pyplot.vlines(x = p1, ymin = 0, ymax = p2, color = 'r', linestyle = 'dashed')

matplotlib.pyplot.plot(p1, EXCEEDANCE_VALUE, marker="o", markersize=6, markeredgecolor='r', markerfacecolor='r')

matplotlib.pyplot.yticks([0,250,500,750,1000,montlyDischarge["Discharge"].max(),EXCEEDANCE_VALUE])
matplotlib.pyplot.xticks([0,20,40,60,80,100,p1])

font = {'size':14}
fontT = {'size':20}

matplotlib.pyplot.annotate(str(round(p1, 1)) +"%", (p1+0.5, EXCEEDANCE_VALUE+10), fontsize=14)
matplotlib.pyplot.title("Ймовірність перевищення щомісячних витрат води позначки " + str(EXCEEDANCE_VALUE) +" м³/с.",fontdict=fontT)
matplotlib.pyplot.xlabel("Ймовірність, %",fontdict=font)
matplotlib.pyplot.ylabel("Витрати води, м³/с",fontdict=font)

matplotlib.pyplot.show()