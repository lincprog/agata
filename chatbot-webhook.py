# -*- coding: utf-8 -*-
"""

Script principal da ÁGATA.

Responsável por realizar a conexão com o banco de dados, setar a url da hospedagem e por gerenciar as respostas do chatbot sempre que uma interação ocorrer.

Baseado no pyTelegramBotAPI (https://github.com/eternnoir/pyTelegramBotAPI)

"""

from agentbot import fetch_reply
from operationsdb import createUser, createConversation, searchUserByFromId
import telebot
from telebot import types
from flask import Flask, request
import os
import pymysql

connection = pymysql.connect(
    host = 'host',
    user = 'user',
    password = 'password',
    database = 'database'
)

cursor = connection.cursor() 

TOKEN = "SEU_TOKEN_AQUI"
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)
        
@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    # if the connection was lost, then it reconnects
    connection.ping(reconnect=True)    
    
    if searchUserByFromId(message.from_user.id, cursor) == False:
        createUser(message.from_user.first_name, message.from_user.last_name, message.from_user.id, cursor, connection)
    bot_responses = fetch_reply(message.text, message.from_user.id)
    for response in bot_responses:
        if response.text.text[0] == "":
            response.text.text[0] = "Desculpe, não entendi! :("
            bot.send_message(message.chat.id, response.text.text[0])
        else:
            bot.send_message(message.chat.id, response.text.text[0])
        createConversation(message.from_user.id, message.text, response.text.text[0], message.date, cursor, connection)
    
@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    # if the connection was lost, then it reconnects
    connection.ping(reconnect=True) 
    bot.reply_to(message, 'Digite "menu" para ver as opções disponíveis :)')

@bot.message_handler(content_types=['text'])
def send_reply(message):
    # if the connection was lost, then it reconnects
    connection.ping(reconnect=True) 
    bot_responses = fetch_reply(message.text, message.from_user.id)
    for response in bot_responses:
        if response.text.text[0] == "":
            response.text.text[0] = "Desculpe, não entendi! :("
            bot.send_message(message.chat.id, response.text.text[0])
        else:
            bot.send_message(message.chat.id, response.text.text[0])
        createConversation(message.from_user.id, message.text, response.text.text[0], message.date, cursor, connection)

@bot.message_handler(content_types=['photo'])
def send_reply(message):
    # if the connection was lost, then it reconnects
    connection.ping(reconnect=True) 
    bot.send_message(message.chat.id, 'Gostei da foto!')

         
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your_heroku_project.com/' + TOKEN) 
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))