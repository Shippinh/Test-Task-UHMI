# type: ignore 

#Перший рядок (коментар вище) - через тех причини. Основний комп зараз в сервісі, а на цьому ноуті - все шкереберть. З правильними дозволами його можна прибрати.

#Функцію parse_xlsx() можна приховати, шлях до файлу вказується в FILE_PATH.

#Дану програму ще довго можна вдосконалювати, але зараз вона повністю виконує завдання в контексті поданих таблиць, 
#при цьому таблиці жодним чином не було модифіковано до початку роботи.

#В зв'язку з цим останній лист таблиці в цій програмі ігнорується.
import pandas

def parse_xlsx(filePath):
     #Рядкова відстань між останнім записом таблиці та першим записом наступної
     nextTableRow = 52
     
     #Рядки які відступаємо до наступної табл.
     rowSkip = 0

     #Місцезнаходження даних
     dayStartRows = range(4, 35)
     monthStartCols = range(1, 13)

     #Місцезнаходження першого запису в таблиці
     currentCol = 1
     currentRow = 4

     #DO WHILE START
     data = pandas.ExcelFile(filePath)
     sheets = data.sheet_names
     sheetCount = 0

     data = pandas.read_excel(filePath, header=None, sheet_name=sheets[sheetCount])

     #print(data)
     newData = {}

     i = 0
     for key in data:
          newData[i] = data[key]
          #print(newData[i])
          i += 1

     stri = ""
     stri += "Date;Discharge\n"
     defaultFileLength = len(stri)

     #print(len(newData[0]))
     rowLimit = len(newData[0])

     while newData[currentCol][currentRow] != "nan":
          if(sheetCount == len(sheets)-1):
               break
          i = 0
          while isinstance(newData[currentCol+11][currentRow-i], str) == False:
               i += 1
          yearDate = newData[currentCol+11][currentRow-i][-4:]#зробити динамічний відступ, тобто будемо спускатися доки не знайдемо текст
          #print("\n" + str(yearDate) + "\n")
          #print("i = " + str(i-4))
          lowRow = i - 4
          for month in monthStartCols:
               monthDate = month
               #print("\n" + str(monthDate) + "\n")
               for day in dayStartRows:
                    dayDate = day-3
                    stri += str(dayDate) + "/" + str(monthDate) + "/" + str(yearDate) + ";" + str(newData[month][day+rowSkip-lowRow]) + "\n"
                    #print(str(dayDate) + "/" + str(monthDate) + "/" + str(yearDate) + ";" + str(newData[month][day+rowSkip-lowRow]) + "\n")
                    #print(dayDate)
          if(currentRow + nextTableRow < rowLimit):
               currentRow += nextTableRow
               rowSkip += nextTableRow
               #print(currentRow)
          else:
               sheetCount += 1
               data = pandas.read_excel(filePath, header=None, sheet_name=sheets[sheetCount])
               currentCol = 1
               currentRow = 4
               rowSkip = 0
               newData = {}
               i = 0
               for key in data:
                    newData[i] = data[key]
                    #print(newData[i])
                    i += 1
               rowLimit = len(newData[0])
     if defaultFileLength < len(stri):
          print("Trimming 'nan' values.")
          stri = "\n".join(x for x in stri.splitlines() if "nan" not in x)
          stri = "\n".join(x for x in stri.splitlines() if "нн" not in x) #тимчасовий фікс, краще перевіряти чи можна конвертувати в float (запис за 15/10/2004)

          print("Saving data...")
          file = open("Final Template.csv", "w")
          file.write(stri)
          file.close()

          print("Successfully saved data in the 'Final Template.csv' file.")
     else:
          print("No data found in xlsx file.")

FILE_PATH = "data.xlsx"
parse_xlsx(FILE_PATH)