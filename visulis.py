import seaborn as sns
import pickle
with open(r"C:\Users\jazza\Desktop\data (2).pickle", 'rb') as file:
    data = pickle.load(file)

# print(data)

# print('Chatid', 'Name',  'State', 'Notifications', sep='         ')

data['43532454643634'] = {"hay"}

longestChatId = 0


for i in data:
    if len(i) > longestChatId:
        longestChatId = len(i)


for user in data:
    # print(user)

    range(len(list(data[user])))

    for i in range(len(list(data[user]))):

        longestitemLen = 0

        for j in data:
            if len(j) > longestitemLen:
                longestitemLen = len(j)

        user1 = list(data[user].values())
        
        # print(user1)

        item = user1[i]

        # print(item)

        spaces = (((longestitemLen)) - len(user1[(i)])) + 5

        # print(spaces)

        print(item, end=spaces*' ')

    print('')

    # print(data[user]['chatid'], data[user]['name'], (data[user]['state']), (data[user]['notifications']))