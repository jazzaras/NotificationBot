import pickle

def addM(chatid):
	userData = {
		"name" : str(message.from_user.first_name),
		"chatid" : str(message.chat.id),
		"notifications" : [],
		"state" : "non",
		"holdValue" : ""
	}	

	data = Rfile()

	if str(chatid) not in data:
		data[str(chatid)] = userData

		print(data)

	with open("data.pickle", 'wb') as file:
		pickle.dump(data, file)    