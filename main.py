from aiogram import Bot, Dispatcher, types, executor, utils
import dotenv
import wikipedia
import os

dotenv.load_dotenv()
Token= os.getenv("Token")
bot = Bot(Token)
dp = Dispatcher(bot)
wikipedia.set_lang('ru')
Not_to_find = ["Что такое ", "что такое ", " это ","Кто такой","кто такой"]

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет! Я бот, который может найти информацию в википедии, текст следующих сообщений я буду искать")

@dp.message_handler()
async def process_message(message: types.Message):
    try:
        chat_id = message.chat.id
        to_find = message.text
        index=-1
        for words in Not_to_find:
            if to_find.find(words)!=None:
                break
            index+=1
        if index!=-1:
            to_find = to_find.replace(Not_to_find[index],"")
        wikitext = wikipedia.summary(to_find)
        if len(wikitext)>500:
            wikitext = wikitext[0:1000]
            wikitext = wikitext[0:int(wikitext.rindex("."))]
        await bot.send_message(text=f'Вот что я нашел: {wikitext}',chat_id=chat_id)
        print(f"Поиск по запросу '{to_find}' выполнен успешно ")
        print(f"Пользователь:{message.from_user}, {message.forward_from_chat}")
    except wikipedia.exceptions.DisambiguationError:
        await bot.send_message(text=f"Я нашел слишком много вариантов по запросу  '{message.text}', попробуйте сформировать запрос точнее",chat_id=chat_id)
        print(f"Поиск по запросу '{to_find}' выполнен с ошибкой 1 ")
    except utils.exceptions.MessageIsTooLong:
            await message.reply(f"Статья слишком большая")
            print(f"Поиск по запросу '{to_find}' выполнен с ошибкой 2 ")
    except Exception:
        await message.reply("Извините, произошла какая-то ошибка и я не смог найти информацию по вашему запросу")
        print(f"Поиск по запросу '{to_find}' выполнен с ошибкой -1 ")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)