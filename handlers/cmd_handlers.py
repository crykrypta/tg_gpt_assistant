import logging
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='#%(levelname)-8s [%(name)s]: '
                    '%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)

cmd_router = Router()


# /start
@cmd_router.message(CommandStart())
async def cmd_start(message: Message):
    message.answer(
        text=f'Привет {message.from_user.first_name}!\n\n'
        'Я бот, который поможет тебе разобратьс в твоих документах')


# /help
@cmd_router.message(Command(commands='help'))
async def cmd_help(message: Message):
    message.answer(text='Здесь ббудет информация о боте')



