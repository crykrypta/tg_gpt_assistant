import logging
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from lexicon import lexicon_ru
from keyboards import keyboards as kb


# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='#%(levelname)-8s [%(name)s]: '
                    '%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)

# Инициализация роутера проекта
router = Router()


# ----------------Command Handlers----------------------- #


# /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text=lexicon_ru.commands['/start'].format(message.from_user.full_name),
        reply_markup=kb.start_kb,
        parse_mode='html'
    )


# /help
@router.message(Command(commands='help'))
async def cmd_help(message: Message):
    await message.answer(text=lexicon_ru.commands['/help'])


# ----------------Callback Handlers----------------------- #


# Переход в главное меню (Для выбора способа загрузки)
@router.callback_query(F.data == 'to_main')
async def load_doc(callback: CallbackQuery):
    await callback.answer(text=lexicon_ru.answers['to_main'])
    await callback.message.edit_text(
        text=lexicon_ru.messages['choose_way_to_load'],
        reply_markup=kb.main_kb,
    )


# Выбор способа через Google Docs
@router.callback_query(F.data == 'load_google_doc')
async def load_doc_from_google_docs(callback: CallbackQuery):
    await callback.answer(
        text=lexicon_ru.answers['load_google_doc']
    )
    await callback.message.edit_text(
        text=lexicon_ru.messages['load_google_doc'],
        parse_mode='html',
        reply_markup=kb.to_main_kb
    )


# Выбор способа через PDF
@router.callback_query(F.data == 'load_PDF')
async def load_doc_from_file(callback: CallbackQuery):
    await callback.answer(
        text=lexicon_ru.answers['load_PDF'],
        show_alert=True)


# Кнопка "Справка"
@router.callback_query(F.data == 'help')
async def help_button(callback: CallbackQuery):
    await callback.answer(text=lexicon_ru.answers['help'])

