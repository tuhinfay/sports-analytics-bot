import asyncio
import os
import subprocess
from telegram import Bot
from config.settings import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    TELEGRAM_CHANNEL,
    CHANNEL_MESSAGE
)

def compress_video(input_path, output_path, target_mb=45):
    """Video compress kore size komabe"""
    # File size check
    size_mb = os.path.getsize(input_path) / (1024 * 1024)
    print(f"Original size: {size_mb:.1f}MB")
    
    if size_mb <= target_mb:
        return input_path
    
    print(f"Compressing to ~{target_mb}MB...")
    
    # FFmpeg diye compress
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vcodec", "libx264",
        "-crf", "28",
        "-preset", "fast",
        "-acodec", "aac",
        "-b:a", "128k",
        "-vf", "scale=1280:720",
        output_path
    ]
    
    subprocess.run(cmd, capture_output=True)
    
    new_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Compressed size: {new_size:.1f}MB")
    return output_path

async def send_video_async(video_path, caption, language="en"):
    # Compress first
    compressed_path = video_path.replace(".mp4", "_compressed.mp4")
    final_path = compress_video(video_path, compressed_path)
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    with open(final_path, "rb") as video_file:
        await bot.send_video(
            chat_id=TELEGRAM_CHAT_ID,
            video=video_file,
            caption=caption,
            supports_streaming=True,
            read_timeout=120,
            write_timeout=120,
            connect_timeout=60
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

    send_message(
        f"📊 <b>Analyze. Predict. Win.</b>\n\n"
        f"{CHANNEL_MESSAGE}\n"
        f"👉 {TELEGRAM_CHANNEL}\n\n"
        f"🔔 Daily football analytics পেতে এখনই join করুন!"
    )