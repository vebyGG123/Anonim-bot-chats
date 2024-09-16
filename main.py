#################	
#				#
#				#
#  TELEGRAM BOT	#
#	 BY VEBY	#
#  TG:@vebytop	#
#				#
#################

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from commands import *
from keybord import inKeyButton, inKeyButton2, inKeyButton_3, inKeyButton_4
import sqlite3 as sq
import yaml


with open("config.yaml") as ymlFile:
    config = yaml.load(ymlFile.read(), Loader=yaml.Loader)



bot = Bot(config.get("group").get("token"))
dp = Dispatcher(bot)


async def on_startup(_):
	print("Бот запущен!")


@dp.message_handler(commands=["start"])
async def start(message: types.message) -> message.answer:
	await message.answer(text=START,
		reply_markup=inKeyButton,
		)



@dp.callback_query_handler()
async def get_callback(callback: types.CallbackQuery):
	if callback.data == "correct":
		with sq.connect("base_date.db") as con: 
			cur = con.cursor() 

			cur.execute("""CREATE TABLE IF NOT EXISTS users (
				user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
				users_nik TEXT NOT NULL,
				users_id TEXT NOT NULL
				)""") 

			

			sql_2 = """SELECT users_nik FROM users"""

			cur.execute(sql_2)
			result = cur.fetchall()

			cheak = False

			for i in result:
				if i[0] == callback.from_user.username:
					cheak = False
					break
				else:
					cheak = True

			if cheak:
				sql = """INSERT INTO users (users_nik, users_id) VALUES(?, ?) 
			            """
				cur.execute(sql, (callback.from_user.username, callback.from_user.id,))
				await callback.message.edit_text(text=DEYSTVEE,
											reply_markup=inKeyButton2,
					)
				await callback.answer()
			else:
				await callback.message.edit_text(text="Вы уже есть в нашей базе!")
				await callback.answer()
	
	elif callback.data == "notcorrect":
		await callback.message.edit_text(text="Прощай!")
		await callback.answer()


	elif callback.data == "pushsms":
		await callback.message.edit_text(text=PUSHSMS)
		await callback.answer()


	elif callback.data == "zaprosnik":
		GET_NIK_OTP = f"""
Привет {user_nik}
У тебя хотят узнать юзер ник.
Нажмите кнопку "Я согласен(на)" и в противном случае "Я не согласен(на)"
"""

		await callback.bot.send_message(user_id_otp, GET_NIK_OTP,
							reply_markup=inKeyButton_3)

		await callback.message.answer("Успешно отправлен запрос!")
		await callback.answer()


	elif callback.data == "getnik":
		text = f"""
На удивление тебе сказали юзер айди.
Вот посмотри --> {"@" + user_nik_otp}

		"""

		await callback.bot.send_message(user_id, text)
		await callback.message.answer("Я отправил твой юзер ник!")
		await callback.answer()

	elif callback.data == "notgetnik":
		text = """
К сожелению тебе не дали узнать юзер ник.
Не растраивайся!
		"""

		await callback.bot.send_message(user_id, text)
		await callback.answer()



def correct_text(message: str) -> str:
	res = ""

	for i in message:
		res += str(i)
		res += " "

	return res


user_nik = None;
user_id = None;
user_nik_otp = None;
user_id_otp = None;
@dp.message_handler(lambda message: message.text[0] == "@")
async def pushsms(message: types.message):
	global user_nik;
	global user_id;
	global user_nik_otp;
	global user_id_otp;

	try:
		user_nik_and_text = message.text.split();
		user_nik = user_nik_and_text[0];
		text_mes = correct_text(user_nik_and_text[1:]);
		user_nik_otp = message.from_user.username;
		user_id_otp = message.from_user.id;
	except Exception or ex:
		await message.answer("Вы не указали айди или текст!");
		return;


	if user_nik[0] != "@" :
		await message.answer("Не правельно указан ник пользователя!");
		return;

	with sq.connect("base_date.db") as con: 
		cur = con.cursor()



		sql_2 = """SELECT users_nik, users_id FROM users"""

		cur.execute(sql_2)
		result = cur.fetchall()

		cheak = False

		for i in result:
			if i[0] == user_nik[1:]:
				cheak = True
				user_id = i[1]
				break
			else:
				cheak = False


	if cheak:
		ANONIM_TEXT = f"""
Привет {user_nik}!
На удивление вам отправили анонимное сообщение.
На почитай --> {text_mes}

Вы можешь ответить отправителю.
Для этого просто напиши текст!
					"""

		await bot.send_message(user_id, ANONIM_TEXT,
								reply_markup=inKeyButton_4,
								)
		await message.answer("На удивление все успешно отправлено!")
		return


	else:
		await message.answer("Не удалось найти пользователя в базе данных!")
		return



@dp.message_handler(lambda message: message.text[0] != "@")
async def otvet_na_anonim_sms(message: types.message):
	global user_id_otp
	text = message.text

	OTVET_NA_SMS = f"""
Вам ответили на сообщение!
На пачитай --> {text}

Вы можешь ответить на сообщение!
Просто напишите его.
				"""
	
	await bot.send_message(user_id_otp, OTVET_NA_SMS)
	await message.answer("На удивление все успешно отправлено!")
	user_id_otp = message.from_user.id
	return




if __name__ == "__main__":
	executor.start_polling(dp, on_startup=on_startup,
							skip_updates=True)