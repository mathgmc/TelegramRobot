import random
import re
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name,URL

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

def is_number_regex(s):
    """ Returns True is string is a number. """
    if re.match("^\d+?\.\d+?$", s) is None:
        return s.isdigit()
    return True

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)

   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # for debugging purposes only
   print("got text message :", text)
   # the first time you chat with the bot AKA the welcoming message
   if text == "/start":
       # print the welcoming message
       bot_welcome = """
       Hello, I'm Matheus's robot.
       Say ´random´ to get a random quote, or say anything to get the backwards.
       """
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

   elif text.lower() == "random":
       bot_text = [6]
       bot_text.append("What you get by achieving your goals is not as important as what you become by achieving your goals")
       bot_text.append("Live as if you were to die tomorrow. Learn as if you were to live forever")
       bot_text.append("We may affirm absolutely that nothing great in the world has been accomplished without passion")
       bot_text.append("Obstacles are those frightful things you see when you take your eyes off the goal")
       bot_text.append("The way to get started is to quit talking and begin doing")
       bot_text.append("If music be the food of love, play on")

       i = random.randint(0,5)

       bot.sendMessage(chat_id=chat_id, text=bot_text[i], reply_to_message_id=msg_id)

   else:
       resp = ""
       for i in text:
           resp = i + resp
       bot.sendMessage(chat_id=chat_id, text=resp, reply_to_message_id=msg_id)

   return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"

@app.route('/')
def index():
   return '.'


if __name__ == '__main__':
   app.run(threaded=True)
