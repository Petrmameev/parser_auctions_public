import asyncio
import datetime
import json
import os

from aiogram import Bot, Dispatcher, exceptions, executor, types

from config import token_bot_executor

# Список пользователей
# helgapataku
allowed_users = ["Petrmameev", "1953377708"]

# Создание бота
bot = Bot(token_bot_executor)
dp = Dispatcher(bot)

sent_messages = set()


async def read_json(chat_id):
    # last_check = None
    while True:
        file_path = f"Data_files/client/{datetime.date.today()}_client.json"
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                json.dump([], file)
        # new_check = None
        try:
            with open(
                f"Data_files/client/{datetime.date.today()}_client.json",
                "r",
                encoding="utf-8",
            ) as file:
                new_list = json.load(file)
                for new_dict in new_list:
                    message_id = (
                        f'{new_dict.get("Time", "")}{new_dict.get("Phone", "")}'
                    )
                    if message_id not in sent_messages:
                        all_contact = (
                            f'{new_dict.get("Time", "")}\n'
                            f'{new_dict.get("Phone", "")}\n'
                            f'{new_dict.get("Email", "")}\n'
                        )
                        await bot.send_message(chat_id, text=all_contact)
                        sent_messages.add(message_id)
                        # new_check = new_dict.get("Time", "")
                # if new_check != last_check:
                #     last_check = new_check
                await asyncio.sleep(10)  # Периодичность проверки обновлений
        except exceptions.ChatNotFound:
            print(f"Чат {chat_id} не найден")
            break


# Запуск функции чтения для каждого пользователя из списка
async def on_startup(dp):
    for user in allowed_users:
        asyncio.create_task(read_json(user))


# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
