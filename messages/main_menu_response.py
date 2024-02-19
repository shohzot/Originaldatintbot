from dotenv import load_dotenv
import os
import random
from loader import bot, dp
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from menus.main_menu import *
from menus.profile_menu import *
from menus.search_menu import *
from database.db_control import DatabaseControl, DatabaseConnection
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from messages.cache_storage import CacheStorage
from languages.lang_en import *
from languages.lang_uz import *
from languages.lang_rus import *


load_dotenv()
HOST, DATABASE, USER, PASSWORD = "ec2-54-86-180-157.compute-1.amazonaws.com", "d1a568i8v42r6j", "sxmrireobmzuut", "7a9e5cffe7a1412f27e8eed56f6617d498ee9d98772bc1f0f4957b3e7e6ae181"


_storage = CacheStorage()
_conn = DatabaseConnection(host=HOST, database=DATABASE, user=USER, password=PASSWORD).connect()
_base = DatabaseControl(_conn)


class Search(StatesGroup):
    search = State()


async def show_profile(message: Message):
    print('checcadadssda')

    if message.text in ("My profile 👤", "Мой профайл 👤", "Mening profilim 👤"):
        print(_base.get_user(message.from_user.id))
        if _base.get_user(message.from_user.id)[2] is not None:
            await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_form"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"PROFILE_MENU"])
            await bot.send_photo(caption=f'{_base.get_user(message.from_user.id)[5]}, {_base.get_user(message.from_user.id)[8]}\n🌐 {_base.get_user(message.from_user.id)[3]}\n\n〰️〰️〰️〰️〰️〰️〰️〰️\n"{_base.get_user(message.from_user.id)[7]}"\n〰️〰️〰️〰️〰️〰️〰️〰️',
                                 photo=_base.get_user(message.from_user.id)[2],
                                 reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"PROFILE_MENU"],
                                 chat_id=message.from_user.id)
        else:
            await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"nosend_form"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"CREATE_NEW_MENU"])

    elif message.text in ("Back to main menu 🔙","Asosiy menyuga qaytish 🔙","Вернуться в главное меню 🔙"):
        await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"turning"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"MAIN_MENU"])
        try:
            await _storage.delete_user(chat_id=message.from_user.id)
        except Exception as _ex:
            pass
