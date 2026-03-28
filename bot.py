import re
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telegram import Bot
from deep_translator import GoogleTranslator

# ===================== CONFIG =====================
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"
API_ID = 12345678   # my.telegram.org-dan götür
API_HASH = "PASTE_API_HASH_HERE"
SOURCE_CHANNEL = "source_channel_username"
TARGET_CHANNEL = "@target_channel_username"
# ==================================================

bot = Bot(token=BOT_TOKEN)
client = TelegramClient("session", API_ID, API_HASH)


def remove_links(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"https?://\\S+|t\\.me/\\S+", "", text).strip()


def translate_to_az(text: str) -> str:
    if not text:
        return ""
    cleaned = remove_links(text)
    try:
        return GoogleTranslator(source='auto', target='az').translate(cleaned)
    except Exception:
        return cleaned


@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    msg = event.message
    translated_text = translate_to_az(msg.text or "")

    # Mətn postu
    if not msg.media:
        await bot.send_message(chat_id=TARGET_CHANNEL, text=translated_text)
        return

    # Foto / video / sənəd
    file_path = await msg.download_media()

    caption = translated_text if translated_text else None

    with open(file_path, "rb") as f:
        if isinstance(msg.media, MessageMediaPhoto):
            await bot.send_photo(chat_id=TARGET_CHANNEL, photo=f, caption=caption)
        else:
            await bot.send_document(chat_id=TARGET_CHANNEL, document=f, caption=caption)


async def main():
    await client.start()
    print("Bot işləyir...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
