import os
import requests
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Pexels API free background video er jonno
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

def get_background_video(query="football stadium", output_path="temp/bg.mp4"):
    """Pexels theke free background video nebe"""
    os.makedirs("temp", exist_ok=True)
    
    if PEXELS_API_KEY:
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=1"
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if data.get("videos"):
            video_url = data["videos"][0]["video_files"][0]["link"]
            video_data = requests.get(video_url)
            with open(output_path, "wb") as f:
                f.write(video_data.content)
            return output_path
    
    return None

def create_text_image(text, width=1920, height=1080, 
                       bg_color=(0,0,0,180), text_color=(255,255,255)):
    """Text overlay image banabe"""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background overlay
    overlay = Image.new("RGBA", (width, height), bg_color)
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    # Text wrap
    wrapped = textwrap.fill(text, width=50)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        font = ImageFont.load_default()
        small_font = font
    
    # Center text
    bbox = draw.textbbox((0, 0), wrapped, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), wrapped, font=font, fill=text_color)
    
    output = "temp/text_overlay.png"
    img.save(output)
    return output

def create_video(script, audio_path, language="en", output_path=None):
    """Full video create korbe"""
    
    os.makedirs("temp", exist_ok=True)
    
    if output_path is None:
        output_path = f"temp/final_video_{language}.mp4"
    
    # Audio load
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration
    
    # Background video try koro
    bg_path = get_background_video("football stadium")
    
    if bg_path and os.path.exists(bg_path):
        bg_clip = VideoFileClip(bg_path).loop(duration=duration)
        bg_clip = bg_clip.resize((1920, 1080))
    else:
        # Background video na thakle color background
        bg_clip = ColorClip(size=(1920, 1080), 
                           color=(15, 32, 67),  # Dark blue
                           duration=duration)
    
    # Script ke chunks e bhag koro
    words = script.split()
    chunk_size = 30
    chunks = [" ".join(words[i:i+chunk_size]) 
              for i in range(0, len(words), chunk_size)]
    
    chunk_duration = duration / len(chunks)
    
    # Text clips banao
    text_clips = []
    for i, chunk in enumerate(chunks):
        img_path = create_text_image(chunk)
        txt_clip = (ImageClip(img_path)
                   .set_start(i * chunk_duration)
                   .set_duration(chunk_duration)
                   .set_opacity(0.85))
        text_clips.append(txt_clip)
    
    # Sob combine koro
    final = CompositeVideoClip([bg_clip] + text_clips)
    final = final.set_audio(audio_clip)
    
    # Export
    final.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        verbose=False,
        logger=None
    )
    
    print(f"✅ Video created: {output_path}")
    return output_path

def create_both_videos(script_en, script_bn, audio_en, audio_bn):
    """English & Bangla dono video banabe"""
    
    en_video = create_video(script_en, audio_en, "en", "temp/video_en.mp4")
    bn_video = create_video(script_bn, audio_bn, "bn", "temp/video_bn.mp4")
    
    return en_video, bn_video