#####################################
    elif message.text in ("Search 🔎", "Qidirmoq 🔎","Поиск 🔎", "Who's this?","Kim bu?","Кто это?", "❌", "❤️", "Ok", "Kelishdik", "Хорошо"):
        print('it is inside of the search!')
        if message.text in ["❌", "❤️"]:
            await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_expired"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"MAIN_MENU"])
            print('it came here and checking')
        try:
            await _storage.delete_user(chat_id=message.from_user.id)
        except Exception as ex:
            print(f"No user has been found {ex}")
            pass

        # await Search.search.set()
        params = _base.get_user(message.from_user.id)
        print(1)
        # print(params)
        try:
            search_forms = _base.searchUser(_base.get_user(message.from_user.id)[0], _base.get_user(message.from_user.id)[3], _base.get_user(message.from_user.id)[8], _base.get_user(message.from_user.id)[6], _base.get_user(message.from_user.id)[4])
            print(2)
            print(search_forms)
            await Search.search.set()

            likes = []

            for i in _base.liked(message.from_user.id):
                likes.append(_base.get_user(i))

            mutual = []

            for i in _base.get_mutual(message.from_user.id):
                mutual.append(_base.get_user(i))
            print(likes)
            print(mutual)
            await _storage.add(chat_id=message.from_user.id, forms=search_forms, likes=likes, mutual=mutual)
            await bot.send_message(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_rem"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"ALARM_MENU"], chat_id=message.from_user.id)
        except Exception as ex:
            await bot.send_message(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_nofound"],
                                   chat_id=message.from_user.id)
            print(f"Need to create account: {ex}")
############################################################

async def forming(user, chat_id):
    await bot.send_photo(caption=f'{user[5]}, {user[8]}\n🌐 {user[3]}\n\n〰️〰️〰️〰️〰️〰️〰️〰️\n"{user[7]}"\n〰️〰️〰️〰️〰️〰️〰️〰️',
                         photo=user[2],
                         chat_id=chat_id,
                         reply_markup=globals()[_base.get_user(int(chat_id))[1][2:].upper()+"SEARCH_MENU"])



async def formingfrompath(user, chat_id):
    print('it is for user')
    print(user)
    await bot.send_photo(caption=f'{user[5]}, {user[8]}\n🌐 {user[3]}\n\n〰️〰️〰️〰️〰️〰️〰️〰️\n"{user[7]}"\n〰️〰️〰️〰️〰️〰️〰️〰️',
                         # photo=open(fr'/app/Pictures/{user[2]}.jpg', "rb"),
                         photo=open(fr'/app/Pictures/{user[2]}.jpg', "rb"),
                         chat_id=chat_id,
                         reply_markup=globals()[_base.get_user(int(chat_id))[1][2:].upper()+"SEARCH_MENU"]
    )

async def mutual(user, chat_id):
    await bot.send_photo(caption=f'{user[5]}, {user[8]}\n🌐 {user[3]}\n'+globals()[_base.get_user(int(chat_id))[1][2:].lower()+"send_mutual"]+f'(tg://user?id={user[0]})💓\n\n〰️〰️〰️〰️〰️〰️〰️〰️\n"{user[7]}"\n〰️〰️〰️〰️〰️〰️〰️〰️',
                         parse_mode="Markdown",
                         photo=user[2],
                         chat_id=chat_id,
                         reply_markup=globals()[_base.get_user(int(chat_id))[1][2:].upper()+"SEARCH_MENU"])


async def search(message: Message, state: FSMContext):
    user = await _storage.get_user(chat_id=message.from_user.id)
    forms_list = user['forms']
    random.shuffle(forms_list)
    user['forms'] = forms_list
    print(user)
    # if user == {}:
    #     await message.answer(text="Fill your form before entering a search tab", reply_markup=MAIN_MENU)

    if message.text in ("Back to main menu 🔙","Asosiy menyuga qaytish 🔙","Вернуться в главное меню 🔙"):
        await state.finish()
        await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"turning"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"MAIN_MENU"])
    #############################################
    elif message.text in ["❤️", "❌"]:
        print('it is here inside of the like function')
        if message.text == "❤️":
            print(user["likes"])
            print(user["likes"] != [])
            if user["likes"] != []:
                _base.set_mutual(liker=user["likes"][0][0], liked=message.from_user.id)
                try:
                    await bot.send_message(chat_id=user["likes"][0][0], reply_markup=globals()[_base.get_user(int(user["likes"][0][0]))[1][2:].upper()+"LIKE_MENU"],
                                           text=globals()[_base.get_user(int(user["likes"][0][0]))[1][2:].lower()+"send_interest"])
                except:
                    pass
                try:
                    await mutual(user=user["likes"][0], chat_id=message.from_user.id)
                except:
                    pass
                await _storage.delete_position(chat_id=message.from_user.id, dictionary="likes")
            else:
                print(message.from_user.id,'----',user["forms"][0][0])
                _base.like(liker=message.from_user.id, liked=user["forms"][0][0])
                try:
                    await bot.send_message(chat_id=user["forms"][0][0], reply_markup=globals()[_base.get_user(int(user["forms"][0][0]))[1][2:].upper()+"LIKE_MENU"],
                                           text=globals()[_base.get_user(int(user["forms"][0][0]))[1][2:].lower()+"send_interest"])
                except:
                    pass
                await _storage.delete_position(chat_id=message.from_user.id, dictionary="forms")
                print(user)
        else:
            print(user)
            try:
                print(user["likes"], 'likes')
                if (user["likes"] !=[] and user["forms"] !=[]) or (user["likes"] !=[] and user["forms"] ==[]):
                    _base.dislike(disliker=message.from_user.id, disliked=user["likes"][0][0])
                    _base.delete_liker(liker=user["likes"][0][0], liked=message.from_user.id)
                    await _storage.delete_position(chat_id=message.from_user.id, dictionary="likes")
                    user = await _storage.get_user(chat_id=message.from_user.id)
                    print(user)
                else:
                    _base.dislike(disliker=message.from_user.id, disliked=user["forms"][0][0])
                    _base.delete_liker(liker=user["forms"][0][0], liked=message.from_user.id)
                    await _storage.delete_position(chat_id=message.from_user.id, dictionary="forms")
                    user = await _storage.get_user(chat_id=message.from_user.id)
                    print(user)
                    print('hey')
            except:
                print(user["forms"],'forms')


        try:

            if user["likes"] != []:
                print(user["likes"][0])
                await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_likedform"]+f'{user["likes"][0][5]}❤️')
                print('cas of this function')
                try:
                    await forming(user["likes"][0], chat_id=message.from_user.id)
                except:
                    await formingfrompath(user["likes"][0], chat_id=message.from_user.id)
            else:
                try:
                    await forming(user["forms"][0], chat_id=message.from_user.id)
                except:
                    await formingfrompath(user["forms"][0], chat_id=message.from_user.id)
        except Exception as _ex:
            try:
                await formingfrompath(user["forms"][0], message.from_user.id)
            except:
                await message.answer(globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_unfor"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"MAIN_MENU"])
                print('it came here')
                await state.finish()


############################################################till  here

    elif message.text in ["Who's this?","Kim bu?","Кто это?","Kelishdik","Хорошо", "Ok"]:
        print('this okay ')
        print(user["likes"])
        print(user["mutual"])
        if user["likes"] != []:
            await message.answer(text=globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_likedform"]+f'{user["likes"][0][5]}❤️')
            await forming(user["likes"][0], message.from_user.id)


        elif user["likes"] == [] and user["mutual"] != []:
            for i in user["mutual"]:
                print('it is: ',i)
                print('it is undername: ',user['mutual'][0][0])
                try:
                    await mutual(user=i, chat_id=message.from_user.id)
                except:
                    pass
                # _base.delete_sympathy(liked=message.from_user.id, liker=i[0])
            try:
                await forming(user["forms"][0], message.from_user.id)
            except:
                try:
                    await formingfrompath(user["forms"][0], message.from_user.id)
                except:
                    await message.answer(globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_unfor"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"MAIN_MENU"])
                    await state.finish()
            print('worked this part ')
        else:
            print(user["forms"])
            if user["forms"] == []:
                await message.answer(globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_unfor"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"MAIN_MENU"])
                await state.finish()
            else:
                try:
                    await forming(user["forms"][0], message.from_user.id)
                except:
                    try:
                        await formingfrompath(user["forms"][0], message.from_user.id)
                    except:
                        await message.answer(globals()[_base.get_user(int(message.from_user.id))[1][2:].lower()+"send_unfor"], reply_markup=globals()[_base.get_user(int(message.from_user.id))[1][2:].upper()+"MAIN_MENU"])
                        print('it came here')
                        await state.finish()

#################################

def main_menu_response_handler():
    dp.register_message_handler(show_profile, Text(equals=[
        "My profile 👤","Mening profilim 👤","Мой профайл 👤", "Back to main menu 🔙","Asosiy menyuga qaytish 🔙" ,"Вернуться в главное меню 🔙", "Search 🔎", "Qidirmoq 🔎", "Поиск 🔎", "Who's this?", "Kim bu?","Кто это?", "❌", "❤️", "Ok","Kelishdik","Хорошо"
    ], ignore_case=False), state=None)
    dp.register_message_handler(search, content_types=["any"], state=Search.search)
