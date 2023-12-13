from aiogram import Bot, Dispatcher, types
from spotdl import Spotdl, DownloaderOptions, Song
from aiogram.filters import Command, CommandObject, CommandStart
from asgiref.sync import sync_to_async
import os
import time
import json
import asyncio
from pathlib import Path
import re

config_file = os.path.join(os.path.dirname(__file__), 'config.json')

with open(config_file, "r") as read_file:
    config = json.load(read_file)

BASE_DIR = Path(__file__).resolve().parent

loop = asyncio.get_event_loop()

bot = Bot(token=config["TOKEN"])
dispatcher = Dispatcher(bot=bot)



spotdl = Spotdl(
	client_id=config["SPOTIFY_ID"],
	client_secret=config["SPOTIFY_SECRET"],
    downloader_settings=DownloaderOptions(output=config["FOLDER"])
)


def update_config():
    with open("config.json", "w") as write_file:
        json.dump(config, write_file)

# Use a constant variable to store the link message
link_type_messages = {
    'track': {
        'uk': 'Завантажую трек зі Spotify...',
        'ru': 'Загружаю трек со Spotify...',
        'en': 'Downloading track from Spotify ...'
    },
    'album': {
        'uk': 'Завантажую альбом зі Spotify ...',
        'ru': 'Загружаю альбом со Spotify...',
        'en': 'Downloading album from Spotify ...'
    },
    'playlist': {
        'uk': 'Завантажую плейлист зі Spotify ...',
        'ru': 'Загружаю плейлист со Spotify...',
        'en': 'Downloading playlist from Spotify ...'
    },
    'invalid': {
        'uk': 'Це не посилання на Spotify!',
        'ru': 'Это не ссылка на Spotify!',
        'en': "It's not a link to a Spotify!"
    }
}

# Use a constant variable to store the authentication message
AUTHORIZATION = {
    'invalid': {
        'uk': 'Ви не ввійшли в систему. Будь ласка, введіть пароль для входу.Наприклад: /password 12345689. Якщо ви його не знаєте, зверніться до власника бота.',
        'ru': 'Вы не вошли в систему. Пожалуйста, введите пароль для входа в систему. Например: /password 12345689. Если вы его не знаете, обратитесь к владельцу бота.',
        'en': 'You are not logged in. Please enter your login password. For example: /password 12345689. If you do not know it, please contact the bot owner.'
    },
    'error':{
        'uk': 'Помилковий пароль!',
        'ru': 'Неверный пароль!',
        'en': 'Incorrect password!'
    },
    'login':{
        'uk': 'Ви успішно увійшли в систему',
        'ru': 'Вы успешно вошли в систему',
        'en': 'You signed in successfully'
    }
}


@dispatcher.message(CommandStart())
async def send_welcome_message(message: types.Message) -> None:
    if message.chat.id in config["AUTH_PASSWORD"]["USERS"]:
        if message.from_user.language_code == 'uk':
            message_text = f"""Привіт, @{message.from_user.username}!
            Я є Telegram-ботом для скачування музики зі Spotify.
            Надішліть мені посилання на Spotify і я відправлю вам цей трек .
            """
        elif message.from_user.language_code == 'ru':
             message_text = f"""Привет, @{message.from_user.username}!
             Я являюсь Telegram ботом для скачивания музыки с Spotify.
             Отправьте мне ссылку на Spotify и я отправлю вам этот трек.
             """
        else:
            message_text = f"""Hello, @{message.from_user.username}!
            I am a Telegram Bot for downloading music from Spotify.
            Send me a link to a Spotify track, and I'll send it back to you.
            """
        sent_message: types.Message = await bot.send_message(chat_id=message.chat.id, text=message_text)
    else:
         if message.from_user.language_code in ['uk', 'ru', 'en']:
              message_text = AUTHORIZATION['invalid'][message.from_user.language_code]
         else:
              message_text = AUTHORIZATION['invalid']['en']
         sent_message: types.Message = await bot.send_message(chat_id=message.chat.id, text=message_text)


@dispatcher.message(Command("password"))
async def handle_message(message: types.Message):
    if message.text.startswith('/password '):
        password_attempt = message.text.split(' ', 1)[1]
        if password_attempt == config["AUTH_PASSWORD"]["PASSWORD"]:
            config["AUTH_PASSWORD"]["USERS"].append(message.chat.id)
            update_config()
            if message.from_user.language_code in ['uk', 'ru', 'en']:
                 message_text = AUTHORIZATION['login'][message.from_user.language_code]
            else:
                 message_text = AUTHORIZATION['login']['en']
            sent_message: types.Message = await bot.send_message(chat_id=message.chat.id, text=message_text)
        else:
             if message.from_user.language_code in ['uk', 'ru', 'en']:
                  message_text = AUTHORIZATION['error'][message.from_user.language_code]
             else:
                  message_text = AUTHORIZATION['error']['en']
             sent_message: types.Message = await bot.send_message(chat_id=message.chat.id, text=message_text)

@dispatcher.message()
async def send_spotify_track_or_album_tracks(message: types.Message) -> None:
    if message.chat.id in config["AUTH_PASSWORD"]["USERS"]:   
        # Use a regular expression to extract the link type from the message text
        link_type = re.search(r'https://open.spotify.com/(track|album|playlist)/', message.text)
        if link_type:
            link_type = link_type.group(1)
            # Use a function to handle the common logic of downloading and sending the audio files
            await download_and_send_audio(message, link_type)
        else:
             if message.from_user.language_code in ['uk', 'ru', 'en']:
                  message_text = link_type_messages['invalid'][message.from_user.language_code]
             else:
                  message_text = link_type_messages['invalid']['en']
             sent_message: types.Message = await message.reply(message_text)
    else:
         if message.from_user.language_code in ['uk', 'ru', 'en']:
              message_text = AUTHORIZATION['invalid'][message.from_user.language_code]
         else:
              message_text = AUTHORIZATION['invalid']['en']
         sent_message: types.Message = await bot.send_message(chat_id=message.chat.id, text=message_text)


async def download_and_send_audio(message: types.Message, link_type: str) -> None:
    if message.from_user.language_code in ['uk', 'ru', 'en']:
         message_text = link_type_messages[link_type][message.from_user.language_code]
    else:
         message_text = link_type_messages[link_type]['en']
    sent_message: types.Message = await bot.send_message(chat_id=message.chat.id, text=message_text)
    spotify_tracks: list[Path] = spotdl.search([message.text])
    spotify_tracks_paths = [await sync_to_async(spotdl.downloader.search_and_download)(song=spotify_track) for spotify_track in spotify_tracks]
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)
    for spotify_track, spotify_track_path in spotify_tracks_paths:
        await message.reply_audio(audio=types.FSInputFile(spotify_track_path))

async def check_downloaded_spotify_tracks() -> None:
    spotify_tracks_dir: Path = BASE_DIR / config["FOLDER"]
    while True:
        for spotify_track in os.listdir(spotify_tracks_dir):
            spotify_track_path: Path = spotify_tracks_dir / spotify_track
            spotify_track_age: float = time.time() - os.path.getatime(spotify_track_path)
            if spotify_track_age > 7 * 24 * 60 * 60:
                os.remove(spotify_track_path)
        await asyncio.sleep(60 * 60)


async def main() -> None:
	await dispatcher.start_polling(bot)
    

if __name__ == '__main__':
        loop.create_task(check_downloaded_spotify_tracks())
        loop.run_until_complete(main())