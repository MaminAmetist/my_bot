# Вынос клавиатур:
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Общая клавиатура
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_main_1 = KeyboardButton(text='Информация')
kb.add(button_main_1)
button_main_2 = KeyboardButton(text='Рассчитать')
kb.add(button_main_2)
button_main_3 = KeyboardButton(text='Купить')
kb.add(button_main_3)
button_main_4 = KeyboardButton(text='Регистрация')
kb.add(button_main_4)

# Инлайн-клавиатура к расчету
kbm = InlineKeyboardMarkup()
button_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
kbm.add(button_1)
button_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kbm.add(button_2)

# Инлайн-клавиатура к выбору пола
gender_kb = InlineKeyboardMarkup()
button_m = InlineKeyboardButton(text='Я мэн', callback_data='gender_male')
button_f = InlineKeyboardButton(text='Я девочка вообщет', callback_data='gender_female')
gender_kb.add(button_m, button_f)

# Инлайн-клавиатура к выбору средства
medicine_kb = InlineKeyboardMarkup()
vitamine_list_kb = ['радостин', 'ностальгиксин', 'релаксин', 'пакостин']

for vitamine in vitamine_list_kb:
    button = InlineKeyboardButton(text=f'Витамин {vitamine}', callback_data='product_buying')
    medicine_kb.add(button)
