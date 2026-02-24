import os
import sys
from ai_script.generate_script import generate_script, generate_title_and_description
from voice.tts import generate_both_languages
from video.create_video import create_both_videos
from uploader.telegram_upload import upload_both_videos, send_message
from datetime import datetime

today_str = datetime.now().strftime("%d %B %Y")

# Sample test data with all fields
SAMPLE_MATCHES = [
    {
        "league": "Premier League",
        "league_id": 39,
        "match_date": today_str,
        "home_team": "Arsenal",
        "home_id": 42,
        "home_logo": None,
        "home_form": "WWDWW",
        "home_stats": {
            "goals_for": 45,
            "goals_against": 22,
            "wins": 15,
            "draws": 4,
            "loses": 3
        },
        "away_team": "Manchester City",
        "away_id": 50,
        "away_logo": None,
        "away_form": "WWWDL",
        "away_stats": {
            "goals_for": 52,
            "goals_against": 18,
            "wins": 17,
            "draws": 2,
            "loses": 3
        },
        "time": "2026-02-25T15:00:00",
        "venue": "Emirates Stadium",
    },
    {
        "league": "La Liga",
        "league_id": 140,
        "match_date": today_str,
        "home_team": "Barcelona",
        "home_id": 529,
        "home_logo": None,
        "home_form": "WDWWW",
        "home_stats": {
            "goals_for": 58,
            "goals_against": 20,
            "wins": 18,
            "draws": 3,
            "loses": 2
        },
        "away_team": "Real Madrid",
        "away_id": 541,
        "away_logo": None,
        "away_form": "WWWWL",
        "away_stats": {
            "goals_for": 61,
            "goals_against": 17,
            "wins": 19,
            "draws": 2,
            "loses": 2
        },
        "time": "2026-02-25T20:00:00",
        "venue": "Camp Nou",
    }
]

def test():
    print("🧪 TEST MODE - Sports Analytics Bot")
    print(f"📅 Date: {today_str}")

    os.makedirs("temp", exist_ok=True)
    os.makedirs("temp/logos", exist_ok=True)

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
        script_en, script_bn,
        audio_en, audio_bn,
        match_data=matches
    )
    print("✅ Videos done!")

    print("📤 Uploading to Telegram...")
    upload_both_videos(
        video_en, video_bn,
        f"🧪 TEST | {today_str} | Football Analytics",
        f"🧪 টেস্ট | {today_str} | ফুটবল বিশ্লেষণ"
    )

    print("🎉 Test complete!")

if __name__ == "__main__":
    test()