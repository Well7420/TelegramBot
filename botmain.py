#.venv\Scripts\activate
import asyncio
import os
from aiogram import Bot, Dispatcher

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from app.handlers import router
from app.database.models import async_main

async def main():
    await async_main()
    bot = Bot(token=os.getenv('TOKEN')) # Токен бота
    dp = Dispatcher() # Диспетчер, щоб Бот міг приймати команди
    dp.include_router(router)
    await dp.start_polling(bot)


# V Додаткова конструкція для def main(). Потрібна для того, щоб виконання функції було тільки якщо запуск був безпосередньо з файлу botmain.py
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот вимкнуто')