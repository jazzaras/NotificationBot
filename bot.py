import telebot
import time
import pandas
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import json
from datetime import datetime
import threading
import os
import pickle
import pytz


# IDI is the id index and time index and so on... it is the user index when all values are in a list
# excelIndex on the other hand is the row in excel file in which the user information are in

BOT_TOKEN = "enter your bot token here"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
filename = 'data.xlsx'
path = os.path.join(BASE_DIR, filename)

bot = telebot.TeleBot(BOT_TOKEN)
days = ['sun', 'mon', 'tue', 'wed', 'Thu', 'fri', 'sat', 'Sun', 'Mon', 'Tue', 'Wed', 'thu', 'Fri', 'Sat']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


tz = pytz.timezone("Asia/Riyadh")



def stringToList(StringinListFormat):
	theList = StringinListFormat.replace("[", "")
	theList = theList.replace("]", "")
	theList = theList.replace("'", "")
	theList = theList.split(",")
	theList = [item.strip() for item in theList]
	return theList

#  function that will reset state and holdValue
def cancel(chatid):
	
	data = Rfile()
	data[str(chatid)]['state'] = 'non'
	data[str(chatid)]['holdValue'] = ''

	return data

def getFull(shortcut):
	if shortcut == 'sat':
		return 'Saturday'
	elif shortcut == 'sun':
		return 'Sunday'
	elif shortcut == 'mon':
		return 'Monday'
	elif shortcut == 'tue':
		return 'Tuesday'
	elif shortcut == 'wed':
		return 'Wednesday'
	elif shortcut == 'thu':
		return 'Thursday'
	elif shortcut == 'fri':
		return 'Friday'

def clear(chatid):

	data = Rfile()	

	data[str(chatid)]['notifications'] = []
	
	with open("data.pickle", 'wb') as file:
		pickle.dump(data, file)	 

def addUserM(message):
	userData = {
		"name" : str(message.from_user.first_name),
		"chatid" : str(message.chat.id),
		"notifications" : [],
		"state" : "non",
		"holdValue" : ""
	}	

	data = Rfile()

	if str(message.chat.id) not in data:
		data[str(message.chat.id)] = userData

		print(data)

	with open("data.pickle", 'wb') as file:
		pickle.dump(data, file)    

# a function that loops through our excel file and send messages if time, day is now
def checkingNotification():
	
	while True:

		# Getting times and dates
		current = datetime.now()
		dayName = current.strftime('%a').lower()
		currentTime = current.strftime("%H:%M")


		# gitting data

		data = Rfile()



		# loop for x times --> x is the number of ids

		for chatid in data:
			for notification in data[chatid]['notifications']:
				if notification[0] == dayName:
					if notification[1] == currentTime:
						if notification[2] == False:
							notification[2] = True
							with open("data.pickle", "wb") as file:
								pickle.dump(data, file)
							bot.send_message(chatid, "you have a class now")
							print(f"sent to {data[chatid]['name']}")



						
		# Reset ALL Done boolean variables in excel				
		
		if currentTime == "00:00":
			
			for chatid in data:
				for notification in data[chatid]['notifications']:
					notification[2] = False	


			with open("data.pickle", 'wb') as file:
				pickle.dump(data, file)
			print("cleared all dones")
			print(data)	
		time.sleep(10)

## making a thread so that the bot thread will not be disturbed by our checking loop
check = threading.Thread(target=checkingNotification)



def addNotification(chatid, Day ,Time):


	data = Rfile()

	Day = Day.lower()	
	chatid = str(chatid)


	notification = [Day, Time, False]

	data[chatid]["notifications"].append(notification)
	data[chatid]["state"] = 'sce'
	data[chatid]["holdValue"] = ''

	print("added")
	return data


def Rfile():
	try:
		with open("data.pickle", "rb") as file:
			data = pickle.load(file)
		return data	
	except:
		print("err ocurd")
		return "err"



