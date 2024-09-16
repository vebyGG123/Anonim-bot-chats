from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


inKeyButton = InlineKeyboardMarkup(row_width=2)

inButton_1 = InlineKeyboardButton(text="Я согласен(на)",
								callback_data="correct")
inButton_2 = InlineKeyboardButton(text="Я не согласен(на)",
								callback_data="notcorrect")
inKeyButton.add(inButton_1, inButton_2)

inKeyButton2 = InlineKeyboardMarkup(row_width=2)

inButton_1_2 = InlineKeyboardButton(text="Написать сообщение!",
								callback_data="pushsms",
								)
inKeyButton2.add(inButton_1_2)


inKeyButton_3 = InlineKeyboardMarkup(row_width=2)

inButton_1_3 = InlineKeyboardButton(text="Я согласен(на)",
								callback_data="getnik")
inButton_2_3 = InlineKeyboardButton(text="Я не согласен(на)",
								callback_data="notgetnik")
inKeyButton_3.add(inButton_1_3, inButton_2_3)

inKeyButton_4 = InlineKeyboardMarkup(row_width=2)
inButton_1_4 = InlineKeyboardButton(text="Узнать кто написал",
								callback_data="zaprosnik")
inKeyButton_4.add(inButton_1_4)