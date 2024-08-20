import logging
import asyncio
from aiogram import Bot, Dispatcher

from config_data.config import load_config
from handlers.handlers import router
from db.models import async_main

# Команда для добавления пути,
# чтобы можно было импортировать модули из других директорий
# sys.path.append(os.path.join(os.getcwd(), 'GPT_assist'))

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='#%(levelname)-8s [%(name)s]: '
                    '%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)


# Асинхронная функция для запуска бота
async def main() -> None:
    # Инициализация базы данных
    await async_main()
    # Загрузка конфигурации
    config = load_config()
    # Инициализация бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    # Регистрация роутера
    dp.include_router(router)
    # Запуск бота
    await dp.start_polling(bot)


# Запуск бота
if __name__ == '__main__':
    try:
        logger.info('Bot started')
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Bot stopped')