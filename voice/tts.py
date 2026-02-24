import edge_tts
import asyncio
import os

# Language wise voice selection
VOICES = {
    "en": "en-US-ChristopherNeural",  # English male voice
    "bn": "bn-BD-NabanitaNeural",      # Bangla female voice
}

async def generate_voice_async(script, language="en", output_path="output_audio.mp3"):
    """Script theke voice banabe"""
    
    voice = VOICES.get(language, VOICES["en"])
    
    communicate = edge_tts.Communicate(script, voice)
    await communicate.save(output_path)
    
    print(f"✅ Voice generated: {output_path}")
    return output_path

def generate_voice(script, language="en", output_path="output_audio.mp3"):
    """Sync wrapper"""
    asyncio.run(generate_voice_async(script, language, output_path))
    return output_path

def generate_both_languages(script_en, script_bn, output_dir="temp/"):
    """English & Bangla dono voice banabe"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    en_path = os.path.join(output_dir, "voice_en.mp3")
    bn_path = os.path.join(output_dir, "voice_bn.mp3")
    
    generate_voice(script_en, "en", en_path)
    generate_voice(script_bn, "bn", bn_path)
    
    return en_path, bn_path
