from loader import dp, bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from menus.profile_menu import *
from database.db_control import DatabaseControl, DatabaseConnection
from menus.main_menu import *
from dotenv import load_dotenv
import urllib.request
import os
from languages.lang_en import *
from languages.lang_uz import *
from languages.lang_rus import *
BOT_TOKEN = "6857088134:AAF3eX3HFGrk1pfvk-980qwqsIPE3ULPXLA"
# print(int(Message.from_user.id))

# VARIABLES
load_dotenv(".env")
HOST, DATABASE, USER, PASSWORD = os.getenv("HOST"), os.getenv("DATABASE"), os.getenv("USER"), os.getenv("PASSWORD")


_conn = DatabaseConnection(host=HOST, database=DATABASE, user=USER, password=PASSWORD).connect()
_base = DatabaseControl(_conn)

# Forming mutual form to send
async def forming(text, connection, message):
    show = DatabaseControl(connection).get_user(chat_id=int(message.from_user.id))
    await message.answer(text=f"{text}", reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"PROFILE_MENU"])
    await bot.send_photo(caption=f'{show[5]}, {show[8]}\n🌐 {show[3]}\n\n〰️〰️〰️〰️〰️〰️〰️〰️\n"{show[7]}"\n〰️〰️〰️〰️〰️〰️〰️〰️',
                         photo=show[2],
                         reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"PROFILE_MENU"],
                         chat_id=message.from_user.id)

async def formingactive(text, connection, message):
    show = DatabaseControl(connection).get_user(chat_id=int(message.from_user.id))
    await message.answer(text=f"{text}", reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"MAIN_MENU"])
    await bot.send_photo(caption=f'{show[5]}, {show[8]}\n🌐 {show[3]}\n\n〰️〰️〰️〰️〰️〰️〰️〰️\n"{show[7]}"\n〰️〰️〰️〰️〰️〰️〰️〰️',
                         photo=show[2],
                         reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"MAIN_MENU"],
                         chat_id=message.from_user.id)


class FSMRegister(StatesGroup):
    lang = State()
    photo = State()
    city = State()
    gender = State()
    name = State()
    preference = State()
    about = State()
    age = State()


async def initialization(message: Message):
    await FSMRegister.lang.set()
    await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_lang"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"LANGUAGE"])


async def lang(message: Message, state: FSMContext):
    print(message.text)
    if message.text not in ["🇺🇿Uzb", "🇷🇺Rus", "🇺🇸Eng"]:
        await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_lang"])

    else:
        async with state.proxy() as data:
            data["chat_id"] = int(message.from_user.id)
            data["lang"] = message.text
        print(data["lang"])
        await message.answer(text=globals()[data["lang"][2:].lower()+"send_photo"],reply_markup=globals()[data["lang"][2:].upper()+"CANCEL"])
        await FSMRegister.next()


async def photo(message: Message, state: FSMContext):
    if message.content_type != 'photo':
        async with state.proxy() as data:
            pass
        await message.answer(text=globals()[data["lang"][2:].lower()+"send_photo"])

    else:
        async with state.proxy() as data:
            data["photo"] = message.photo[0].file_id
        file_info = await message.bot.get_file(message.photo[0].file_id)
        urllib.request.urlretrieve(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}",
                                   f"/app/Pictures/{message.photo[0].file_id}.jpg")
        print(data["lang"])
        await message.answer(text=globals()[data["lang"][2:].lower()+"send_city"])
        await FSMRegister.next()


