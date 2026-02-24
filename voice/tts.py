import edge_tts
import asyncio
import os

# Better, more natural voices
VOICES = {
    "en": "en-US-AndrewNeural",      # Natural male voice
    "bn": "bn-BD-PradeepNeural",      # Bangla male voice
}

# Voice styles for more natural feel
VOICE_SETTINGS = {
    "en": {
        "rate": "-5%",        # Slightly slower = clearer
        "volume": "+10%",     # Louder
        "pitch": "-3Hz",      # Slightly deeper
    },
    "bn": {
        "rate": "-8%",        # Bangla te aro slow = clear
        "volume": "+10%",
        "pitch": "-2Hz",
    }
}

async def generate_voice_async(script, language="en", output_path="output_audio.mp3"):
    voice = VOICES.get(language, VOICES["en"])
    settings = VOICE_SETTINGS.get(language, VOICE_SETTINGS["en"])
    
    communicate = edge_tts.Communicate(
        script,
        voice,
        rate=settings["rate"],
        volume=settings["volume"],
        pitch=settings["pitch"]
    )
    
    await communicate.save(output_path)
    print(f"✅ Voice generated ({language}): {output_path}")
    return output_path

def generate_voice(script, language="en", output_path="output_audio.mp3"):
    asyncio.run(generate_voice_async(script, language, output_path))
    return output_path

def generate_both_languages(script_en, script_bn, output_dir="temp/"):
    os.makedirs(output_dir, exist_ok=True)
    
    en_path = os.path.join(output_dir, "voice_en.mp3")
    bn_path = os.path.join(output_dir, "voice_bn.mp3")
    
    print("🎙️ Generating English voice...")
    generate_voice(script_en, "en", en_path)
    
    print("🎙️ Generating Bangla voice...")
    generate_voice(script_bn, "bn", bn_path)
    
    return en_path, bn_path