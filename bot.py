import telebot
import time
import pandas
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import json
from datetime import datetime

# IDI is the id index and time index and so on... it is the user index when all values are in a list
# excelIndex on the other hand is the row in excel file in which the user information are in

BOT_TOKEN = "5795294189:AAEmDCQ9t0SmznafZEBP-Ivrc7HS2IDZW8I"


filename = 'data.xlsx'

bot = telebot.TeleBot(BOT_TOKEN)
days = ['sun', 'mon', 'tue', 'wed', 'Thu', 'fri', 'sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def firstEmptyRow():

    df = pandas.read_excel(filename, sheet_name='main')
    
    ids =  df['Chatid'].tolist()

    firstEmpytCell = len(ids)+2

    for i in range(len(ids)):
        
        id_ = str(ids[i]) 


        if id_ == "nan":
            firstEmpytCell = i+2
            return firstEmpytCell

    return firstEmpytCell

def FindingIDIndex(Chatid):

    df = pandas.read_excel(filename, sheet_name='main')
    
    ids =  df['Chatid'].tolist()

    cell = len(ids) -1

    for i in range(len(ids)):
        
        id_ = str(ids[i])


        if id_ == Chatid:
            cell = i
            return (cell)
    return (cell)    

def addNotification(Chatid, Day ,Time):

	df = pandas.read_excel(filename, sheet_name='main')
	wb = load_workbook(filename)
	ws = wb.worksheets[0]

	IDI = FindingIDIndex(Chatid)

	times =  df['Time'].tolist()
	userTimes = times[IDI] # type = str
	userTimes = userTimes.replace("[", "")
	userTimes = userTimes.replace("]", "")
	userTimes = userTimes.replace("'", "")
	userTimes = userTimes.split(",")
	userTimes = [time.strip() for time in userTimes]
	# userTimes = json.loads(userTimes) # type = list

	
	days = df['Day'].tolist()
	userDays = days[IDI] # type = str
	userDays = userDays.replace("[", "")
	userDays = userDays.replace("]", "")
	userDays = userDays.replace("'", "")
	userDays = userDays.split(",")
	userDays = [Day.strip() for Day in userDays]

	# userDays = json.loads(userDays) # type = list  

	exelIndex = IDI + 2

	# for i in userTimes:
	# 	if i == '':
	# 		userTimes.remove(i)

	# for i in userDays:
	# 	if i == '':
	# 		userDays.remove(i)


	posDAY = 'B' + str(exelIndex)
	posTIME = 'C' + str(exelIndex)
	posSTATE = 'E' + str(exelIndex)
	posHOLD = 'F' + str(exelIndex)
	
	print(Time)
	userTimes.append(Time)
	userTimes = str(userTimes)

	userDays.append(Day)
	userDays = str(userDays)

	ws[posDAY] = userDays
	ws[posTIME] = userTimes
	ws[posSTATE] = "sce"	
	ws[posHOLD] = "nothing"


	wb.save(filename)







@bot.message_handler(commands=["start", "help"])
def welcome(message):
	bot.send_message(message.chat.id, "welcome to the graetest bot ever made")

	df = pandas.read_excel(filename, sheet_name='main')
	wb = load_workbook(filename)
	ws = wb.worksheets[0]

	if message.chat.id in df['Chatid'].tolist():
		print("in system")
		return


	FER = firstEmptyRow()

	posID = 'A' + str(FER)
	posDAY = 'B' + str(FER)
	posTIME = 'C' + str(FER)
	posDONE = 'D' + str(FER)
	posSTATE = 'E' + str(FER)
	posHOLD = 'F' + str(FER)


	ws[posID] = message.chat.id
	ws[posDONE] = False
	ws[posDAY] = "[]"
	ws[posTIME] = "[]"	
	ws[posSTATE] = "non"
	ws[posHOLD] = "nothing"

	wb.save(filename)	

@bot.message_handler(commands=["add" , "Add"])
def adding(message):

	df = pandas.read_excel(filename, sheet_name='main')
	wb = load_workbook(filename)
	ws = wb.worksheets[0]
	
	IDI = FindingIDIndex(message.chat.id)
	exelIndex = IDI + 2
	
	posSTATE = 'E' + str(exelIndex)

	bot.send_message(message.chat.id, "at what day is you lecture(Sun / Mon / Tue / Wed / Thu / Fri / Sat)")
	
	ws[posSTATE] = 'waitingForDay'
	wb.save(filename)


	
@bot.message_handler()
def general(message):
	
	mes = (str(message.text)).strip()

	df = pandas.read_excel(filename, sheet_name='main')
	wb = load_workbook(filename)
	ws = wb.worksheets[0]

	IDI = FindingIDIndex(message.chat.id)
	exelIndex = IDI + 2

	posSTATE = 'E' + str(exelIndex)
	posHOLD = 'F' + str(exelIndex)


	states = df["State"].tolist()
	userStat = states[IDI]

	holdValues = df["Hold"].tolist()
	userHoldValue = holdValues[IDI]	


	if (userStat == "non") or (userStat == "sce"):
		bot.reply_to(message, "Enter a command")
	
	elif userStat == "waitingForDay":
		if mes in days:
			ws[posHOLD] = mes
			ws[posSTATE] = 'waitingForTime'
			wb.save(filename)
			bot.reply_to(message, "good, now enter a time ex.(14:59,, 09:12, 15:02)")
		else:
			bot.reply_to(message, "not a valid Day")
	
	elif userStat == "waitingForTime":

		timeFor = mes.replace(":", "")

		try:
		    datetime.strptime(timeFor, '%H%M')
		    valid = True
		except ValueError:
		    valid = False

		if valid and len(mes) == 5 and mes[2] == ":" and (mes[0] in numbers) and (mes[1] in numbers) and (mes[3] in numbers) and (mes[4] in numbers):
			day = userHoldValue 
			addNotification(message.chat.id, day, mes)
			bot.reply_to(message, "Perfect... your notification has been added")
			
		else:
			bot.reply_to(message, "not a valid Time")
			bot.send_message(message.chat.id, "enter a time ex.(14:59,, 09:12, 15:02)")






bot.polling()

