# import libs
import discord
import telebot
import os
import requests
from dotenv import load_dotenv
from colorama import init, Fore, Back, Style
init()

T_TOKEN = None
D_TOKEN = None
CHAT_ID = None
status = False

pins = []  # a list of attachments

image_types = ["png", "jpeg", "gif", "jpg", 'jfif', 'webp']
document_types = ['html', 'txt', 'docx', 'pdf', 'xls', 'xlsx', 'ppt', 'pptx']
audio_types = ['mp3', 'm4a', 'ogg']
video_types = ['mp4', 'm4p','webm']


discord_conn = False


# init discord.py
class MyClient(discord.Client):
	async def on_ready(self):
		global discord_conn
		print(Fore.GREEN + Style.BRIGHT + '\n\t{0} успешно подключился к серверу!\n'.format(self.user) + Style.RESET_ALL)  # when bot has been ligged in
		discord_conn = True
		

	async def on_message(self, message):  # when bot has been recived a message
		author = '{0.author}'.format(message)
		mess = '{0.content}'.format(message)
		global pins

		# downloading an attachments into 'tmp/' directory
		for attachment in message.attachments:
			if any(attachment.filename.lower().endswith(image) for image in image_types):
				await attachment.save(f'tmp/{attachment.filename}')
				pins.append(attachment.filename)  # add attachments to 'pins' list for further usage
				tb_send_image(mess + format_message(author))

			elif any(attachment.filename.lower().endswith(doc) for doc in document_types):
				await attachment.save(f'tmp/{attachment.filename}')
				pins.append(attachment.filename)
				tb_send_doc(mess + format_message(author))

			elif any(attachment.filename.lower().endswith(audio) for audio in audio_types):
				await attachment.save(f'tmp/{attachment.filename}')
				pins.append(attachment.filename)
				tb_send_audio(mess + format_message(author))

			elif any(attachment.filename.lower().endswith(video) for video in video_types):
				pins.append(attachment.filename)
				tb_send_message(mess + f'\n\nСсылка на видео:\n{attachment.url}' + format_message(author))

		if len(pins) == 0:
			tb_send_message(mess + format_message(author))  # call telebot method to send a message

		check_connection()

		pins = []





# format message author (delete 5 end chars)
def format_message(author):
	a = list(author)[:(len(author)-5)]
	author_ready = ''.join(str(i) for i in a) 
	from_ = f'\n\n<i>Form: <b>{author_ready}</b></i>'
	return from_




# send message with telebot
def tb_send_message(message):
	tb.send_message(CHAT_ID, message)

def tb_send_image(message):
	photo = open(f'tmp/{pins[0]}', 'rb')
	tb.send_photo(CHAT_ID, photo, caption=message)

def tb_send_doc(message):
	doc = open(f'tmp/{pins[0]}', 'rb')
	tb.send_document(CHAT_ID, doc, caption=message)

def tb_send_audio(message):
	audio = open(f'tmp/{pins[0]}', 'rb')
	tb.send_audio(CHAT_ID, audio, caption=message)

def tb_send_video(message):
	video = open(f'tmp/{pins[0]}', 'rb')
	tb.send_video(CHAT_ID, video, caption=message)






def create_tmp():
	if os.path.exists('tmp'):
		return
	else:
	    os.mkdir('tmp')

def create_dotenv():
	global T_TOKEN
	global D_TOKEN
	global CHAT_ID
	if os.path.exists('.env'):
		load_dotenv()
		T_TOKEN = str(os.getenv('T_TOKEN'))
		D_TOKEN = str(os.getenv('D_TOKEN'))
		CHAT_ID = str(os.getenv('CHAT_ID'))
	else:
		get_tokens()


def get_tokens():
	global T_TOKEN
	global D_TOKEN
	global CHAT_ID
	print(Fore.MAGENTA + Style.BRIGHT +'\n\tNote:')
	print(Fore.RED + Style.NORMAL + '\n\tЕсли программа завершится с ошибкой,\n\tзначит, один из введённых вами параметров НЕВЕРЕН!\n\tЗапустите программу заново и повторите попытку!\n' + Style.RESET_ALL)
	T_TOKEN = input('\tВведите токен telegram бота: ')
	D_TOKEN = input('\tВведите токен discord бота: ')
	CHAT_ID = input('\tВведите chat-id группы telegram: ')



def check_connection():
	global status
	if requests.get(f'https://api.telegram.org/bot{T_TOKEN}/getMe').status_code == 200 and discord_conn == True:
		status = True
		write_config()



def write_config():
	if status == True:
		config = open('.env', 'w')
		config.write(f'T_TOKEN={T_TOKEN}\n')
		config.write(f'D_TOKEN={D_TOKEN}\n')
		config.write(f'CHAT_ID={CHAT_ID}\n')
		config.close()

print(Fore.YELLOW + Style.BRIGHT + '\n\n\n\tДИСКО-БОТ ПРИВЕТСТВУЕТ ВАС!\n' + Style.RESET_ALL)
create_dotenv()
create_tmp()

tb = telebot.TeleBot(T_TOKEN, parse_mode='HTML')  # init telebot

client = MyClient()  # init discord bot
client.run(D_TOKEN)  # run discord bot

tb.polling(none_stop=True)  # run telebot