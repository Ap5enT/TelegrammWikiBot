from aiogram import Bot, Dispatcher, types, executor, utils
import wikipedia

bot = Bot(token="5540520397:AAFEI9nOttNyJKBVZ7whFIm5qcTekIc0UnY")
dp = Dispatcher(bot)
wikipedia.set_lang('ru')


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет! Я бот, который может найти информацию в википедии, текст следующих сообщений я буду искать")

@dp.message_handler()
async def process_message(message: types.Message):
    try:
        chat_id = message.chat.id
        wikitext = wikipedia.summary(message.text)
        if len(wikitext)>500:
            wikitext = wikitext[0:1000]
            wikitext = wikitext[0:int(wikitext.rindex("."))]
        await bot.send_message(text=f'Вот что я нашел: {wikitext}',chat_id=chat_id)
    except wikipedia.exceptions.DisambiguationError:
        await bot.send_message(text=f"Я нашел слишком много вариантов по запросу  '{message.text}', попробуйте сформировать запрос точнее",chat_id=chat_id)
    except utils.exceptions.MessageIsTooLong:
            await message.reply(f"Статья слишком большая")
    except Exception:
        await message.reply("Извините, произошла какая-то ошибка и я не смог найти такой информации")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
