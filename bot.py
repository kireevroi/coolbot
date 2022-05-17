#A funny bot for interacting with chat members
#Copyright kireevroi

#Censored version

import telebot
import re
import urllib
import random
import db
import time
import queryhandler

#main variables
TOKEN = "#####" #Private API token
bot = telebot.TeleBot(TOKEN) #The bot that is started
chats = {} #array of chats

#initializing database
database = db.db("Chatdb") #set any db name

#initializing Querylist
mylist = []
queryhandler.readQuery("QueryList.txt", mylist)

#initializing photos
def memeInit(url, name):
    f = open(name,'wb')
    f.write(urllib.request.urlopen(url).read())
    f.close()

#making super letters to normal text
def get_non_super(x):
    result = ""
    try:
        normal = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh"
                 "ijklmnopqrstuvwxyz0123456789+-=()")
        super_s = ("ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍ"
                   "ʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾")
        res = x.maketrans(''.join(super_s), ''.join(normal))
        result = x.translate(res)
    except Exception as e:
        print(e)
    return result

#making funny insertions :D
def num_to_censored(chat_id, num):
    try:
        first_insetion = ['цензор', 'мужик', 'массив', 'апдейт']
        second_insetion = ['цензора', 'мужика', 'массива', 'апдейта']
        third_insetion = ['цензоров', 'мужиков', 'массивов', 'апдейтов']
        num_res = int(num.group())
        if num_res == 300:
            pass
        else:
            if num_res%100 > 10 and num_res%100 < 20:
                if num_res == 1:
                    bot.send_message(chat_id, num.group() + ' '
                    + random.choice(first_insetion)
                    + ' тебе в что нибудь цензурное')
                elif num_res > 1 and num_res < 5:
                    bot.send_message(chat_id, num.group() + ' '
                    + random.choice(second_insetion)
                    + ' тебе в что нибудь цензурное')
                elif num_res >= 5 or num_res == 0:
                    bot.send_message(chat_id, num.group() + ' '
                    + random.choice(third_insetion)
                    + ' тебе в что нибудь цензурное')
            else:
                if num_res%10 == 1:
                    bot.send_message(chat_id, num.group() + ' '
                    + random.choice(first_insetion)
                    + ' тебе в что нибудь цензурное')
                elif num_res%10 > 1 and num_res%10 < 5:
                    bot.send_message(chat_id, num.group() + ' '
                    + random.choice(second_insetion)
                    + ' тебе в что нибудь цензурное')
                elif num_res%10 >= 5 or num_res%10 == 0:
                    bot.send_message(chat_id, num.group() + ' '
                    + random.choice(third_insetion)
                    + ' тебе в что нибудь цензурное')
    except Exception as e:
        print(e)

#sending normal message, depending on the situation
def sendcoolmsg(chat_id, text, num):
    try:
        #normal queries
        for i in range(len(mylist)):
            if(text == mylist[i][0]):
                bot.send_message(chat_id, mylist[i][1])
        #regular expression analysis
        if re.search(r'^([ха]*ха+х[ха]*|[хи]*хи+х[хи]*)(?!\S)$', text):
            bot.send_message(chat_id, 'Что смеешься, плакать надо')
        if re.search(r'кофе|чай', text):
            bot.send_message(chat_id, 'Что, культурно выпиваем? :)')
        if re.search(r'нюдс|нюдсы|нюдесы', text):
            bot.send_message(chat_id, 'Ну... Кому нибудь в ЛС, быстро.')
        #checking if number
        if num:
            num_to_censored(chat_id, num)
    except Exception as e:
        print(e)

#handlers for standard commands
@bot.message_handler(commands = ['add_token'])
def start_handler(message):
    bot.send_message(message.chat.id, '+1 token added')
#handling meme delivery
@bot.message_handler(commands = ['noice'])
def start_handler(message):
    try:
        bot.send_chat_action(message.chat.id, 'upload_photo')
        memeInit('https://noice.lol/noice.jpg', 'out.jpg')
        img = open('out.jpg', 'rb')
    except Exception as e:
        print(e)
    try:
        bot.send_photo(message.chat.id, img,
                       reply_to_message_id=message.message_id)
    except Exception:
        print('Атата, кто-то не разрешил тебе отправлять фото...')
    img.close()

