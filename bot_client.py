import asyncio
import datetime
import json
import logging
import os
import re

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import token_bot_client

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=token_bot_client, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
current_date = datetime.date.today().strftime("%Y-%m-%d")


class Form(StatesGroup):
    phone = State()
    email = State()


@dp.message_handler(commands="start")
async def start(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    photo_path = "Data_files/image/111.jpg"
    with open(photo_path, "rb") as photo:
        initial_buttons = [
            "Алтайский край",
            "Иркутская область",
            "Кемеровская область",
            "Красноярский край",
            "Новосибирская область",
            "Подготовка документов для участия",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in initial_buttons:
            keyboard.add(types.KeyboardButton(button))
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption="Выберите субъект проведения аукционов и публичных предложений",
            reply_markup=keyboard,
        )


@dp.message_handler(lambda message: message.text == "Подготовка документов для участия")
async def podgotovka_dokumentov(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Отмена"))
    await message.answer("Введите ваш номер телефона для связи", reply_markup=keyboard)
    await Form.phone.set()


@dp.message_handler(state=Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.finish()
        await start(message, state)
        return

    phone_number = message.text
    if not is_valid_phone(phone_number):
        await message.answer(
            "Введен некорректный номер телефона. Пожалуйста, введите еще раз."
        )
        return
    await state.update_data(phone=phone_number)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Отмена"))
    await message.answer("Введите email", reply_markup=keyboard)
    await Form.email.set()


@dp.message_handler(state=Form.email)
async def process_email(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.finish()
        await start(message, state)
        return
    email = message.text
    if not is_valid_email(email):
        await message.answer("Введен некорректный email. Пожалуйста, введите еще раз.")
        return
    await state.update_data(email=email)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    data = await state.get_data()
    phone = data.get("phone")
    email = data.get("email")
    client_dict = {
        "Time": current_time,
        "Phone": phone,
        "Email": email,
    }
    try:
        with open(
            f"Data_files/client/{datetime.date.today()}_client.json",
            "r",
            encoding="utf-8",
        ) as file:
            clients = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error reading JSON file: {e}")
        clients = []

    clients.append(client_dict)

    try:
        with open(
            f"Data_files/client/{datetime.date.today()}_client.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(clients, file, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Error writing JSON file: {e}")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Назад"))
    await message.answer("Мы с Вами свяжемся в течении 1 часа", reply_markup=keyboard)
    await state.finish()


def is_valid_phone(phone_number: str) -> bool:
    pattern = r"^(8|\+7)?(\(\d{3}\)?\-)?[\d\-]{7,10}$"
    return bool(re.fullmatch(pattern, phone_number))


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.fullmatch(pattern, email))

    @dp.message_handler(lambda message: message.text == "Нaзад")  # первая а английская
    async def go_back(message: types.Message):
        initial_buttons = [
            "Алтайский край",
            "Иркутская область",
            "Кемеровская область",
            "Красноярский край",
            "Новосибирская область",
            "Подготовка документов для участия",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in initial_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer(
            "Выберите субъект проведения аукционов и публичных предложений",
            reply_markup=keyboard,
        )


class AltayskiyKray:
    @dp.message_handler(lambda message: message.text == "Алтайский край")
    async def altayskiy_kray(message: types.Message, state: FSMContext):
        # await state.update_data(region="Altayskiy_kray")
        # photo_path = "Data_files/image/21.jpg"
        # with open(photo_path, "rb") as photo:
        initial_buttons = [
            "Аукцион (Алт.кр)",
            "Публичное предложение (Алт.кр)",
            "К выбору субъекта",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in initial_buttons:
            keyboard.add(types.KeyboardButton(button))
        await bot.send_message(
            chat_id=message.chat.id,  # добавить photo=photo, text изменить на caption
            text="Выберите вид тогов:\n "
            "- При продаже посредством аукциона цена повышается до максимальной, в результате чего наибольшая цена становится выигрышной.\n"
            "- При продаже посредством публичного предложения осуществляется последовательное снижение цены первоначального предложения на шаг понижения до цены отсечения. \n",
            reply_markup=keyboard,
        )

    @dp.message_handler(
        lambda message: message.text == "Публичное предложение (Алт.кр)"
    )
    async def publichnoe_predlozhenie(message: types.Message):
        # Названия кнопок с одной латинской буквой
        start_buttons = [
            "Автомобили и спецтехникa (Алт.кр)",
            "Недвижимость для личных целeй (Алт.кр)",
            "Недвижимость для бизнесa (Алт.кр)",
            "Земельные учaстки (Алт.кр)",
            "Дебиторская задолженность и Ценные бумaги (Алт.кр)",
            "Оборудованиe (Алт.кр)",
            "Товарно-материальные ценнoсти (Алт.кр)",
            "Сельскохозяйственное имуществo (Алт.кр)",
            "Прочеe (Алт.кр)",
            "Назад",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in start_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer("Выберите подкатегорию", reply_markup=keyboard)

    @dp.message_handler(lambda message: message.text == "Аукцион (Алт.кр)")
    async def aukcion(message: types.Message):
        start_buttons = [
            "Автомобили и спецтехника (Алт.кр)",
            "Недвижимость для личных целей (Алт.кр)",
            "Недвижимость для бизнеса (Алт.кр)",
            "Земельные участки (Алт.кр)",
            "Дебиторская задолженность и Ценные бумаги (Алт.кр)",
            "Оборудование (Алт.кр)",
            "Товарно-материальные ценности (Алт.кр)",
            "Сельскохозяйственное имущество (Алт.кр)",
            "Прочее (Алт.кр)",
            "Назад",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in start_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer("Выберите подкатегорию", reply_markup=keyboard)

    @dp.message_handler(lambda message: message.text == "Назад")
    async def go_back(message: types.Message):
        initial_buttons = [
            "Аукцион (Алт.кр)",
            "Публичное предложение (Алт.кр)",
            "К выбору субъекта",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in initial_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer(
            "Выберите вид тогов:\n "
            "- При продаже посредством аукциона цена повышается до максимальной, в результате чего наибольшая цена становится выигрышной.\n"
            "- При продаже посредством публичного предложения осуществляется последовательное снижение цены первоначального предложения на шаг понижения до цены отсечения. \n",
            reply_markup=keyboard,
        )

    @dp.message_handler(lambda message: message.text == "К выбору субъекта")
    async def go_to_choice_region(message: types.Message, state: FSMContext):
        # await state.update_data(region=None)  # сбросить состояние region
        initial_buttons = [
             "Алтайский край",
            "Иркутская область",
            "Кемеровская область",
            "Красноярский край",
            "Новосибирская область",
            "Подготовка документов для участия",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in initial_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer(
            "Выберите субъект проведения аукционов и публичных предложений",
            reply_markup=keyboard,
        )

    async def send_items(self, message: types.Message, file_path: str):
        # Проверка на существование файла и его содержимое
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            await bot.send_message(
                chat_id=message.chat.id, text="По Вашему запросу ничего не найдено!"
            )
            return
        with open(f"{file_path}", encoding="utf-8") as file:
            new_list = json.load(file)
        for new_dict in new_list:
            step_or_min_price = new_dict.get("Step_or_min_price", "")
            ### если захочешь поставить жирный шрифт при условии \/
            if new_dict.get("Subtext_2") == "Минимальная цена" and step_or_min_price:
                step_or_min_price = f"<b>{step_or_min_price}</b> 🔥"
            url = f'<a href="{new_dict.get("Url", "")}">Ссылка на аукцион</a>'
            auctions = (
                f'<b>{new_dict.get("Title", "")}</b>\n'
                f'{new_dict.get("Subtext_1", "")}\n'
                f'{new_dict.get("Start_price", "")}\n'
                f'{new_dict.get("Subtext_2", "")}\n'
                f"{step_or_min_price}\n"
                f'{new_dict.get("Deadline", "")}\n'
                f"{url}\n"
            )
            if new_dict.get("Image"):
                try:
                    await bot.send_photo(
                        chat_id=message.chat.id,
                        photo=new_dict.get("Image"),
                        caption=auctions,
                    )
                except Exception as e:
                    print(f"Не удалось отправить изображение: {e}")
            else:
                try:
                    await bot.send_message(chat_id=message.chat.id, text=auctions)
                except Exception as e:
                    print(f"Не удалось отправить сообщение: {e}")


altayskiy_kray = AltayskiyKray()


@dp.message_handler(Text(equals="Земельные участки (Алт.кр)"))
async def get_all_auctions_zemelniye_uchastki(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/auctions/data_json/auk_zemelniye_uchastki.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Земельные учaстки (Алт.кр)"))
async def get_all_auctions_zemelniye_uchastki(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_zemelniye_uchastki.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для бизнеса (Алт.кр)"))
async def get_all_auctions_nedvizhimost_dlya_biznesa(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/auctions/data_json/auk_nedvizhimost_dlya_biznesa.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для бизнесa (Алт.кр)"))
async def get_all_auctions_nedvizhimost_dlya_biznesa(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_nedvizhimost_dlya_biznesa.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для личных целей (Алт.кр)"))
async def get_all_auctions_nedvizhimost_dlya_lichnih_celey(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/auctions/data_json/auk_nedvizhimost_dlya_lichnih_celey.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для личных целeй (Алт.кр)"))
async def get_all_auctions_nedvizhimost_dlya_lichnih_celey(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_nedvizhimost_dlya_lichnih_celey.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Автомобили и спецтехника (Алт.кр)"))
async def get_all_auctions_avto_i_spectehnika(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/auctions/data_json/auk_avto_i_spectehnika.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Автомобили и спецтехникa (Алт.кр)"))
async def get_all_auctions_avto_i_spectehnika(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_avto_i_spectehnika.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Дебиторская задолженность и Ценные бумаги (Алт.кр)"))
async def get_all_auctions_debitorskaya_zadolzhnost_i_cennie_bumagi(
    message: types.Message,
):
    file_path = "Data_files/Altayskiy_kray/auctions/data_json/auk_debitorskaya_zadolzhnost_i_cennie_bumagi.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Дебиторская задолженность и Ценные бумaги (Алт.кр)"))
async def get_all_auctions_debitorskaya_zadolzhnost_i_cennie_bumagi(
    message: types.Message,
):
    file_path = "Data_files/Altayskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_debitorskaya_zadolzhnost_i_cennie_bumagi.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Прочее (Алт.кр)"))
async def get_all_auctions_prochee(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/auctions/data_json/auk_prochee.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Прочеe (Алт.кр)"))
async def get_all_auctions_prochee(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_prochee.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Сельскохозяйственное имущество (Алт.кр)"))
async def get_all_auctions_selskohozyaystvennoe_imushestvo(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/auctions/data_json/auk_selskohozyaystvennoe_imushestvo.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Сельскохозяйственное имуществo (Алт.кр)"))
async def get_all_auctions_selskohozyaystvennoe_imushestvo(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_selskohozyaystvennoe_imushestvo.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Оборудование (Алт.кр)"))
async def get_all_auctions_oborudovanie(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/auctions/data_json/auk_oborudovanie.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Оборудованиe (Алт.кр)"))
async def get_all_auctions_oborudovanie(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_oborudovanie.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Товарно-материальные ценности (Алт.кр)"))
async def get_all_auctions_tovarno_materialnie_cennosti(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/auctions/data_json/auk_tovarno_materialnie_cennosti.json"
    await altayskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Товарно-материальные ценнoсти (Алт.кр)"))
async def get_all_auctions_tovarno_materialnie_cennosti(message: types.Message):
    file_path = "Data_files/Altayskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_tovarno_materialnie_cennosti.json"
    await altayskiy_kray.send_items(message, file_path)


class Novosibirskaya_obl:
    @dp.message_handler(lambda message: message.text == "Новосибирская область")
    async def novosibirskaya_oblast(message: types.Message, state: FSMContext):
        # await state.update_data(region="Novosibirskaya_oblast")
        # photo_path = "Data_files/image/21.jpg"
        # with open(photo_path, "rb") as photo:
        initial_buttons = [
            "Аукцион (Нов.обл)",
            "Публичное предложение (Нов.обл)",
            "К выбору субъекта",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in initial_buttons:
            keyboard.add(types.KeyboardButton(button))
        await bot.send_message(
            chat_id=message.chat.id,  # добавить photo=photo, text изменить на caption
            text="Выберите вид тогов:\n "
            "- При продаже посредством аукциона цена повышается до максимальной, в результате чего наибольшая цена становится выигрышной.\n"
            "- При продаже посредством публичного предложения осуществляется последовательное снижение цены первоначального предложения на шаг понижения до цены отсечения. \n",
            reply_markup=keyboard,
        )

    @dp.message_handler(
        lambda message: message.text == "Публичное предложение (Нов.обл)"
    )
    async def publichnoe_predlozhenie(message: types.Message):
        # Названия кнопок с одной латинской буквой
        start_buttons = [
            "Автомобили и спецтехникa (Нов.обл)",
            "Недвижимость для личных целeй (Нов.обл)",
            "Недвижимость для бизнесa (Нов.обл)",
            "Земельные учaстки (Нов.обл)",
            "Дебиторская задолженность и Ценные бумaги (Нов.обл)",
            "Оборудованиe (Нов.обл)",
            "Товарно-материальные ценнoсти (Нов.обл)",
            "Сельскохозяйственное имуществo (Нов.обл)",
            "Прочеe (Нов.обл)",
            "<Назад",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in start_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer("Выберите подкатегорию", reply_markup=keyboard)

    @dp.message_handler(lambda message: message.text == "Аукцион (Нов.обл)")
    async def aukcion(message: types.Message):
        start_buttons = [
            "Автомобили и спецтехника (Нов.обл)",
            "Недвижимость для личных целей (Нов.обл)",
            "Недвижимость для бизнеса (Нов.обл)",
            "Земельные участки (Нов.обл)",
            "Дебиторская задолженность и Ценные бумаги (Нов.обл)",
            "Оборудование (Нов.обл)",
            "Товарно-материальные ценности (Нов.обл)",
            "Сельскохозяйственное имущество (Нов.обл)",
            "Прочее (Нов.обл)",
            "<Назад",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in start_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer("Выберите подкатегорию", reply_markup=keyboard)

    @dp.message_handler(lambda message: message.text == "<Назад")
    async def go_back(message: types.Message):
        initial_buttons = [
            "Аукцион (Нов.обл)",
            "Публичное предложение (Нов.обл)",
            "К выбору субъекта",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in initial_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer(
            "Выберите вид тогов:\n "
            "- При продаже посредством аукциона цена повышается до максимальной, в результате чего наибольшая цена становится выигрышной.\n"
            "- При продаже посредством публичного предложения осуществляется последовательное снижение цены первоначального предложения на шаг понижения до цены отсечения. \n",
            reply_markup=keyboard,
        )

    async def send_items(self, message: types.Message, file_path: str):
        # Проверка на существование файла и его содержимое
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            await bot.send_message(
                chat_id=message.chat.id, text="По Вашему запросу ничего не найдено!"
            )
            return
        with open(f"{file_path}", encoding="utf-8") as file:
            new_list = json.load(file)
        for new_dict in new_list:
            step_or_min_price = new_dict.get("Step_or_min_price", "")
            ### если захочешь поставить жирный шрифт при условии \/
            if new_dict.get("Subtext_2") == "Минимальная цена" and step_or_min_price:
                step_or_min_price = f"<b>{step_or_min_price}</b> 🔥"
            url = f'<a href="{new_dict.get("Url", "")}">Ссылка на аукцион</a>'
            auctions = (
                f'<b>{new_dict.get("Title", "")}</b>\n'
                f'{new_dict.get("Subtext_1", "")}\n'
                f'{new_dict.get("Start_price", "")}\n'
                f'{new_dict.get("Subtext_2", "")}\n'
                f"{step_or_min_price}\n"
                f'{new_dict.get("Deadline", "")}\n'
                f"{url}\n"
            )
            if new_dict.get("Image"):
                try:
                    await bot.send_photo(
                        chat_id=message.chat.id,
                        photo=new_dict.get("Image"),
                        caption=auctions,
                    )
                except Exception as e:
                    print(f"Не удалось отправить изображение: {e}")
            else:
                try:
                    await bot.send_message(chat_id=message.chat.id, text=auctions)
                except Exception as e:
                    print(f"Не удалось отправить сообщение: {e}")


novosibirskaya_obl = Novosibirskaya_obl()


@dp.message_handler(Text(equals="Земельные участки (Нов.обл)"))
async def get_all_auctions_zemelniye_uchastki(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/auctions/data_json/auk_zemelniye_uchastki.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Земельные учaстки (Нов.обл)"))
async def get_all_auctions_zemelniye_uchastki(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/publichnoe_predlozhenie/data_json/pub_pred_zemelniye_uchastki.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для бизнеса (Нов.обл)"))
async def get_all_auctions_nedvizhimost_dlya_biznesa(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/auctions/data_json/auk_nedvizhimost_dlya_biznesa.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для бизнесa (Нов.обл)"))
async def get_all_auctions_nedvizhimost_dlya_biznesa(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/publichnoe_predlozhenie/data_json/pub_pred_nedvizhimost_dlya_biznesa.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для личных целей (Нов.обл)"))
async def get_all_auctions_nedvizhimost_dlya_lichnih_celey(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/auctions/data_json/auk_nedvizhimost_dlya_lichnih_celey.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для личных целeй (Нов.обл)"))
async def get_all_auctions_nedvizhimost_dlya_lichnih_celey(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/publichnoe_predlozhenie/data_json/pub_pred_nedvizhimost_dlya_lichnih_celey.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Автомобили и спецтехника (Нов.обл)"))
async def get_all_auctions_avto_i_spectehnika(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/auctions/data_json/auk_avto_i_spectehnika.json"

    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Автомобили и спецтехникa (Нов.обл)"))
async def get_all_auctions_avto_i_spectehnika(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/publichnoe_predlozhenie/data_json/pub_pred_avto_i_spectehnika.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(
    Text(equals="Дебиторская задолженность и Ценные бумаги (Нов.обл)")
)
async def get_all_auctions_debitorskaya_zadolzhnost_i_cennie_bumagi(
    message: types.Message,
):
    file_path = "Data_files/Novosibirsk_obl/auctions/data_json/auk_debitorskaya_zadolzhnost_i_cennie_bumagi.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(
    Text(equals="Дебиторская задолженность и Ценные бумaги (Нов.обл)")
)
async def get_all_auctions_debitorskaya_zadolzhnost_i_cennie_bumagi(
    message: types.Message,
):
    file_path = "Data_files/Novosibirsk_obl/publichnoe_predlozhenie/data_json/pub_pred_debitorskaya_zadolzhnost_i_cennie_bumagi.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Прочее (Нов.обл)"))
async def get_all_auctions_prochee(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/auctions/data_json/auk_prochee.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Прочеe (Нов.обл)"))
async def get_all_auctions_prochee(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/publichnoe_predlozhenie/data_json/pub_pred_prochee.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Сельскохозяйственное имущество (Нов.обл)"))
async def get_all_auctions_selskohozyaystvennoe_imushestvo(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/auctions/data_json/auk_selskohozyaystvennoe_imushestvo.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Сельскохозяйственное имуществo (Нов.обл)"))
async def get_all_auctions_selskohozyaystvennoe_imushestvo(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/publichnoe_predlozhenie/data_json/pub_pred_selskohozyaystvennoe_imushestvo.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Оборудование (Нов.обл)"))
async def get_all_auctions_oborudovanie(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/auctions/data_json/auk_oborudovanie.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Оборудованиe (Нов.обл)"))
async def get_all_auctions_oborudovanie(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/publichnoe_predlozhenie/data_json/pub_pred_oborudovanie.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Товарно-материальные ценности (Нов.обл)"))
async def get_all_auctions_tovarno_materialnie_cennosti(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/auctions/data_json/auk_tovarno_materialnie_cennosti.json"
    await novosibirskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Товарно-материальные ценнoсти (Нов.обл)"))
async def get_all_auctions_tovarno_materialnie_cennosti(message: types.Message):
    file_path = "Data_files/Novosibirsk_obl/publichnoe_predlozhenie/data_json/pub_pred_tovarno_materialnie_cennosti.json"
    await novosibirskaya_obl.send_items(message, file_path)

class Krasnoyarskiy_kray():
    @dp.message_handler(lambda message: message.text == "Красноярский край")
    async def krasnoyarskiy_kray(message: types.Message, state: FSMContext):
        # await state.update_data(region="Novosibirskaya_oblast")
        # photo_path = "Data_files/image/21.jpg"
        # with open(photo_path, "rb") as photo:
        initial_buttons = [
            "Аукцион (Красн.кр)",
            "Публичное предложение (Красн.кр)",
            "К выбору субъекта",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in initial_buttons:
            keyboard.add(types.KeyboardButton(button))
        await bot.send_message(
            chat_id=message.chat.id,  # добавить photo=photo, text изменить на caption
            text="Выберите вид тогов:\n "
            "- При продаже посредством аукциона цена повышается до максимальной, в результате чего наибольшая цена становится выигрышной.\n"
            "- При продаже посредством публичного предложения осуществляется последовательное снижение цены первоначального предложения на шаг понижения до цены отсечения. \n",
            reply_markup=keyboard,
        )

    @dp.message_handler(
        lambda message: message.text == "Публичное предложение (Красн.кр)"
    )
    async def publichnoe_predlozhenie(message: types.Message):
        # Названия кнопок с одной латинской буквой
        start_buttons = [
            "Автомобили и спецтехникa (Красн.кр)",
            "Недвижимость для личных целeй (Красн.кр)",
            "Недвижимость для бизнесa (Красн.кр)",
            "Земельные учaстки (Красн.кр)",
            "Дебиторская задолженность и Ценные бумaги (Красн.кр)",
            "Оборудованиe (Красн.кр)",
            "Товарно-материальные ценнoсти (Красн.кр)",
            "Сельскохозяйственное имуществo (Красн.кр)",
            "Прочеe (Красн.кр)",
            "<<Назад",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in start_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer("Выберите подкатегорию", reply_markup=keyboard)

    @dp.message_handler(lambda message: message.text == "Аукцион (Красн.кр)")
    async def aukcion(message: types.Message):
        start_buttons = [
            "Автомобили и спецтехника (Красн.кр)",
            "Недвижимость для личных целей (Красн.кр)",
            "Недвижимость для бизнеса (Красн.кр)",
            "Земельные участки (Красн.кр)",
            "Дебиторская задолженность и Ценные бумаги (Красн.кр)",
            "Оборудование (Красн.кр)",
            "Товарно-материальные ценности (Красн.кр)",
            "Сельскохозяйственное имущество (Красн.кр)",
            "Прочее (Красн.кр)",
            "<<Назад",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in start_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer("Выберите подкатегорию", reply_markup=keyboard)

    @dp.message_handler(lambda message: message.text == "<<Назад")
    async def go_back(message: types.Message):
        initial_buttons = [
            "Аукцион (Красн.кр)",
            "Публичное предложение (Красн.кр)",
            "К выбору субъекта",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in initial_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer(
            "Выберите вид тогов:\n "
            "- При продаже посредством аукциона цена повышается до максимальной, в результате чего наибольшая цена становится выигрышной.\n"
            "- При продаже посредством публичного предложения осуществляется последовательное снижение цены первоначального предложения на шаг понижения до цены отсечения. \n",
            reply_markup=keyboard,
        )

    async def send_items(self, message: types.Message, file_path: str):
        # Проверка на существование файла и его содержимое
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            await bot.send_message(
                chat_id=message.chat.id, text="По Вашему запросу ничего не найдено!"
            )
            return
        with open(f"{file_path}", encoding="utf-8") as file:
            new_list = json.load(file)
        for new_dict in new_list:
            step_or_min_price = new_dict.get("Step_or_min_price", "")
            ### если захочешь поставить жирный шрифт при условии \/
            if new_dict.get("Subtext_2") == "Минимальная цена" and step_or_min_price:
                step_or_min_price = f"<b>{step_or_min_price}</b> 🔥"
            url = f'<a href="{new_dict.get("Url", "")}">Ссылка на аукцион</a>'
            auctions = (
                f'<b>{new_dict.get("Title", "")}</b>\n'
                f'{new_dict.get("Subtext_1", "")}\n'
                f'{new_dict.get("Start_price", "")}\n'
                f'{new_dict.get("Subtext_2", "")}\n'
                f"{step_or_min_price}\n"
                f'{new_dict.get("Deadline", "")}\n'
                f"{url}\n"
            )
            if new_dict.get("Image"):
                try:
                    await bot.send_photo(
                        chat_id=message.chat.id,
                        photo=new_dict.get("Image"),
                        caption=auctions,
                    )
                except Exception as e:
                    print(f"Не удалось отправить изображение: {e}")
            else:
                try:
                    await bot.send_message(chat_id=message.chat.id, text=auctions)
                except Exception as e:
                    print(f"Не удалось отправить сообщение: {e}")


krasnoyarskiy_kray = Krasnoyarskiy_kray()


@dp.message_handler(Text(equals="Земельные участки (Красн.кр)"))
async def get_all_auctions_zemelniye_uchastki(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/auctions/data_json/auk_zemelniye_uchastki.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Земельные учaстки (Красн.кр)"))
async def get_all_auctions_zemelniye_uchastki(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_zemelniye_uchastki.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для бизнеса (Красн.кр)"))
async def get_all_auctions_nedvizhimost_dlya_biznesa(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/auctions/data_json/auk_nedvizhimost_dlya_biznesa.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для бизнесa (Красн.кр)"))
async def get_all_auctions_nedvizhimost_dlya_biznesa(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_nedvizhimost_dlya_biznesa.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для личных целей (Красн.кр)"))
async def get_all_auctions_nedvizhimost_dlya_lichnih_celey(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/auctions/data_json/auk_nedvizhimost_dlya_lichnih_celey.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для личных целeй (Красн.кр)"))
async def get_all_auctions_nedvizhimost_dlya_lichnih_celey(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_nedvizhimost_dlya_lichnih_celey.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Автомобили и спецтехника (Красн.кр)"))
async def get_all_auctions_avto_i_spectehnika(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/auctions/data_json/auk_avto_i_spectehnika.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Автомобили и спецтехникa (Красн.кр)"))
async def get_all_auctions_avto_i_spectehnika(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_avto_i_spectehnika.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(
    Text(equals="Дебиторская задолженность и Ценные бумаги (Красн.кр)")
)
async def get_all_auctions_debitorskaya_zadolzhnost_i_cennie_bumagi(
    message: types.Message,
):
    file_path = "Data_files/Krasnoyarskiy_kray/auctions/data_json/auk_debitorskaya_zadolzhnost_i_cennie_bumagi.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(
    Text(equals="Дебиторская задолженность и Ценные бумaги (Красн.кр)")
)
async def get_all_auctions_debitorskaya_zadolzhnost_i_cennie_bumagi(
    message: types.Message,
):
    file_path = "Data_files/Krasnoyarskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_debitorskaya_zadolzhnost_i_cennie_bumagi.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Прочее (Красн.кр)"))
async def get_all_auctions_prochee(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/auctions/data_json/auk_prochee.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Прочеe (Красн.кр)"))
async def get_all_auctions_prochee(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_prochee.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Сельскохозяйственное имущество (Красн.кр)"))
async def get_all_auctions_selskohozyaystvennoe_imushestvo(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/auctions/data_json/auk_selskohozyaystvennoe_imushestvo.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Сельскохозяйственное имуществo (Красн.кр)"))
async def get_all_auctions_selskohozyaystvennoe_imushestvo(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_selskohozyaystvennoe_imushestvo.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Оборудование (Красн.кр)"))
async def get_all_auctions_oborudovanie(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/auctions/data_json/auk_oborudovanie.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Оборудованиe (Красн.кр)"))
async def get_all_auctions_oborudovanie(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_oborudovanie.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Товарно-материальные ценности (Красн.кр)"))
async def get_all_auctions_tovarno_materialnie_cennosti(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/auctions/data_json/auk_tovarno_materialnie_cennosti.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


@dp.message_handler(Text(equals="Товарно-материальные ценнoсти (Красн.кр)"))
async def get_all_auctions_tovarno_materialnie_cennosti(message: types.Message):
    file_path = "Data_files/Krasnoyarskiy_kray/publichnoe_predlozhenie/data_json/pub_pred_tovarno_materialnie_cennosti.json"
    await krasnoyarskiy_kray.send_items(message, file_path)


class Irkutskaya_oblast():
    @dp.message_handler(lambda message: message.text == "Иркутская область")
    async def irkutskaya_oblast(message: types.Message, state: FSMContext):
        # await state.update_data(region="Novosibirskaya_oblast")
        # photo_path = "Data_files/image/21.jpg"
        # with open(photo_path, "rb") as photo:
        initial_buttons = [
            "Аукцион (Ирк.обл)",
            "Публичное предложение (Ирк.обл)",
            "К выбору субъекта",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in initial_buttons:
            keyboard.add(types.KeyboardButton(button))
        await bot.send_message(
            chat_id=message.chat.id,  # добавить photo=photo, text изменить на caption
            text="Выберите вид тогов:\n "
            "- При продаже посредством аукциона цена повышается до максимальной, в результате чего наибольшая цена становится выигрышной.\n"
            "- При продаже посредством публичного предложения осуществляется последовательное снижение цены первоначального предложения на шаг понижения до цены отсечения. \n",
            reply_markup=keyboard,
        )

    @dp.message_handler(
        lambda message: message.text == "Публичное предложение (Ирк.обл)"
    )
    async def publichnoe_predlozhenie(message: types.Message):
        # Названия кнопок с одной латинской буквой
        start_buttons = [
            "Автомобили и спецтехникa (Ирк.обл)",
            "Недвижимость для личных целeй (Ирк.обл)",
            "Недвижимость для бизнесa (Ирк.обл)",
            "Земельные учaстки (Ирк.обл)",
            "Дебиторская задолженность и Ценные бумaги (Ирк.обл)",
            "Оборудованиe (Ирк.обл)",
            "Товарно-материальные ценнoсти (Ирк.обл)",
            "Сельскохозяйственное имуществo (Ирк.обл)",
            "Прочеe (Ирк.обл)",
            "<<<Назад",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in start_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer("Выберите подкатегорию", reply_markup=keyboard)

    @dp.message_handler(lambda message: message.text == "Аукцион (Ирк.обл)")
    async def aukcion(message: types.Message):
        start_buttons = [
            "Автомобили и спецтехника (Ирк.обл)",
            "Недвижимость для личных целей (Ирк.обл)",
            "Недвижимость для бизнеса (Ирк.обл)",
            "Земельные участки (Ирк.обл)",
            "Дебиторская задолженность и Ценные бумаги (Ирк.обл)",
            "Оборудование (Ирк.обл)",
            "Товарно-материальные ценности (Ирк.обл)",
            "Сельскохозяйственное имущество (Ирк.обл)",
            "Прочее (Ирк.обл)",
            "<<<Назад",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in start_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer("Выберите подкатегорию", reply_markup=keyboard)

    @dp.message_handler(lambda message: message.text == "<<<Назад")
    async def go_back(message: types.Message):
        initial_buttons = [
            "Аукцион (Ирк.обл)",
            "Публичное предложение (Ирк.обл)",
            "К выбору субъекта",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in initial_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer(
            "Выберите вид тогов:\n "
            "- При продаже посредством аукциона цена повышается до максимальной, в результате чего наибольшая цена становится выигрышной.\n"
            "- При продаже посредством публичного предложения осуществляется последовательное снижение цены первоначального предложения на шаг понижения до цены отсечения. \n",
            reply_markup=keyboard,
        )

    async def send_items(self, message: types.Message, file_path: str):
        # Проверка на существование файла и его содержимое
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            await bot.send_message(
                chat_id=message.chat.id, text="По Вашему запросу ничего не найдено!"
            )
            return
        with open(f"{file_path}", encoding="utf-8") as file:
            new_list = json.load(file)
        for new_dict in new_list:
            step_or_min_price = new_dict.get("Step_or_min_price", "")
            ### если захочешь поставить жирный шрифт при условии \/
            if new_dict.get("Subtext_2") == "Минимальная цена" and step_or_min_price:
                step_or_min_price = f"<b>{step_or_min_price}</b> 🔥"
            url = f'<a href="{new_dict.get("Url", "")}">Ссылка на аукцион</a>'
            auctions = (
                f'<b>{new_dict.get("Title", "")}</b>\n'
                f'{new_dict.get("Subtext_1", "")}\n'
                f'{new_dict.get("Start_price", "")}\n'
                f'{new_dict.get("Subtext_2", "")}\n'
                f"{step_or_min_price}\n"
                f'{new_dict.get("Deadline", "")}\n'
                f"{url}\n"
            )

            if new_dict.get("Image"):
                try:
                    await bot.send_photo(
                        chat_id=message.chat.id,
                        photo=new_dict.get("Image"),
                        caption=auctions,
                    )
                except Exception as e:
                    print(f"Не удалось отправить изображение: {e}")
            else:
                try:
                    await bot.send_message(chat_id=message.chat.id, text=auctions)
                except Exception as e:
                    print(f"Не удалось отправить сообщение: {e}")


irkutskaya_obl = Irkutskaya_oblast()


@dp.message_handler(Text(equals="Земельные участки (Ирк.обл)"))
async def get_all_auctions_zemelniye_uchastki(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/auctions/data_json/auk_zemelniye_uchastki.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Земельные учaстки (Ирк.обл)"))
async def get_all_auctions_zemelniye_uchastki(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_zemelniye_uchastki.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для бизнеса (Ирк.обл)"))
async def get_all_auctions_nedvizhimost_dlya_biznesa(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/auctions/data_json/auk_nedvizhimost_dlya_biznesa.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для бизнесa (Ирк.обл)"))
async def get_all_auctions_nedvizhimost_dlya_biznesa(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_nedvizhimost_dlya_biznesa.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для личных целей (Ирк.обл)"))
async def get_all_auctions_nedvizhimost_dlya_lichnih_celey(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/auctions/data_json/auk_nedvizhimost_dlya_lichnih_celey.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для личных целeй (Ирк.обл)"))
async def get_all_auctions_nedvizhimost_dlya_lichnih_celey(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_nedvizhimost_dlya_lichnih_celey.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Автомобили и спецтехника (Ирк.обл)"))
async def get_all_auctions_avto_i_spectehnika(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/auctions/data_json/auk_avto_i_spectehnika.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Автомобили и спецтехникa (Ирк.обл)"))
async def get_all_auctions_avto_i_spectehnika(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_avto_i_spectehnika.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(
    Text(equals="Дебиторская задолженность и Ценные бумаги (Ирк.обл)")
)
async def get_all_auctions_debitorskaya_zadolzhnost_i_cennie_bumagi(
    message: types.Message,
):
    file_path = "Data_files/Irkutskaya_oblast/auctions/data_json/auk_debitorskaya_zadolzhnost_i_cennie_bumagi.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(
    Text(equals="Дебиторская задолженность и Ценные бумaги (Ирк.обл)")
)
async def get_all_auctions_debitorskaya_zadolzhnost_i_cennie_bumagi(
    message: types.Message,
):
    file_path = "Data_files/Irkutskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_debitorskaya_zadolzhnost_i_cennie_bumagi.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Прочее (Ирк.обл)"))
async def get_all_auctions_prochee(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/auctions/data_json/auk_prochee.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Прочеe (Ирк.обл)"))
async def get_all_auctions_prochee(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_prochee.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Сельскохозяйственное имущество (Ирк.обл)"))
async def get_all_auctions_selskohozyaystvennoe_imushestvo(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/auctions/data_json/auk_selskohozyaystvennoe_imushestvo.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Сельскохозяйственное имуществo (Ирк.обл)"))
async def get_all_auctions_selskohozyaystvennoe_imushestvo(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_selskohozyaystvennoe_imushestvo.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Оборудование (Ирк.обл)"))
async def get_all_auctions_oborudovanie(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/auctions/data_json/auk_oborudovanie.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Оборудованиe (Ирк.обл)"))
async def get_all_auctions_oborudovanie(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_oborudovanie.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Товарно-материальные ценности (Ирк.обл)"))
async def get_all_auctions_tovarno_materialnie_cennosti(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/auctions/data_json/auk_tovarno_materialnie_cennosti.json"
    await irkutskaya_obl.send_items(message, file_path)


@dp.message_handler(Text(equals="Товарно-материальные ценнoсти (Ирк.обл)"))
async def get_all_auctions_tovarno_materialnie_cennosti(message: types.Message):
    file_path = "Data_files/Irkutskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_tovarno_materialnie_cennosti.json"
    await irkutskaya_obl.send_items(message, file_path)

class Kemerovskaya_oblast():
    @dp.message_handler(lambda message: message.text == "Кемеровская область")
    async def kemerovskaya_oblast(message: types.Message, state: FSMContext):
        # await state.update_data(region="Novosibirskaya_oblast")
        # photo_path = "Data_files/image/21.jpg"
        # with open(photo_path, "rb") as photo:
        initial_buttons = [
            "Аукцион (Кем.обл)",
            "Публичное предложение (Кем.обл)",
            "К выбору субъекта",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in initial_buttons:
            keyboard.add(types.KeyboardButton(button))
        await bot.send_message(
            chat_id=message.chat.id,  # добавить photo=photo, text изменить на caption
            text="Выберите вид тогов:\n "
            "- При продаже посредством аукциона цена повышается до максимальной, в результате чего наибольшая цена становится выигрышной.\n"
            "- При продаже посредством публичного предложения осуществляется последовательное снижение цены первоначального предложения на шаг понижения до цены отсечения. \n",
            reply_markup=keyboard,
        )

    @dp.message_handler(
        lambda message: message.text == "Публичное предложение (Кем.обл)"
    )
    async def publichnoe_predlozhenie(message: types.Message):
        # Названия кнопок с одной латинской буквой
        start_buttons = [
            "Автомобили и спецтехникa (Кем.обл)",
            "Недвижимость для личных целeй (Кем.обл)",
            "Недвижимость для бизнесa (Кем.обл)",
            "Земельные учaстки (Кем.обл)",
            "Дебиторская задолженность и Ценные бумaги (Кем.обл)",
            "Оборудованиe (Кем.обл)",
            "Товарно-материальные ценнoсти (Кем.обл)",
            "Сельскохозяйственное имуществo (Кем.обл)",
            "Прочеe (Кем.обл)",
            "<<<<Назад",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in start_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer("Выберите подкатегорию", reply_markup=keyboard)

    @dp.message_handler(lambda message: message.text == "Аукцион (Кем.обл)")
    async def aukcion(message: types.Message):
        start_buttons = [
            "Автомобили и спецтехника (Кем.обл)",
            "Недвижимость для личных целей (Кем.обл)",
            "Недвижимость для бизнеса (Кем.обл)",
            "Земельные участки (Кем.обл)",
            "Дебиторская задолженность и Ценные бумаги (Кем.обл)",
            "Оборудование (Кем.обл)",
            "Товарно-материальные ценности (Кем.обл)",
            "Сельскохозяйственное имущество (Кем.обл)",
            "Прочее (Кем.обл)",
            "<<<<Назад",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in start_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer("Выберите подкатегорию", reply_markup=keyboard)

    @dp.message_handler(lambda message: message.text == "<<<<Назад")
    async def go_back(message: types.Message):
        initial_buttons = [
            "Аукцион (Кем.обл)",
            "Публичное предложение (Кем.обл)",
            "К выбору субъекта",
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in initial_buttons:
            keyboard.add(types.KeyboardButton(button))
        await message.answer(
            "Выберите вид тогов:\n "
            "- При продаже посредством аукциона цена повышается до максимальной, в результате чего наибольшая цена становится выигрышной.\n"
            "- При продаже посредством публичного предложения осуществляется последовательное снижение цены первоначального предложения на шаг понижения до цены отсечения. \n",
            reply_markup=keyboard,
        )

    async def send_items(self, message: types.Message, file_path: str):
        # Проверка на существование файла и его содержимое
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            await bot.send_message(
                chat_id=message.chat.id, text="По Вашему запросу ничего не найдено!"
            )
            return
        with open(f"{file_path}", encoding="utf-8") as file:
            new_list = json.load(file)
        for new_dict in new_list:
            step_or_min_price = new_dict.get("Step_or_min_price", "")
            ### если захочешь поставить жирный шрифт при условии \/
            if new_dict.get("Subtext_2") == "Минимальная цена" and step_or_min_price:
                step_or_min_price = f"<b>{step_or_min_price}</b> 🔥"
            url = f'<a href="{new_dict.get("Url", "")}">Ссылка на аукцион</a>'
            auctions = (
                f'<b>{new_dict.get("Title", "")}</b>\n'
                f'{new_dict.get("Subtext_1", "")}\n'
                f'{new_dict.get("Start_price", "")}\n'
                f'{new_dict.get("Subtext_2", "")}\n'
                f"{step_or_min_price}\n"
                f'{new_dict.get("Deadline", "")}\n'
                f"{url}\n"
            )

            if new_dict.get("Image"):
                try:
                    await bot.send_photo(
                        chat_id=message.chat.id,
                        photo=new_dict.get("Image"),
                        caption=auctions,
                    )
                except Exception as e:
                    print(f"Не удалось отправить изображение: {e}")
            else:
                try:
                    await bot.send_message(chat_id=message.chat.id, text=auctions)
                except Exception as e:
                    print(f"Не удалось отправить сообщение: {e}")


kemerovskaya_oblast = Kemerovskaya_oblast()


@dp.message_handler(Text(equals="Земельные участки (Кем.обл)"))
async def get_all_auctions_zemelniye_uchastki(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/auctions/data_json/auk_zemelniye_uchastki.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(Text(equals="Земельные учaстки (Кем.обл)"))
async def get_all_auctions_zemelniye_uchastki(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_zemelniye_uchastki.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для бизнеса (Кем.обл)"))
async def get_all_auctions_nedvizhimost_dlya_biznesa(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/auctions/data_json/auk_nedvizhimost_dlya_biznesa.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для бизнесa (Кем.обл)"))
async def get_all_auctions_nedvizhimost_dlya_biznesa(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_nedvizhimost_dlya_biznesa.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для личных целей (Кем.обл)"))
async def get_all_auctions_nedvizhimost_dlya_lichnih_celey(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/auctions/data_json/auk_nedvizhimost_dlya_lichnih_celey.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(Text(equals="Недвижимость для личных целeй (Кем.обл)"))
async def get_all_auctions_nedvizhimost_dlya_lichnih_celey(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_nedvizhimost_dlya_lichnih_celey.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(Text(equals="Автомобили и спецтехника (Кем.обл)"))
async def get_all_auctions_avto_i_spectehnika(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/auctions/data_json/auk_avto_i_spectehnika.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(Text(equals="Автомобили и спецтехникa (Кем.обл)"))
async def get_all_auctions_avto_i_spectehnika(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_avto_i_spectehnika.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(
    Text(equals="Дебиторская задолженность и Ценные бумаги (Кем.обл)")
)
async def get_all_auctions_debitorskaya_zadolzhnost_i_cennie_bumagi(
    message: types.Message,
):
    file_path = "Data_files/Kemerovskaya_oblast/auctions/data_json/auk_debitorskaya_zadolzhnost_i_cennie_bumagi.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(
    Text(equals="Дебиторская задолженность и Ценные бумaги (Кем.обл)")
)
async def get_all_auctions_debitorskaya_zadolzhnost_i_cennie_bumagi(
    message: types.Message,
):
    file_path = "Data_files/Kemerovskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_debitorskaya_zadolzhnost_i_cennie_bumagi.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(Text(equals="Прочее (Кем.обл)"))
async def get_all_auctions_prochee(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/auctions/data_json/auk_prochee.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(Text(equals="Прочеe (Кем.обл)"))
async def get_all_auctions_prochee(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_prochee.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(Text(equals="Сельскохозяйственное имущество (Кем.обл)"))
async def get_all_auctions_selskohozyaystvennoe_imushestvo(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/auctions/data_json/auk_selskohozyaystvennoe_imushestvo.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(Text(equals="Сельскохозяйственное имуществo (Кем.обл)"))
async def get_all_auctions_selskohozyaystvennoe_imushestvo(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_selskohozyaystvennoe_imushestvo.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(Text(equals="Оборудование (Кем.обл)"))
async def get_all_auctions_oborudovanie(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/auctions/data_json/auk_oborudovanie.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(Text(equals="Оборудованиe (Кем.обл)"))
async def get_all_auctions_oborudovanie(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_oborudovanie.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(Text(equals="Товарно-материальные ценности (Кем.обл)"))
async def get_all_auctions_tovarno_materialnie_cennosti(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/auctions/data_json/auk_tovarno_materialnie_cennosti.json"
    await kemerovskaya_oblast.send_items(message, file_path)


@dp.message_handler(Text(equals="Товарно-материальные ценнoсти (Кем.обл)"))
async def get_all_auctions_tovarno_materialnie_cennosti(message: types.Message):
    file_path = "Data_files/Kemerovskaya_oblast/publichnoe_predlozhenie/data_json/pub_pred_tovarno_materialnie_cennosti.json"
    await kemerovskaya_oblast.send_items(message, file_path)

if __name__ == "__main__":
    from aiogram import executor

    try:
        loop = asyncio.get_event_loop()
        bot_info = loop.run_until_complete(bot.get_me())
        print(f"Bot info: {bot_info}")
    except Exception as e:
        print(f"Bot is already running: {str(e)}")
        exit(0)
    executor.start_polling(dp)