async def city(message: Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    if message.content_type == "text" and len(message.text) in range(3, 20):
        async with state.proxy() as data:
            data["City"] = message.text.capitalize()
        await message.answer(text=globals()[data["lang"][2:].lower()+"send_gender"], reply_markup=globals()[data["lang"][2:].upper()+"GENDER_MENU"])
        await FSMRegister.next()

    else:
        if message.content_type != "text":
            await message.answer(text=globals()[data["lang"][2:].lower()+"send_city"])
        else:
            await message.answer(text=globals()[data["lang"][2:].lower()+"send_realcity"])


async def gender(message: Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    if message.content_type == "text" and (message.text in ("Male",'Erkak','Мужской')):
        async with state.proxy() as data:
            data["gender"] = "Male"
        await message.answer(text=globals()[data["lang"][2:].lower()+"send_name"], reply_markup=ReplyKeyboardRemove())
        await FSMRegister.next()
    elif message.content_type == "text" and (message.text in ("Female",'Ayol','Женский')):
        async with state.proxy() as data:
            data["gender"] = "Female"
        await message.answer(text=globals()[data["lang"][2:].lower()+"send_name"], reply_markup=ReplyKeyboardRemove())
        await FSMRegister.next()
    else:
        await message.answer(text=globals()[data["lang"][2:].lower()+"send_realgender"])


async def name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    if message.content_type == "text" and len(message.text) in range(3, 30):
        async with state.proxy() as data:
            data["Name"] = message.text
            await message.answer(text=globals()[data["lang"][2:].lower()+"send_preference"], reply_markup=globals()[data["lang"][2:].upper()+"PREFERENCE_MENU"])
            await FSMRegister.next()
    else:
        await message.answer(text=globals()[data["lang"][2:].lower()+"send_realname"])


async def preference(message: Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    if message.content_type == "text" and (message.text in ("Male",'Erkak','Мужской')):
        async with state.proxy() as data:
            data["preference"] = "Male"
        await message.answer(text=globals()[data["lang"][2:].lower()+"send_about"],
                             reply_markup=ReplyKeyboardRemove())
        await FSMRegister.next()
    elif message.content_type == "text" and (message.text in ("Female",'Ayol','Женский')):
        async with state.proxy() as data:
            data["preference"] = "Female"
        await message.answer(text=globals()[data["lang"][2:].lower() + "send_about"],
                             reply_markup=ReplyKeyboardRemove())
        await FSMRegister.next()
    elif message.content_type == "text" and (message.text in ('Both','Ikkalasi','Оба')):
        async with state.proxy() as data:
            data["preference"] = 'Both'
        await message.answer(text=globals()[data["lang"][2:].lower() + "send_about"],
                             reply_markup=ReplyKeyboardRemove())
        await FSMRegister.next()

    else:
        await message.answer(text=globals()[data["lang"][2:].lower()+"send_realpreference"])


async def about_me(message: Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    if message.content_type == "text" and len(message.text) > 5:
        async with state.proxy() as data:
            data["about"] = message.text
        await message.answer(globals()[data["lang"][2:].lower()+"send_age"])
        await FSMRegister.next()

    else:
        if len(message.text) <= 5:
            await message.answer(text=globals()[data["lang"][2:].lower()+"send_realabout"])
        else:
            await message.answer(text=globals()[data["lang"][2:].lower()+"send_about"])


async def age(message: Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    try:
        if message.content_type == "text" and int(message.text) in range(0, 150):
            async with state.proxy() as data:
                data["age"] = int(message.text)
            await message.answer(globals()[data["lang"][2:].lower()+"created_successfully"])
            show = tuple(data.values()) + (True,)
            print(show)
            await bot.send_photo(caption=f'{show[5]}, {show[8]}\n🌐 {show[3]}\n\n〰️〰️〰️〰️〰️〰️〰️〰️\n"{show[7]}"\n〰️〰️〰️〰️〰️〰️〰️〰️',
                                 photo=show[2],
                                 reply_markup=globals()[data["lang"][2:].upper()+"PROFILE_MENU"],
                                 chat_id=message.from_user.id)

            try:
                base = DatabaseControl(_conn)
                base.delete_user(chat_id=message.from_user.id)
                base.create_user(show)
            except Exception as _ex:
                base = DatabaseControl(_conn)
                base.create_user(show)
            await state.finish()

        else:
            try:
                if int(message.text) not in range(0, 150):
                    await message.answer(text=globals()[data["lang"][2:].lower()+"send_realage"])
            except Exception as _ex:
                await message.answer(text=globals()[data["lang"][2:].lower()+"send_realage"])
    except:
        await message.answer(text=globals()[data["lang"][2:].lower()+"send_realage"])


async def cancel(message: Message, state: FSMContext):
    if message.text in ("Cancel","Bekor qilish","Отмена"):
        await state.finish()
        await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"turning"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"MAIN_MENU"])

class Changes(StatesGroup):
    picture = State()
    about = State()
    active_true = State()
    lang = State()




def form_fill_handlers():
    dp.register_message_handler(cancel, Text(equals=["Cancel","Bekor qilish","Отмена"]), state=[FSMRegister.lang,
                                                                        FSMRegister.photo,
                                                                        FSMRegister.city,
                                                                        FSMRegister.gender,
                                                                        FSMRegister.name,
                                                                        FSMRegister.preference,
                                                                        FSMRegister.about,
                                                                        FSMRegister.age,
                                                                        Changes.picture,
                                                                        Changes.about,
                                                                        Changes.lang])
    dp.register_message_handler(initialization, Text(equals=["Refill my form 🖊","Formani boshidan to'ldirish 🖊","Заполните мою форму 🖊", "Create new 🖊","Yangi yaratish 🖊","Создавать новое 🖊"], ignore_case=True))
    dp.register_message_handler(lang, content_types=["any"], state=FSMRegister.lang)
    dp.register_message_handler(photo, content_types=["any"], state=FSMRegister.photo)
    dp.register_message_handler(city, content_types=["any"], state=FSMRegister.city)
    dp.register_message_handler(gender, content_types=["any"], state=FSMRegister.gender)
    dp.register_message_handler(name, content_types=["any"], state=FSMRegister.name)
    dp.register_message_handler(preference, content_types=["any"], state=FSMRegister.preference)
    dp.register_message_handler(about_me, content_types=["any"], state=FSMRegister.about)
    dp.register_message_handler(age, content_types=["any"], state=FSMRegister.age)



async def changes(message: Message):
    if message.text in ("Change photo 📸","Rasmni o'zgartirmoq 📸","Измени фотографию 📸"):
        await Changes.picture.set()
        await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_photo"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"CANCEL"])
    print('heeey')
    if message.text in ("Change language 📚",'Tilni ozgartirmoq 📚','Изменить язык 📚'):
        await Changes.lang.set()
        await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_lang"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"LANGUAGE"])

    if message.text in ('Change - "about" 📄','"Haqida" ni ozgartirmoq 📄','Изменение - "около" 📄'):
        await Changes.about.set()
        await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_about"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"CANCEL"])

    if message.text in ("I don't want to search any more 🌛","Boshqa qidirishni xoxlamiman 🌛","Я не хочу больше искать 🌛"):
        await Changes.active_true.set()
        await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"disform"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"DISABLE_MENU"])

    if message.text in ("Activate my form",'Formani aktivlashtirish','Активировать мою форму'):
        try:
            DatabaseControl(_conn).change(column="active", data=(True,), chat_id=message.from_user.id)
            await formingactive(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"remember"], message=message, connection=_conn)
        except:
            pass



