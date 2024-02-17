from loader import dp, bot
from dotenv import load_dotenv
from aiogram.types import Message
from menus.main_menu import *
import os
from database.db_control import DatabaseControl, DatabaseConnection
from aiogram.dispatcher import FSMContext
import random

load_dotenv()
HOST, DATABASE, USER, PASSWORD = "ec2-54-86-180-157.compute-1.amazonaws.com", "d1a568i8v42r6j", "sxmrireobmzuut", "7a9e5cffe7a1412f27e8eed56f6617d498ee9d98772bc1f0f4957b3e7e6ae181"


_conn = DatabaseConnection(host=HOST, database=DATABASE, user=USER, password=PASSWORD).connect()
_base = DatabaseControl(_conn)

async def start(message: Message,state: FSMContext):

    try:
        print(_base.get_user(message.from_user.id)[0])
    except:
        _base.create_lang((int(message.from_user.id),'🇺🇿Uzb'))

    user = _base.get_user(message.from_user.id)

    if user[1] == '🇺🇿Uzb':
        message_one = "Salom✋\nBu bot sizga yangi tanishuvlarda yordam beradi\nIltimos muloyim bo'ling boshqalar bilan👁"

        await message.answer(text=message_one,
                                 reply_markup=UZBMAIN_MENU)
    elif user[1] == '🇷🇺Rus':
        message_one = "Привет✋\nЭтот бот поможет вам найти новых людей и отлично провести время.\nНе забывайте быть вежливыми с другими людьми👁"
        animation = open("/app/commands/flame1.gif", "rb")
        await message.answer(text=message_one,
                                 reply_markup=RUSMAIN_MENU)
    else:
        message_one = "Hi✋\nThis bot can help you find new people and awesome spend time\nDon't forget to be " \
                      "polite with other people👁"

        await message.answer(text=message_one,
                                 reply_markup=ENGMAIN_MENU)

    # names = ["Tony", "Kiki", "Dilnoza", "Nigora", "Zarina", "Munira", "Feruza", "Malika", "Shirin", "Nazokat",
    #          "Shakhnoza", "Nilufar", "Rukhshona", "Zulfia", "Gulbahor", "Shahnoza", "Surayyo", "Shahzoda", "Mahira",
    #          "Anora", "Farangiz", "Sitora", "Dilorom", "Zarnigor", "Shaxnoza", "Nasiba", "Zulfiya", "Gulnora", "Nozima",
    #          "Firuza", "Ziyoda"]
    # profile_about_sections = [
    #     "Dreamer navigating reality.", "Passionate soul, endless dreams.",
    #     "Life enthusiast and curious explorer.", "Creating joy in simple moments.",
    #     "In love with every sunset.", "Eternal optimist, daydream believer.",
    #     "Seeker of adventure and inner peace.", "Spreading smiles, one day at a time.",
    #     "Finding beauty in ordinary moments.", "Chasing dreams, catching moments.",
    #     "Creating memories, not just moments.", "Adventurous spirit, heart full of dreams.",
    #     "Enjoying the journey called life.", "Aspiring to inspire with positivity.",
    #     "Living with gratitude and purpose.", "Sunshine mixed with a little hurricane.",
    #     "Finding joy in the little things.", "Savoring life's sweetest moments.",
    #     "Dancing through life's ups and downs.", "Heart full of dreams, mind full of wonders.",
    #     "Embracing the journey, cherishing moments.", "Radiating positivity, chasing dreams.",
    #     "Making memories and embracing imperfections.", "Passionate about growth and kindness.",
    #     "Exploring the beauty in simplicity.", "Admiring sunsets and chasing dreams.",
    #     "Life's a journey; cherish every step.", "Dream big, live bigger.",
    #     "In love with the magic of existence.", "Creating a life I love.", "Discovering joy in everyday moments."
    # ]
    #
    # print(len(profile_about_sections))
    # print(len(names))
    # print(message.from_user.id)
    # if message.from_user.id == 147019723:
    #     print('hhshh')
    #     for i in range(1, len(names) + 1):
    #         async with state.proxy() as data:
    #             data["chat_id"] = i
    #             data["lang"] = "🇺🇿Uzb"
    #             data["photo"] = f'{i}'
    #             data["City"] = 'Tashkent'
    #             data["gender"] = 'Female'
    #             data["Name"] = names[i - 1]
    #             data["preference"] = 'Both'
    #             data["about"] = profile_about_sections[i - 1]
    #             data["age"] = int(random.randint(20, 30))
    #             show = tuple(data.values()) + (True,)
    #             base = DatabaseControl(_conn)
    #             base.create_user(show)





async def help_command(message: Message):
    message_one = "---> HELP ME TOO:) <---"
    photo = open("/app/commands/creator1.jpg", "rb")
    await bot.send_photo(caption=message_one,
                         photo=photo,
                         reply_markup=ENGMAIN_MENU,
                         chat_id=message.from_user.id,
                         parse_mode="Markdown")


def commands_file_handlers():
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(help_command, commands=["help"])






