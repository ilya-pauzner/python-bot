import config
import telebot
import requests
import os
import logging

# config is python file
# now the only variable there is TOKEN, its value is Telegram Bot Token

bot = telebot.TeleBot(config.TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)

jobs = 0

def handle(file_id):
	file_info = bot.get_file(file_id)
	file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.TOKEN, file_info.file_path))
	name = 'task_%d.py' % jobs
	py_file = open(name, 'w')
	py_file.write(file.text)
	py_file.close()
	os.system("python %s" % (name))

@bot.message_handler(content_types = ["document"])
def handle_job(message):
	global jobs
	jobs += 1
	bot.send_message(message.chat.id, "job %d assigned" % (jobs))
	handle(message.document.file_id)
	bot.send_message(message.chat.id, "job %d done" % (jobs))

	
@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, 'Unknown command')
	
bot.polling()
