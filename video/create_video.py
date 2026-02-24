import os
import requests
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import textwrap

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

def get_background_video(query="football stadium crowd", output_path="temp/bg.mp4"):
    os.makedirs("temp", exist_ok=True)
    
    if PEXELS_API_KEY:
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=3&orientation=landscape"
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if data.get("videos"):
            for video in data["videos"]:
                for vf in video["video_files"]:
                    if vf.get("width", 0) >= 1280:
                        video_url = vf["link"]
                        video_data = requests.get(video_url, timeout=30)
                        with open(output_path, "wb") as f:
                            f.write(video_data.content)
                        return output_path
    return None

def create_intro_image(title, subtitle, width=1920, height=1080):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    
    # Gradient overlay
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    
    for i in range(height):
        alpha = int(200 * (i / height))
        draw_overlay.line([(0, i), (width, i)], fill=(10, 20, 50, alpha))
    
    img = Image.alpha_composite(img, overlay)
    
    # Green accent bar at top
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (width, 12)], fill=(0, 200, 80, 255))
    draw.rectangle([(0, height-12), (width, height)], fill=(0, 200, 80, 255))
    
    # Title
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
        sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 45)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
    except:
        title_font = ImageFont.load_default()
        sub_font = title_font
        small_font = title_font
    
    # Main title center
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    tx = (width - tw) // 2
    
    # Shadow
    draw.text((tx+4, 354), title, font=title_font, fill=(0, 0, 0, 180))
    draw.text((tx, 350), title, font=title_font, fill=(255, 255, 255, 255))
    
    # Green underline
    draw.rectangle([(tx, 455), (tx+tw, 462)], fill=(0, 200, 80, 255))
    
    # Subtitle
    bbox2 = draw.textbbox((0, 0), subtitle, font=sub_font)
    sw = bbox2[2] - bbox2[0]
    sx = (width - sw) // 2
    draw.text((sx, 490), subtitle, font=sub_font, fill=(180, 220, 180, 255))
    
    # Bottom tag
    tag = "⚽ SPORTS ANALYTICS"
    bbox3 = draw.textbbox((0, 0), tag, font=small_font)
    tagw = bbox3[2] - bbox3[0]
    draw.text(((width - tagw)//2, 950), tag, font=small_font, fill=(0, 200, 80, 200))
    
    output = "temp/intro.png"
    img.save(output)
    return output

def create_content_image(text, chunk_num, total_chunks, width=1920, height=1080):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    
    # Dark overlay
    overlay = Image.new("RGBA", (width, height), (5, 15, 40, 210))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    # Side accent
    draw.rectangle([(0, 0), (8, height)], fill=(0, 200, 80, 255))
    
    # Progress bar at bottom
    progress = int((chunk_num / total_chunks) * width)
    draw.rectangle([(0, height-8), (width, height)], fill=(30, 30, 60, 255))
    draw.rectangle([(0, height-8), (progress, height)], fill=(0, 200, 80, 255))
    
    try:
        content_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 52)
        num_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    except:
        content_font = ImageFont.load_default()
        num_font = content_font
    
    # Wrap text
    wrapped = textwrap.fill(text, width=40)
    lines = wrapped.split('\n')
    
    line_height = 65
    total_text_height = len(lines) * line_height
    start_y = (height - total_text_height) // 2
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=content_font)
        lw = bbox[2] - bbox[0]
        lx = (width - lw) // 2
        ly = start_y + (i * line_height)
        
        # Shadow
        draw.text((lx+3, ly+3), line, font=content_font, fill=(0, 0, 0, 150))
        draw.text((lx, ly), line, font=content_font, fill=(255, 255, 255, 255))
    
    # Chunk counter
    counter = f"{chunk_num}/{total_chunks}"
    draw.text((width-120, 30), counter, font=num_font, fill=(100, 100, 100, 200))
    
    output = f"temp/content_{chunk_num}.png"
    img.save(output)
    return output

def create_outro_image(channel_link, width=1920, height=1080):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    overlay = Image.new("RGBA", (width, height), (5, 15, 40, 230))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([(0, 0), (width, 12)], fill=(0, 200, 80, 255))
    draw.rectangle([(0, height-12), (width, height)], fill=(0, 200, 80, 255))
    
    try:
        big_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 75)
        med_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
        link_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 45)
    except:
        big_font = ImageFont.load_default()
        med_font = big_font
        link_font = big_font
    
    texts = [
        ("THANK YOU FOR WATCHING!", big_font, (255, 255, 255, 255), 300),
        ("Daily Football Analytics", med_font, (180, 220, 180, 255), 420),
        ("Join our channel for more:", med_font, (150, 150, 150, 200), 540),
        (channel_link, link_font, (0, 220, 100, 255), 620),
        ("⚽ Like | Share | Subscribe", med_font, (200, 200, 200, 200), 750),
    ]
    
    for text, font, color, y in texts:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        tx = (width - tw) // 2
        draw.text((tx, y), text, font=font, fill=color)
    
    output = "temp/outro.png"
    img.save(output)
    return output

def create_video(script, audio_path, language="en", output_path=None):
    from config.settings import TELEGRAM_CHANNEL
    
    os.makedirs("temp", exist_ok=True)
    
    if output_path is None:
        output_path = f"temp/final_video_{language}.mp4"
    
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration
    
    # Background video
    bg_path = get_background_video()
    
    if bg_path and os.path.exists(bg_path):
        bg_clip = VideoFileClip(bg_path).without_audio()
        bg_clip = bg_clip.loop(duration=duration)
        bg_clip = bg_clip.resize((1920, 1080))
    else:
        bg_clip = ColorClip(size=(1920, 1080), color=(5, 15, 40), duration=duration)
    
    clips = [bg_clip]
    
    # Intro (first 4 seconds)
    intro_duration = min(4, duration * 0.15)
    lang_name = "বাংলা ফুটবল বিশ্লেষণ" if language == "bn" else "Football Analytics"
    intro_img = create_intro_image("⚽ TODAY'S MATCHES", lang_name)
    intro_clip = (ImageClip(intro_img)
                 .set_start(0)
                 .set_duration(intro_duration)
                 .set_opacity(0.92))
    clips.append(intro_clip)
    
    # Content chunks
    words = script.split()
    chunk_size = 25
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    
    content_start = intro_duration
    content_duration = duration - intro_duration - 4
    chunk_dur = content_duration / len(chunks)
    
    for i, chunk in enumerate(chunks):
        img_path = create_content_image(chunk, i+1, len(chunks))
        txt_clip = (ImageClip(img_path)
                   .set_start(content_start + i * chunk_dur)
                   .set_duration(chunk_dur)
                   .set_opacity(0.90)
                   .crossfadein(0.3))
        clips.append(txt_clip)
    
    # Outro (last 4 seconds)
    outro_start = duration - 4
    outro_img = create_outro_image(TELEGRAM_CHANNEL)
    outro_clip = (ImageClip(outro_img)
                 .set_start(outro_start)
                 .set_duration(4)
                 .set_opacity(0.92)
                 .crossfadein(0.5))
    clips.append(outro_clip)
    
    # Final render
    final = CompositeVideoClip(clips)
    final = final.set_audio(audio_clip)
    
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
    en_video = create_video(script_en, audio_en, "en", "temp/video_en.mp4")
    bn_video = create_video(script_bn, audio_bn, "bn", "temp/video_bn.mp4")
    return en_video, bn_video