import asyncio
from telegram import Bot
from config.settings import (
    TELEGRAM_BOT_TOKEN, 
    TELEGRAM_CHAT_ID,
    TELEGRAM_CHANNEL,
    CHANNEL_MESSAGE
)

async def send_video_async(video_path, caption, language="en"):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    with open(video_path, "rb") as video_file:
        await bot.send_video(
            chat_id=TELEGRAM_CHAT_ID,
            video=video_file,
            caption=caption,
            supports_streaming=True
        )
    print(f"✅ Telegram e video sent ({language})")

async def send_message_async(text):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=text,
        parse_mode="HTML"
    )

def send_video(video_path, caption, language="en"):
    asyncio.run(send_video_async(video_path, caption, language))

def send_message(text):
    asyncio.run(send_message_async(text))

def upload_both_videos(en_video, bn_video, en_caption, bn_caption):
    send_message("🏆 <b>Today's Football Analytics</b> 🏆\n\nVideo upload hocche...")
    
    send_video(en_video, f"🇬🇧 {en_caption}", "en")
    send_video(bn_video, f"🇧🇩 {bn_caption}", "bn")
    
    # Channel promotion
    send_message(
        f"📊 <b>Analyze. Predict. Win.</b>\n\n"
        f"{CHANNEL_MESSAGE}\n"
        f"👉 {TELEGRAM_CHANNEL}\n\n"
        f"🔔 Daily football analytics পেতে এখনই join করুন!"
    )