#rulersize randomizer
@bot.message_handler(commands = ['rulersize'])
def start_handler(message):
    try:
        name_seq = ['Линейка', 'Длина']
        emoji_seq = ['\U0001F605','\U0001F614']
        chat_id = str(message.chat.id).replace('-', 'min')
        user = str(message.from_user.username)
        database.createTable(chat_id)
        database.addLine(chat_id, user, str(random.randint(0, 40)),
                         str(random.randint(0, 100)))
        data = database.getLine(chat_id, user) # returns a tuple
        bot.send_message(message.chat.id, random.choice(name_seq) +
                         ' у @' + user + ' *' + str(data[0]) + 'см*. ' +
                         random.choice(emoji_seq), parse_mode= 'Markdown')
    except Exception as e:
        print(e)
    deleteMsg(message.chat.id, message.message_id)

#cool randomizer
@bot.message_handler(commands = ['COOL'])
def start_handler(message):
    try:
        chat_id = str(message.chat.id).replace('-', 'min')
        user = str(message.from_user.username)
        database.createTable(chat_id)
        database.addLine(chat_id, user, str(random.randint(0, 40)),
                         str(random.randint(0, 100)))
        data = database.getLine(chat_id, user) # returns a tuple
        bot.send_message(message.chat.id, '@' + user +
                         ' сегодня красавчик на *'+str(data[1])+'%*!',
                         parse_mode= 'Markdown')
    except Exception as e:
        print(e)
    deleteMsg(message.chat.id, message.message_id)

#cool of the day intrachat
@bot.message_handler(commands = ['cooloftheday'])
def start_handler(message):
    try:
        chat_id = str(message.chat.id).replace('-', 'min')
        user = str(message.from_user.username)
        database.createTable(chat_id)
        database.addLine(chat_id, user, str(random.randint(0, 40)),
                         str(random.randint(0, 100)))
        data = database.getMax(chat_id, "COOL") # returns a tuple
        bot.send_message(message.chat.id, '@' + data[0] +
                         ' *самый красавчик* среди всех красавчиков!',
                         parse_mode= 'Markdown')
    except Exception as e:
        print(e)
    deleteMsg(message.chat.id, message.message_id)

#smallest rulersize of the day
@bot.message_handler(commands = ['smallestruler'])
def start_handler(message):
    try:
        chat_id = str(message.chat.id).replace('-', 'min')
        user = str(message.from_user.username)
        database.createTable(chat_id)
        database.addLine(chat_id, user, str(random.randint(0, 40)),
                         str(random.randint(0, 100)))
        data = database.getMin(chat_id, "RULERSIZE") # returns a tuple
        bot.send_message(message.chat.id, 'У @' + data[0] +
                         ' *самая маленькая* линейка!', parse_mode= 'Markdown')
    except Exception as e:
        print(e)
    deleteMsg(message.chat.id, message.message_id)

#droptable only for admin
@bot.message_handler(commands = ['droptable'])
def start_handler(message):
    try:
        chat_id = str(message.chat.id).replace('-', 'min')
        user = str(message.from_user.username)
        if user == 'Admin': #This is where you set the user
            database.dropTable(chat_id)
            bot.send_message(message.chat.id, 'Values dropped')
        else:
            bot.send_message(message.chat.id, 'Kids, don\'t do drugs')
    except Exception as e:
        print(e)
    deleteMsg(message.chat.id, message.message_id)

#delete messages function
def deleteMsg(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(e)

#Checking chat status, to have individual stop/start for every chat
@bot.message_handler(content_types=['text'])
def text_handler(message):
    try:
        #make the message lowercase for easier interaction
        text = message.text.lower()
        #make the text non-super, for those who wanted to escape the wrath
        text = get_non_super(text)
        #searching for standalone numbers in text
        num = re.search(r'(?<!\S)(?:-?\d+)+(?!\S)', text)
        chat_id = message.chat.id #just for ease of use
        global chats #setting global
        chats = startManager(chat_id, text, chats) #start On/off startManager
        #checking if the status is a 1 and then answering
        if chats[chat_id] == 1:
            sendcoolmsg(chat_id, text, num)
    except Exception as e:
        print(e)

#manage turning on and off chats
def startManager(chat_id, text, chat_array):
    #checking if chat is in chat list (locally, not db)
    if chat_id not in chat_array:
        chat_array[chat_id] = 1
        print(str(chat_id))
        print("Set to 1")
    #implementing local bot ON/OFF
    if chat_array[chat_id] == 0 and text == "выпускайте кракена!":
        print(str(chat_id))
        print("Set to 1")
        chat_array[chat_id] = 1
    if chat_array[chat_id] == 1 and text == "запускайте кракена!":
        print(str(chat_id))
        print("Set to 0")
        chat_array[chat_id] = 0
    #returning the array back
    return chat_array

#Start polling
bot.polling()
