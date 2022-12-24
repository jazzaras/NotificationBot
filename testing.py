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

# # IDI is the id index and time index and so on... it is the user index when all values are in a list
# # excelIndex on the other hand is the row in excel file in which the user information are in


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# filename = 'data.xlsx'
# path = os.path.join(BASE_DIR, filename)

# bot = telebot.TeleBot(BOT_TOKEN)
# days = ['sun', 'mon', 'tue', 'wed', 'Thu', 'fri', 'sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
# numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


# def Rfile():
# 	with open("data.pickle", "rb") as file:
# 		data = pickle.load(file)
# 	return data
# def checkingNotification():
	
# 	while True:

# 		# Getting times and dates
# 		current = datetime.now()
# 		dayName = current.strftime('%a').lower()
# 		currentTime = current.strftime("%H:%M")


# 		# gitting data

# 		data = Rfile()



# 		# loop for x times --> x is the number of ids

# 		for chatid in data:
# 			for notification in data[chatid]['notifications']:
# 				if notification[0] == dayName:
# 					if notification[1] == currentTime:
# 						if notification[2] == False:
# 							notification[2] = True
# 							with open("data.pickle", "wb") as file:
# 								pickle.dump(data, file)
# 							bot.send_message(chatid, "you have a class now")
# 							print(f"sent to {data[chatid]['name']}")



						
# 		# Reset ALL Done boolean variables in excel				
		
# 		if currentTime == "00:00":
			
# 			for chatid in data:
# 				for notification in data[chatid]['notifications']:
# 					notification[2] = False	


# 			with open("data.pickle", 'wb') as file:
# 				pickle.dump(data, file)
# 			print("cleared all dones")
# 			print(data)	
# 		time.sleep(10)


# checkingNotification()

with open("data.pickle", "wb") as file:
	pickle.dump({}, file)

with open("data.pickle", "rb") as file:
	print(pickle.load(file))

