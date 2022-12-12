import telebot
import time as thetime
import pandas
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import json
from datetime import datetime
import threading
import os

# IDI is the id index and time index and so on... it is the user index when all values are in a list
# excelIndex on the other hand is the row in excel file in which the user information are in

BOT_TOKEN = "5795294189:AAEmDCQ9t0SmznafZEBP-Ivrc7HS2IDZW8I"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
filename = 'data.xlsx'
path = os.path.join(BASE_DIR, filename)

bot = telebot.TeleBot(BOT_TOKEN)
days = ['sun', 'mon', 'tue', 'wed', 'Thu', 'fri', 'sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def stringToList(StringinListFormat):
	theList = StringinListFormat.replace("[", "")
	theList = theList.replace("]", "")
	theList = theList.replace("'", "")
	theList = theList.split(",")
	theList = [item.strip() for item in theList]
	return theList

def clear(Chatid):

	df = pandas.read_excel(filename, sheet_name='main')
	wb = load_workbook(filename)
	ws = wb.worksheets[0]

	exelIndex = (FindingIDIndex(Chatid) + 2)

	posDAY = 'B' + str(exelIndex)
	posTIME = 'C' + str(exelIndex)
	posDONE = 'D' + str(exelIndex)
	posSTATE = 'E' + str(exelIndex)
	posHOLD = 'F' + str(exelIndex)	



	ws[posTIME] = "[]"
	ws[posDAY] = "[]"
	ws[posDONE] = "[]"
	ws[posSTATE] = "non"
	ws[posHOLD] = "nothing"

	wb.save(filename)

# a function that loops through our excel file and send messages if time, day is now
def checkingNotification():
	
	while True:

		thetime.sleep(10)

		df = pandas.read_excel(filename, sheet_name='main')
		wb = load_workbook(filename)
		ws = wb.worksheets[0]


		# Getting information from excel sheet
		ids = df['Chatid'].tolist()
		day = df['Day'].tolist()
		time = df['Time'].tolist()	
		done = df['Done'].tolist()

		# Getting times and dates
		current = datetime.now()
		dayName = current.strftime('%a').lower()
		currentTime = current.strftime("%H:%M")






		# loop for x times --> x is the number of ids
		for i in range(len(ids)):

			userdays = stringToList(day[i])
			usertimes = stringToList(time[i])
			userdones = stringToList(done[i]) 

			for x in range(len(userdays)):
				if dayName == userdays[x]:
					if currentTime == usertimes[x]:
						if userdones[x] == "False":
							# Send Noti0fication

							bot.send_message(ids[i], "you have a class now")

							# Set Done (one item in the list) to True --> so it will not go in the if statment for a whole minute
							cell = "D" + str(i+2)
							userdones[x] = "True"
							ws[cell] = str(userdones)
							wb.save(filename)

							print("sent")


						
		# Reset ALL Done boolean variables in excel				
		
		if currentTime == "00:00":
			
			for i in range(len(ids)):
				userdones = stringToList(done[i])
				print(userdones)
				cell = "D" + str(i+2)								 
				for x in range(userdones[i]):

					userdones[x] = "False"

				ws[cell] = str(userdones)
				wb.save(filename)

			print("cleared all dones")


### making a thread so that the bot thread will not be disturbed by our checking loop
check = threading.Thread(target=checkingNotification)


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

		# print(id_, Chatid)

        if id_ == str(Chatid):
            cell = i
            return (cell)
    return (cell)    



def addNotification(Chatid, Day ,Time):

	df = pandas.read_excel(filename, sheet_name='main')
	wb = load_workbook(filename)
	ws = wb.worksheets[0]
	
	IDI = FindingIDIndex(Chatid)

	Day = Day.lower()

	times =  df['Time'].tolist()
	userTimes = stringToList(times[IDI]) # type = str

	# userTimes = json.loads(userTimes) # type = list

	
	days = df['Day'].tolist()
	userDays = stringToList(days[IDI]) # type = str

	dones = df['Done'].tolist()
	userDones = stringToList(dones[IDI])

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
	posDONE = 'D' + str(exelIndex)
	posSTATE = 'E' + str(exelIndex)
	posHOLD = 'F' + str(exelIndex)
	
	userTimes.append(Time)
	userTimes = str(userTimes)

	userDays.append(Day)
	userDays = str(userDays)

	userDones.append('False')
	userDones = str(userDones)


	ws[posDAY] = userDays
	ws[posTIME] = userTimes
	ws[posDONE] = userDones
	ws[posSTATE] = "sce"	
	ws[posHOLD] = "nothing"


	wb.save(filename)







@bot.message_handler(commands=["start", "help"])
def welcome(message):
	bot.send_message(message.chat.id, f"hay {message.from_user.first_name} \n welcome to the graetest bot ever made")
	bot.send_message(message.chat.id, "commamds: \n /add ==> to add weekly notifications \n /clear ==> to clear all notifictions")

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
	ws[posDONE] = "[]"
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

@bot.message_handler(commands=["clear", "Clear"])
def clearing(message):

	clear(message.chat.id)

	bot.send_message(message.chat.id, "Done... All notifications where deleted")


	
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

	# print(states, IDI)

	userStat = states[IDI]

	holdValues = df["Hold"].tolist()
	userHoldValue = holdValues[IDI]	

	# print(userStat)

	if (userStat == "non") or (userStat == "sce"):
		if message.text == "hay" or message.text == "Hay":
			print(message)
			bot.reply_to(message, "Hello")
		else:
			bot.reply_to(message, "I did not understand...\n you can ask for /help if your lost \n or you can say hay...")
	
	elif userStat == "waitingForDay":
		if mes in days:
			ws[posHOLD] = mes
			ws[posSTATE] = 'waitingForTime'
			wb.save(filename)
			bot.reply_to(message, "good, now enter a time in 24H Format ex.(14:59,, 09:12, 15:02)")
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
			bot.reply_to(message, "not a valid Time \nmake sure you enter Time with zeros.. ex: \n 01:20")




check.start()

while True:
    try:
        bot.polling(non_stop=True, interval=0)
    except Exception as e:
        print("error: ", e)
        thetime.sleep(5)
        continue

