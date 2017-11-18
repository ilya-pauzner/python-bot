import config
import telebot
import requests
import os

bot = telebot.TeleBot(config.TOKEN)
jobs = 0

def handle(file_id):
	file_info = bot.get_file(file_id)
	file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.TOKEN, file_info.file_path))
	py_file = open('task %d.py' % jobs, 'w')
	py_file.write(file.text)
	py_file.close()
	os.system("python test.py")

@bot.message_handler(content_types = ["document"])
def handle_job(message):
	global jobs
	bot.reply_to(message, "job %d assigned" % (jobs))
	print(message)
	handle(message.document.file_id)
	bot.send_message(message.chat.id, "job %d done" % (jobs))
	jobs += 1
	
@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, 'Unknown command')
	
bot.polling()
