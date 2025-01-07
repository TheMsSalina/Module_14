
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import crud_functions

products = crud_functions.get_all_products()

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')],
    [KeyboardButton(text='Купить')]],
    resize_keyboard=True)

kb = InlineKeyboardMarkup()
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_ = InlineKeyboardButton(text='Формула рассчёта', callback_data='formula')
kb.add(button, button_)

kb2 = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb2.add(button1, button2, button3, button4)


class UserState(StatesGroup):
    weight = State()
    growth = State()
    age = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message_handler(text ='Рассчитать')
async def start_message(message):
    await message.answer('Выберите опцию:', reply_markup = kb)

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norma = (10 * int(data["weight"])) + (6.25 * int(data["growth"])) - (5 * int(data["age"])- 161)
    await message.answer(f"Ваша норма калорий: {norma}")
    await state.finish()

@dp.callback_query_handler(text='formula')
async def get_formulas(call):
    await call.message.answer('Норма калорий = 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for number in range (1,5):
        with open(f'files/{number}.png', 'rb') as img:
            await message.answer_photo(img)
        await message.answer(f'Название: Product{number} | Описание: описание{number} | Цена: {number * 100}', )
    await message.answer('Выберите продукт для покупки:', reply_markup=kb2)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')

@dp.message_handler(text=['Регистрация'])
async def sign_up(message):
    await message.answer(
        'Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if crud_functions.is_included(message.text):
        await message.answer('Пользователь существует, введите другое имя')
        return
    await state.update_data(username=message.text)
    await message.answer('Введите свой email:')
    await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    crud_functions.add_user(data['username'], data['email'], data['age'])
    await message.answer(f'Пользователь {data["username"]} зарегистрирован.')
    await state.finish()

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer(f'Привет {message.from_user.username}! Я бот помогающий твоему здоровью.', reply_markup = menu)

@dp.message_handler(text = ['Информация'])
async def info_message(message):
    await message.answer('Информация о боте')

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
