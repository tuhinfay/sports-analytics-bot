import os
import sys
from collectors.football_data import get_todays_matches
from ai_script.generate_script import generate_script, generate_title_and_description
from voice.tts import generate_both_languages
from video.create_video import create_both_videos
from uploader.telegram_upload import upload_both_videos, send_message

# Sample test data
SAMPLE_MATCHES = [
    {
        "league": "Premier League",
        "home_team": "Arsenal",
        "away_team": "Manchester City",
        "time": "2026-02-25T15:00:00",
        "home_form": "WWDWW",
        "away_form": "WWWDL",
        "venue": "Emirates Stadium",
    },
    {
        "league": "La Liga",
        "home_team": "Barcelona",
        "away_team": "Real Madrid",
        "time": "2026-02-25T20:00:00",
        "home_form": "WDWWW",
        "away_form": "WWWWL",
        "venue": "Camp Nou",
    }
]

def test():
    print("🧪 TEST MODE - Sports Analytics Bot")
    
    os.makedirs("temp", exist_ok=True)
    
    matches = SAMPLE_MATCHES
    print(f"✅ Using {len(matches)} sample matches")
    
    print("✍️ Generating scripts...")
    script_en = generate_script(matches, language="en")
    script_bn = generate_script(matches, language="bn")
    print("✅ Scripts done!")
    
    print("📝 Generating titles...")
    meta_en = generate_title_and_description(script_en, "en")
    meta_bn = generate_title_and_description(script_bn, "bn")
    
    print("🎙️ Generating voices...")
    audio_en, audio_bn = generate_both_languages(script_en, script_bn)
    print("✅ Voices done!")
    
    print("🎬 Creating videos...")
    video_en, video_bn = create_both_videos(
        script_en, script_bn, audio_en, audio_bn
    )
    print("✅ Videos done!")
    
    print("📤 Uploading to Telegram...")
    upload_both_videos(
        video_en, video_bn,
        f"🧪 TEST | Football Analytics | {meta_en[:80]}",
        f"🧪 টেস্ট | ফুটবল বিশ্লেষণ | {meta_bn[:80]}"
    )
    
    print("🎉 Test complete!")

if __name__ == "__main__":
    test()
