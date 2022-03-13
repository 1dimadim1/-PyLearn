import requests
import telebot

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from collections import Counter

bot = telebot.TeleBot('5015716211:AAGNmfZzVpGeG5ITB3ZNVIWGFi1wa3kC_zg')
calc_val = 0
calc_val2 = 0
operator = ""

mystem = Mystem()
russian_stopwords = stopwords.words("russian")
english_stopwords = stopwords.words("english")

def build_keyboard():
    keyboard = [
    [
        telebot.types.InlineKeyboardButton("1", callback_data='key:1'),
        telebot.types.InlineKeyboardButton("2", callback_data='key:2'),
        telebot.types.InlineKeyboardButton("3", callback_data='key:3')
    ],
    [
        telebot.types.InlineKeyboardButton("4", callback_data='key:4'),
        telebot.types.InlineKeyboardButton("5", callback_data='key:5'),
        telebot.types.InlineKeyboardButton("6", callback_data='key:6')
    ],
    [
        telebot.types.InlineKeyboardButton("7", callback_data='key:7'),
        telebot.types.InlineKeyboardButton("8", callback_data='key:8'),
        telebot.types.InlineKeyboardButton("9", callback_data='key:9')
    ],
    [
        telebot.types.InlineKeyboardButton("<=", callback_data='back_operator'),
        telebot.types.InlineKeyboardButton("0", callback_data='key:0'),
        telebot.types.InlineKeyboardButton("=", callback_data='final')
    ]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

def build_operator():
    keyboard = [
    [
        telebot.types.InlineKeyboardButton("*", callback_data='operation*'),
        telebot.types.InlineKeyboardButton("-", callback_data='operation-'),
        telebot.types.InlineKeyboardButton("+", callback_data='operation+')
    ],
    [
        telebot.types.InlineKeyboardButton("<=", callback_data='back_keyboard'),
        telebot.types.InlineKeyboardButton("/", callback_data='operation/'),
        telebot.types.InlineKeyboardButton("^", callback_data='operation^')
    ]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup
def show_calc(user_id, func):
        keyboard = telebot.types.InlineKeyboardMarkup()
        if len(operator) > 0:
            bot.send_message(user_id, text="=" + str(calc_val) + operator + str(calc_val2), reply_markup=func)           
        else:
            bot.send_message(user_id, text="=" + str(calc_val), reply_markup=func)

def calcVal(first, second, operator):
    if operator == '*':
        return first * second
    elif operator == '/':
        return first / second
    elif operator == '-':
        return first - second
    elif operator == '+':
        return first + second    
    elif operator == '^':
        return first ** second
    else:
        return 0

def checkSite(url, user_id):
    try:
        response = requests.get(url) 
        if response.status_code == 200: 
            bot.send_message(user_id,'Site avaliable!') 
        else:         
            bot.send_message(user_id,'Does it exist? Site unavaliable')
    except:
         bot.send_message(user_id,'Is it even a site?')

def TokenizeLem(words):
    new_punctuation = punctuation + '—'
    tokens = mystem.lemmatize(words.lower())
    tokens = [token for token in tokens if token not in russian_stopwords\
             and token not in english_stopwords\
             and token != " "\
             and token.strip() not in new_punctuation]
    return tokens
def countParagraphs(words):
    possible_par = words.split('.')
    paragraphs = 0
    for par in possible_par:
        if par.strip()[:1].isupper():
            paragraphs+=1
    return paragraphs
def MostLong(tokens):
    long_word = ""
    for word in tokens:
        if len(word) > len(long_word):
            long_word = word
    return long_word
    
def checkWords(words, user_id):
    try:
        bot.send_message(user_id,"Amount of paragraphs: " + str(countParagraphs(words)))
        tokens = TokenizeLem(words)
        bot.send_message(user_id,"Most long word: " + MostLong(tokens))
        counts = Counter(tokens)
#         output = ""
#         for key, count in counts.items():
#             output += key+ ":" + str(count) + ", "
#         bot.send_message(user_id,output) 
        bot.send_message(user_id,"Amount of uniq word: " + str(len(counts)))
        key_max = max(counts, key=counts.get)
        bot.send_message(user_id,f"Most popular word: {key_max} ({counts[key_max]} times)")
    except:
        bot.send_message(user_id,'Something went wrong')



@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global operator
    global calc_val
    global calc_val2
    if ':' in call.data:
        number = int(call.data[-1:])
        if len(operator) > 0:
            calc_val2 = calc_val2 * 10 + number
        else:
            calc_val = calc_val * 10 + number
        show_calc(call.message.chat.id, build_keyboard()) 
    elif 'back' in call.data:
        if 'operator' in call.data:
            calc_val2 = 0
            show_calc(call.message.chat.id, build_operator()) 
        else:
            show_calc(call.message.chat.id, build_keyboard()) 
    elif 'operation' in call.data:
        operator = call.data[-1:]
        show_calc(call.message.chat.id, build_keyboard()) 
    elif 'final' == call.data:
        try:
            calc_val = calcVal(calc_val, calc_val2, operator)
            operator = ""
            show_calc(call.message.chat.id, build_keyboard())             
        except:
            bot.send_message(call.message.chat.id,'Something broke')
        
        

@bot.message_handler(commands=['menu'])
def getChoise(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    itembtn1 = telebot.types.KeyboardButton("/site")
    itembtn2 = telebot.types.KeyboardButton('/words')
    itembtn3 = telebot.types.KeyboardButton('/calc')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Choose an action:", reply_markup=markup)
        
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    u_id = message.from_user.id
    if message.text == "/start":
        bot.send_message(u_id, "Oh Hi Mark (please, type /menu)")
    elif message.text == "/help":
        bot.send_message(u_id, "/menu - to choose functional")
    elif message.text == "/calc":
        show_calc(u_id, build_keyboard())
    elif "/site" in message.text:
        parsed_m = message.text.split()
        if len(parsed_m) != 2:
            bot.send_message(u_id, "/site url_of_site - for check site are avaliable")
        else:            
            checkSite(message.text[6:],u_id)           
    elif "/words" in message.text:   
        parsed_m = message.text.split()     
        if len(parsed_m) < 2:
            bot.send_message(message.from_user.id, "/words some words - for check words stat")
        else:            
            checkWords(message.text[7:],u_id) 



bot.polling(non_stop=True, interval=0)