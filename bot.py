
import telebot
import requests

import os
import logging

if __name__ == '__main__':
	# Telegram bot token
	TOKEN = open('config', 'r').read()
	bot = telebot.TeleBot(TOKEN)
	
	logger = telebot.logger
	telebot.logger.setLevel(logging.WARNING)
	
	jobs = 0
	
	@bot.message_handler(content_types = ["document"])
	def handle_job(message):
		global jobs
		jobs += 1
		j = jobs
		bot.send_message(message.chat.id, "job %d assigned" % (j))
		
		file_info = bot.get_file(message.document.file_id)
		file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.TOKEN, file_info.file_path))
		name = 'task_%d.py' % jobs
		py_file = open(name, 'w')
		py_file.write(file.text)
		py_file.close()
		os.system("python %s" % (name))
		
		bot.send_message(message.chat.id, "job %d done" % (j))
	
		
	@bot.message_handler(func=lambda m: True)
	def echo_all(message):
		bot.reply_to(message, 'Unknown command')
		
	bot.polling()