async def change_photo(message: Message, state: FSMContext):
    if message.content_type == "photo":
        DatabaseControl(_conn).change(column="photo", data=(message.photo[0].file_id,), chat_id=message.from_user.id)
        file_info = await message.bot.get_file(message.photo[0].file_id)
        urllib.request.urlretrieve(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}",
                                   f"/app/Pictures/{message.photo[0].file_id}.jpg")
        await forming(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"changed_photo"], message=message, connection=_conn)
        await state.finish()

    else:
        await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_photo"])


async def change_about(message: Message, state: FSMContext):
    if message.content_type == "text":
        DatabaseControl(_conn).change(column="about", data=(message.text,), chat_id=message.from_user.id)
        await forming(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"changed_about"], message=message, connection=_conn)
        await state.finish()

    else:
        await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_about"])


async def change_lang(message: Message, state: FSMContext):
    if message.text in ["🇺🇿Uzb", "🇷🇺Rus", "🇺🇸Eng"]:
        DatabaseControl(_conn).change(column="lang", data=(message.text,), chat_id=message.from_user.id)
        await forming(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"languagenew"], message=message, connection=_conn)
        await state.finish()

    else:
        await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"lanthese"])


async def disable_form(message: Message, state: FSMContext):
    if message.content_type == "text" and message.text in ("Yes",'Ha','Да'):
        DatabaseControl(_conn).change(column="active", data=(False,), chat_id=message.from_user.id)
        await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"disabletext"],
                             reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"TURN_BACK_MENU"])
        await state.finish()

    elif message.text in ("No","Yo'q",'Нет'):
        await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"turning"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"MAIN_MENU"])
        await state.finish()

    else:
        await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"yesno"])


def changes_handlers():
    dp.register_message_handler(changes, Text(equals=["Change photo 📸","Rasmni o'zgartirmoq 📸",'Измени фотографию 📸',
                                                      'Change - "about" 📄','"Haqida" ni ozgartirmoq 📄','Изменение - "около" 📄',
                                                      "I don't want to search any more 🌛","Boshqa qidirishni xoxlamiman 🌛","Я не хочу больше искать 🌛",
                                                      "Activate my form",'Formani aktivlashtirish','Активировать мою форму',
                                                      "Change language 📚",'Tilni ozgartirmoq 📚','Изменить язык 📚'],
                                              ignore_case=False), state=None)
    dp.register_message_handler(change_photo, content_types=["any"], state=Changes.picture)
    dp.register_message_handler(change_about, content_types=["any"], state=Changes.about)
    dp.register_message_handler(change_lang, content_types=["any"], state=Changes.lang)
    dp.register_message_handler(disable_form, content_types=["any"], state=Changes.active_true)




