import os
import sys
from collectors.football_data import get_todays_matches, get_standings
from ai_script.generate_script import generate_script, generate_title_and_description
from voice.tts import generate_both_languages
from video.create_video import create_both_videos
from uploader.telegram_upload import upload_both_videos, send_message

def main():
    print("🚀 Sports Analytics Bot Starting...")
    
    # Temp folder banao
    os.makedirs("temp", exist_ok=True)
    
    # Step 1: Aajker matches collect koro
    print("📊 Fetching today's matches...")
    matches = get_todays_matches()
    
    if not matches:
        send_message("⚠️ Aaj kono match nei!")
        print("No matches today. Exiting.")
        sys.exit(0)
    
    print(f"✅ {len(matches)} matches found!")
    
    # Step 2: AI diye script banao (English & Bangla)
    print("✍️ Generating scripts...")
    script_en = generate_script(matches, language="en")
    script_bn = generate_script(matches, language="bn")
    
    if not script_en or not script_bn:
        send_message("❌ Script generation failed!")
        sys.exit(1)
    
    print("✅ Scripts generated!")
    
    # Step 3: Title & Description banao
    print("📝 Generating titles...")
    meta_en = generate_title_and_description(script_en, "en")
    meta_bn = generate_title_and_description(script_bn, "bn")
    
    # Step 4: Voice banao
    print("🎙️ Generating voices...")
    audio_en, audio_bn = generate_both_languages(script_en, script_bn)
    print("✅ Voices generated!")
    
    # Step 5: Video banao
    print("🎬 Creating videos...")
    video_en, video_bn = create_both_videos(
        script_en, script_bn, audio_en, audio_bn
    )
    print("✅ Videos created!")
    
    # Step 6: Telegram e upload koro
    print("📤 Uploading to Telegram...")
    upload_both_videos(
        video_en, video_bn,
        f"🏆 Football Analytics | {meta_en[:100]}",
        f"🏆 ফুটবল বিশ্লেষণ | {meta_bn[:100]}"
    )
    
    print("🎉 All done!")

if __name__ == "__main__":
    main()
