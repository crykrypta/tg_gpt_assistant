import logging
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from lexicon import lexicon_ru
from keyboards import keyboards as kb

import db.requests as rq


class Loading(StatesGroup):
    google_doc_url = State()
    pdf_file = State()


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
    # Ответ по лексикону
    await message.answer(
        text=lexicon_ru.commands['/start'].format(message.from_user.full_name),
        reply_markup=kb.start_kb,
        parse_mode='html'
    )
    #  Добавление пользователя в БД
    await rq.set_user(tg_id=message.from_user.id,
                      name=message.from_user.full_name)


# /help
@router.message(Command(commands='help'))
async def cmd_help(message: Message):
    await message.answer(text=lexicon_ru.commands['/help'])


# /salam
@router.message(Command(commands='salam'))
async def cmd_salam(message: Message):
    name = rq.get_name()
    await message.answer(
        text=f'Ваалейкум ас-саляму ва-рахмату ва-баракатуху {name}!' /
        '\n\nИуууууу'
    )

# ----------------Callback Handlers----------------------- #


# Переход в главное меню (Для выбора способа загрузки)
@router.callback_query(F.data == 'to_main')
async def load_doc(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer(text=lexicon_ru.answers['to_main'])
    await callback.message.edit_text(
        text=lexicon_ru.messages['choose_way_to_load'],
        reply_markup=kb.main_kb,
    )


# Выбор способа через Google Docs
@router.callback_query(F.data == 'load_google_doc')
async def load_doc_from_google_docs(callback: CallbackQuery,
                                    state: FSMContext):
    await state.set_state('google_doc_url')
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
async def load_doc_from_file(callback: CallbackQuery,
                             state: FSMContext):
    await state.set_state('pdf_file')
    await callback.answer(
        text=lexicon_ru.answers['load_PDF'],
        show_alert=True)


# Кнопка "Справка"
@router.callback_query(F.data == 'help')
async def help_button(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer(text=lexicon_ru.answers['help'])


# Кнопка "Мои документы"
@router.callback_query(F.data == 'my_docs')
async def my_docs_button(callback: CallbackQuery):
    await callback.answer(text=lexicon_ru.answers['my_docs'],
                          show_alert=True)


@router.message(Loading.google_doc_url)
async def getting_google_doc_url(message: Message, state: FSMContext):
    pass
    # Здесь нужно подключить Алхимию и передать URL
    # Предварительно проверив валидность этой URL
    # Если он валиден, то предложить взглянуть на список своих документов
    # Если нет, то предложить повторить попытку
