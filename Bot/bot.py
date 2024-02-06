from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from parser import Parser
from keyboards import kb, start_kb

from api import TOKEN_API, PARSER_TOKEN_API

TOKEN_API = TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

parser = Parser(api_key=PARSER_TOKEN_API)

HelpText = """
<b>/help</b> - <em>Give us info about commands</em>
<b>/price</b> - <em>Price stock exchange</em>
<b>/convert</b> - <em>Convert between two currencies</em>
<B>/news</b> - <em>Get the fresh news</em>
"""

async def on_startup(_):
    print('Bot was succesfully uploaded on Telegram')

@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    await message.answer(text="Welcome! I'm here to assist you. Feel free to ask any questions or explore my features. 😊",
                         reply_markup=kb)
    await message.delete()

@dp.message_handler(commands=['start_bot'])
async def start_bot(message: types.Message):
    await message.reply('', reply_markup=start_kb)

@dp.callback_query_handler(lambda query: query.data == 'start_bot')
async def start_bot_callback(query: types.CallbackQuery):
    await query.answer()
    await start_command(query.message)

@dp.message_handler(commands='help')
async def help_command(message: types.Message):
    await message.answer(text = HelpText, parse_mode='HTML')

class PriceState(StatesGroup):
    waiting_for_symbol = State()

@dp.message_handler(commands=['price'])
async def cmd_price(message: types.Message):
    await message.reply("Input symbol (for example AAPL):")
    await PriceState.waiting_for_symbol.set()

@dp.message_handler(state=PriceState.waiting_for_symbol)
async def process_symbol(message: types.Message, state: FSMContext):
    symbol = message.text.upper()
    price = parser.get_stock_price(symbol)
    await message.answer(f'Price of {symbol}: {price}')
    await state.finish()

class ConvertState(StatesGroup):
    waiting_for_first_currency = State()
    waiting_for_second_currency = State()
    waiting_for_amount = State()

@dp.message_handler(commands='convert')
async def convert_command(message: types.Message):
    await message.reply("Input currency (for example USD):")
    await ConvertState.waiting_for_first_currency.set()

@dp.message_handler(state=ConvertState.waiting_for_first_currency)
async def convert_process(message: types.Message, state: FSMContext):
    first_currency = message.text.upper()
    await message.reply("Input second currency (for example GBP):")
    await state.update_data(first_currency=first_currency)
    await ConvertState.waiting_for_second_currency.set()

@dp.message_handler(state=ConvertState.waiting_for_second_currency)
async def process_second_currency(message: types.Message, state: FSMContext):
    second_currency = message.text.upper()
    await message.reply("Please input amount:")
    await state.update_data(second_currency=second_currency)
    await ConvertState.waiting_for_amount.set()

@dp.message_handler(state=ConvertState.waiting_for_amount)
async def process_amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    amount = float(message.text)
    result = parser.get_convert(data['first_currency'], data['second_currency'], amount)
    await message.answer(f"{amount} {data['first_currency']} is equal to {result} {data['second_currency']}")
    await state.finish()

class NewsState(StatesGroup):
    waiting_for_symbol = State()

@dp.message_handler(commands=['news'])
async def news_price(message: types.Message):
    await message.reply("Input symbol (for example USD):")
    await NewsState.waiting_for_symbol.set()

@dp.message_handler(state=NewsState.waiting_for_symbol)
async def process_symbol(message: types.Message, state: FSMContext):
    symbol = message.text.upper()
    news = parser.get_news(symbol)
    await message.answer(f'News of {symbol}: \n{news}')
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)



