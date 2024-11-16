# Пытаюсь придать своему боту удобоваримый вид:

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery
from crud_functions import get_all_products, add_user, is_included, initiate_db, create_products
from keyboards import *
from config import api

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


medicine_list = ['catharsis.jpg', 'nostalgia.jpg', 'relax.jpg', 'smile.jpg']


class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    initiate_db()
    flag = is_included(message.text)
    if flag:
        await message.answer('Пользователь существует, введите другое имя.')
        await message.answer('Введите имя пользователя (только латинский алфавит):')
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        data_us = await state.get_data()
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    data_us = await state.get_data()
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data_us = await state.get_data()
    username, email, age = data_us['username'], data_us['email'], data_us['age']
    add_user(username, email, age)
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Для подсчета суточной нормы калорий нажмите кнопку "Рассчитать".',
                         reply_markup=kb)


@dp.message_handler(text='Информация')
async def info(message):
    with open('norma.jpg', 'rb') as img:
        await message.answer_photo(img, 'Привет! Я бот, помогающий вашему здоровью.')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kbm)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    medicine_list_file = ['catharsis.jpg', 'nostalgia.jpg', 'relax.jpg', 'smile.jpg']
    initiate_db()
    create_products()
    products = get_all_products()
    for i in range(len(medicine_list_file)):
        with open(medicine_list[i], 'rb') as img:
            await message.answer_photo(img, f'Название: Product {products[i][1]}\n'
                                            f'Описание: {products[i][2]}\n'
                                            f'Цена: {products[i][3]}')
    await message.answer('Выберите продукт:', reply_markup=medicine_kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Упрощенный вариант формулы Миффлина-Сан Жеора: \n'
                              'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;\n'
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_gender(call):
    await call.message.answer('Выберите ваш пол:', reply_markup=gender_kb)
    await UserState.gender.set()
    await call.answer()


@dp.callback_query_handler(lambda c: c.data.startswith('gender_'), state=UserState.gender)
async def process_gender(call: CallbackQuery, state):
    gender = 'М' if call.data == 'gender_male' else 'Ж'
    await state.update_data(gender=gender)
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer('Введите свой рост в сантиметрах:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес в килограммах:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    try:
        if data['gender'] == 'М' or data['gender'] == 'м':
            norm = 10 * abs(int(data['weight'])) + 6.25 * abs(int(data['growth'])) - 5 * abs(int(data['age'])) + 5
        else:
            norm = 10 * abs(int(data['weight'])) + 6.25 * abs(int(data['growth'])) - 5 * abs(int(data['age'])) - 161
        await message.answer(f'Ваша суточная нома {norm} калорий.')
    except:
        await message.answer('Вы воробушек.')
    finally:
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