@bot.message_handler(commands=["start", "help"])
def welcome(message):
	bot.send_message(message.chat.id, f"hay {message.from_user.first_name} \n welcome to the graetest bot ever made")
	bot.send_message(message.chat.id, "commamds: \n /Add ==> to add weekly notifications \n /Show ==> to show all notifications \n /Clear ==> to clear all notifictions \n /Contact ==> to contact the developer")

	userData = {
		"name" : str(message.from_user.first_name),
		"chatid" : str(message.chat.id),
		"notifications" : [],
		"state" : "non",
		"holdValue" : ""
	}	

	data = Rfile()

	if str(message.chat.id) not in data:
		data[str(message.chat.id)] = userData

		print(data)

	with open("data.pickle", 'wb') as file:
		pickle.dump(data, file)



		
@bot.message_handler(commands=["add" , "Add"])
def adding(message):

	data = Rfile()

	if str(message.chat.id) not in data:
		addUserM(message)
		data = Rfile()	


	data[(str(message.chat.id))]["state"]  = "waitingForDay"


	with open("data.pickle", "wb") as file:
		pickle.dump(data, file)

	bot.send_message(message.chat.id, "at what day is you lecture(Sun / Mon / Tue / Wed / Thu / Fri / Sat)")
	

@bot.message_handler(commands=["clear", "Clear"])
def clearing(message):

	data = Rfile()

	if str(message.chat.id) not in data:
		addUserM(message)
		data = Rfile()	

	clear(message.chat.id)

	bot.send_message(message.chat.id, "Done... All notifications where deleted")

@bot.message_handler(commands=["show", "Show"])
def show(message):
	
	data = Rfile()

	if str(message.chat.id) not in data:
		addUserM(message)
		data = Rfile()	
	
	notifications = data[str(message.chat.id)]['notifications']

	if notifications == []:
		bot.send_message(message.chat.id, "You don't have any notifications yet")
		return

	notificationsMessage = 'you have a notifiction on: \n'
	for notification in notifications:
		notificationsMessage += f'{getFull(notification[0])} at {notification[1]} \n' 

	bot.send_message(message.chat.id, notificationsMessage)
@bot.message_handler(commands=["contact", "Contact"])
def contact(message):

	data = Rfile()

	if str(message.chat.id) not in data:
		addUserM(message)
		data = Rfile()		
	#replace my username with yours
	bot.send_message(message.chat.id, "@jazzaras")	
	
@bot.message_handler()
def general(message):
	
	mes = (str(message.text)).strip()

	data = Rfile()

	if str(message.chat.id) not in data:
		addUserM(message)
		data = Rfile()
		print("was not in data")	

	if data == "err":
		return

	state = data[str(message.chat.id)]["state"]


	holdValue = data[str(message.chat.id)]["holdValue"]


	if (state == "non") or (state == "sce"):
		if message.text == "hay" or message.text == "Hay":
			print(message)
			bot.reply_to(message, f"Hello {message.from_user.first_name}")
		else:
			bot.reply_to(message, "I did not understand...\n you can ask for /help if your lost \n or you can say hay...")
	
	elif state == "waitingForDay":
		if mes in days:
			data[str(message.chat.id)]["holdValue"] = mes
			data[str(message.chat.id)]["state"] = "waitingForTime"
			bot.reply_to(message, "good, now enter a time in 24H Format ex.(14:59,, 09:12, 15:02)")
		elif mes == 'cancel':
			data = cancel(message.chat.id)
			bot.reply_to(message, "ok")
		else:
			bot.reply_to(message, "not a valid Day\nto cancel --> send 'cancel'")
	
	elif state == "waitingForTime":

		timeFor = mes.replace(":", "")

		try:
		    datetime.strptime(timeFor, '%H%M')
		    valid = True
		except ValueError:
		    valid = False

		if valid and len(mes) == 5 and mes[2] == ":" and (mes[0] in numbers) and (mes[1] in numbers) and (mes[3] in numbers) and (mes[4] in numbers):
			day = holdValue 
			data = addNotification(message.chat.id, day, mes)
			bot.reply_to(message, "Perfect... your notification has been added")
		elif mes == 'cancel':
			data = cancel(message.chat.id)
			bot.reply_to(message, "ok")		
		else:
			bot.reply_to(message, "not a valid Time \nmake sure you enter Time with zeros.. ex: \n 01:20\nto cancel --> send 'cancel'")

	with open("data.pickle", "wb") as file:
		pickle.dump(data, file)


check.start()

# while True:
#     try:
#         bot.polling(non_stop=True, interval=0)
#     except Exception as e:
#         print("error: ", e)
#         time.sleep(5)
#         continue

bot.polling()
