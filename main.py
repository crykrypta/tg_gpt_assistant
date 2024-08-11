import openai
import asyncio
from aiogram import Bot, Dispatcher

from config_data.config import load_config
from handlers.cmd_handlers import cmd_router
# Команда для добавления пути,
# чтобы можно было импортировать модули из других директорий
# sys.path.append(os.path.join(os.getcwd(), 'GPT_assist'))

config = load_config()

openai.api_key = config.openai.token


async def main() -> None:
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    dp.include_router(cmd_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот был остановлен.')
