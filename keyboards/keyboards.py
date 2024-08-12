from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon import lexicon_ru


# Часто используемые кнопки
buttons: dict[str, InlineKeyboardButton] = {
    'to_main': InlineKeyboardButton(text=lexicon_ru.buttons['to_main'],
                                    callback_data='to_main'),
    'help': InlineKeyboardButton(text=lexicon_ru.buttons['help'],
                                 callback_data='help'),
}


# Стартовая клавиатура
start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Загрузить документ',
                              callback_data='to_main')]
    ]
)

# Клавиатура главного меню
main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=lexicon_ru.buttons['load_google_doc'],
                              callback_data='load_google_doc')],
        [InlineKeyboardButton(text=lexicon_ru.buttons['load_PDF'],
                              callback_data='load_PDF')],
        [buttons['help'], buttons['to_main']]
    ]
)

# Клавиатура в с одной кнопкой "На главную"
to_main_kb = InlineKeyboardMarkup(inline_keyboard=[[buttons['to_main']]])

# Клавиатура с двумя кнопками "На главную" и "Справка"
main_help_kb = InlineKeyboardMarkup(
    inline_keyboard=[[buttons['help'], buttons['to_main']]]
)
