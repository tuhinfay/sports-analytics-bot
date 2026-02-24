import os
import requests
import subprocess
from datetime import datetime
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

# BBC/Sky Sports color scheme
COLORS = {
    "bg_dark": (8, 15, 35),
    "bg_mid": (15, 25, 55),
    "accent": (0, 180, 255),      # Sky blue
    "accent2": (255, 60, 60),     # Red
    "green": (0, 220, 80),
    "white": (255, 255, 255),
    "gray": (150, 160, 180),
    "gold": (255, 200, 0),
    "card_bg": (20, 35, 70),
}

W, H = 1920, 1080

def load_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill, outline=None, outline_width=2):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=outline_width)

def paste_logo(img, logo_path, position, size=(120, 120)):
    try:
        if logo_path and os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            logo = logo.resize(size, Image.LANCZOS)
            img.paste(logo, position, logo)
    except:
        pass

def get_background_video(output_path="temp/bg.mp4"):
    os.makedirs("temp", exist_ok=True)
    if PEXELS_API_KEY:
        headers = {"Authorization": PEXELS_API_KEY}
        queries = ["football stadium lights", "soccer match crowd", "football pitch"]
        for query in queries:
            try:
                url = f"https://api.pexels.com/videos/search?query={query}&per_page=3&orientation=landscape"
                response = requests.get(url, headers=headers, timeout=15)
                data = response.json()
                if data.get("videos"):
                    for video in data["videos"]:
                        for vf in video["video_files"]:
                            if vf.get("width", 0) >= 1280:
                                video_data = requests.get(vf["link"], timeout=30)
                                with open(output_path, "wb") as f:
                                    f.write(video_data.content)
                                return output_path
            except:
                continue
    return None

def create_intro_frame(match, today_str):
    img = Image.new("RGBA", (W, H), (*COLORS["bg_dark"], 255))
    draw = ImageDraw.Draw(img)

    # Top bar
    draw.rectangle([(0, 0), (W, 70)], fill=(*COLORS["accent"], 255))
    draw.text((40, 15), "⚽  SPORTS ANALYTICS", font=load_font(32, bold=True), fill=(*COLORS["white"], 255))
    draw.text((W-300, 15), f"📅 {today_str}", font=load_font(28), fill=(*COLORS["white"], 200))

    # League badge
    draw_rounded_rect(draw, [W//2-200, 90, W//2+200, 150], 8,
                      fill=(*COLORS["accent"], 40), outline=(*COLORS["accent"], 180))
    draw.text((W//2, 120), match["league"], font=load_font(30, bold=True),
              fill=(*COLORS["accent"], 255), anchor="mm")

    # VS section
    center_y = 480

    # Home team card
    draw_rounded_rect(draw, [150, center_y-180, 750, center_y+180], 20,
                      fill=(*COLORS["card_bg"], 255), outline=(*COLORS["accent"], 100))
    paste_logo(img, match["home_logo"], (390, center_y-150), (180, 180))
    draw.text((450, center_y+50), match["home_team"], font=load_font(42, bold=True),
              fill=(*COLORS["white"], 255), anchor="mm")

    # Form badges home
    form = match.get("home_form", "")
    for i, r in enumerate(form[:5]):
        color = COLORS["green"] if r == "W" else COLORS["accent2"] if r == "L" else COLORS["gold"]
        draw_rounded_rect(draw, [220 + i*80, center_y+110, 285 + i*80, center_y+150], 8,
                          fill=(*color, 200))
        draw.text((252 + i*80, center_y+130), r, font=load_font(24, bold=True),
                  fill=(*COLORS["white"], 255), anchor="mm")

    # Away team card
    draw_rounded_rect(draw, [1170, center_y-180, 1770, center_y+180], 20,
                      fill=(*COLORS["card_bg"], 255), outline=(*COLORS["accent2"], 100))
    paste_logo(img, match["away_logo"], (1350, center_y-150), (180, 180))
    draw.text((1470, center_y+50), match["away_team"], font=load_font(42, bold=True),
              fill=(*COLORS["white"], 255), anchor="mm")

    # Form badges away
    form2 = match.get("away_form", "")
    for i, r in enumerate(form2[:5]):
        color = COLORS["green"] if r == "W" else COLORS["accent2"] if r == "L" else COLORS["gold"]
        draw_rounded_rect(draw, [1240 + i*80, center_y+110, 1305 + i*80, center_y+150], 8,
                          fill=(*color, 200))
        draw.text((1272 + i*80, center_y+130), r, font=load_font(24, bold=True),
                  fill=(*COLORS["white"], 255), anchor="mm")

    # VS circle
    draw.ellipse([870, center_y-70, 1050, center_y+70], fill=(*COLORS["accent2"], 220))
    draw.text((960, center_y), "VS", font=load_font(56, bold=True),
              fill=(*COLORS["white"], 255), anchor="mm")

    # Match info bottom
    draw_rounded_rect(draw, [W//2-400, H-180, W//2+400, H-100], 12,
                      fill=(*COLORS["card_bg"], 255))
    draw.text((W//2, H-140), f"🏟️  {match.get('venue', 'TBD')}",
              font=load_font(32), fill=(*COLORS["gray"], 255), anchor="mm")

    # Bottom bar
    draw.rectangle([(0, H-60), (W, H)], fill=(*COLORS["accent"], 255))
    draw.text((W//2, H-30), "ANALYSIS • STATS • PREDICTIONS",
              font=load_font(26, bold=True), fill=(*COLORS["white"], 255), anchor="mm")

    output = f"temp/intro_{match['home_id']}.png"
    img.save(output)
    return output

def create_stats_frame(match):
    img = Image.new("RGBA", (W, H), (*COLORS["bg_dark"], 255))
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([(0, 0), (W, 70)], fill=(*COLORS["accent"], 255))
    draw.text((W//2, 35), "📊  MATCH STATISTICS", font=load_font(34, bold=True),
              fill=(*COLORS["white"], 255), anchor="mm")

    home_stats = match.get("home_stats", {})
    away_stats = match.get("away_stats", {})

    stats_data = [
        ("Goals Scored", home_stats.get("goals_for", 0), away_stats.get("goals_for", 0)),
        ("Goals Conceded", home_stats.get("goals_against", 0), away_stats.get("goals_against", 0)),
        ("Wins", home_stats.get("wins", 0), away_stats.get("wins", 0)),
        ("Draws", home_stats.get("draws", 0), away_stats.get("draws", 0)),
        ("Losses", home_stats.get("loses", 0), away_stats.get("loses", 0)),
    ]

    # Team names
    draw.text((400, 110), match["home_team"], font=load_font(38, bold=True),
              fill=(*COLORS["accent"], 255), anchor="mm")
    draw.text((W-400, 110), match["away_team"], font=load_font(38, bold=True),
              fill=(*COLORS["accent2"], 255), anchor="mm")

    # Stat bars
    for i, (label, home_val, away_val) in enumerate(stats_data):
        y = 200 + i * 140
        total = max(home_val + away_val, 1)

        # Background
        draw_rounded_rect(draw, [100, y, W-100, y+90], 12,
                          fill=(*COLORS["card_bg"], 255))

        # Label
        draw.text((W//2, y+20), label, font=load_font(28, bold=True),
                  fill=(*COLORS["gray"], 255), anchor="mm")

        # Bar
        bar_w = W - 300
        home_w = int((home_val / total) * bar_w // 2)
        away_w = int((away_val / total) * bar_w // 2)

        mid = W // 2
        draw.rounded_rectangle([mid - home_w, y+50, mid, y+80],
                                radius=6, fill=(*COLORS["accent"], 220))
        draw.rounded_rectangle([mid, y+50, mid + away_w, y+80],
                                radius=6, fill=(*COLORS["accent2"], 220))

        # Values
        draw.text((mid - home_w - 20, y+65), str(home_val), font=load_font(28, bold=True),
                  fill=(*COLORS["white"], 255), anchor="rm")
        draw.text((mid + away_w + 20, y+65), str(away_val), font=load_font(28, bold=True),
                  fill=(*COLORS["white"], 255), anchor="lm")

    output = f"temp/stats_{match['home_id']}.png"
    img.save(output)
    return output

def create_analysis_frame(script_chunk, chunk_num, total):
    img = Image.new("RGBA", (W, H), (*COLORS["bg_dark"], 255))
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([(0, 0), (W, 70)], fill=(*COLORS["bg_mid"], 255))
    draw.rectangle([(0, 0), (8, H)], fill=(*COLORS["accent"], 255))
    draw.text((50, 35), "🎙️  ANALYSIS", font=load_font(30, bold=True),
              fill=(*COLORS["accent"], 255), anchor="lm")

    # Progress
    prog_w = int((chunk_num / total) * (W - 100))
    draw.rectangle([(50, H-20), (W-50, H-8)], fill=(*COLORS["card_bg"], 255))
    draw.rectangle([(50, H-20), (50 + prog_w, H-8)], fill=(*COLORS["accent"], 255))

    # Content card
    draw_rounded_rect(draw, [80, 100, W-80, H-60], 20,
                      fill=(*COLORS["card_bg"], 180))

    # Text
    wrapped = textwrap.fill(script_chunk, width=55)
    lines = wrapped.split('\n')
    line_h = 68
    total_h = len(lines) * line_h
    start_y = (H - total_h) // 2

    for i, line in enumerate(lines):
        y = start_y + i * line_h
        bbox = draw.textbbox((0, 0), line, font=load_font(48))
        lw = bbox[2] - bbox[0]
        lx = (W - lw) // 2
        draw.text((lx+3, y+3), line, font=load_font(48), fill=(0, 0, 0, 100))
        draw.text((lx, y), line, font=load_font(48), fill=(*COLORS["white"], 255))

    output = f"temp/analysis_{chunk_num}.png"
    img.save(output)
    return output

def create_outro_frame(channel_link, today_str):
    img = Image.new("RGBA", (W, H), (*COLORS["bg_dark"], 255))
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (W, 10)], fill=(*COLORS["accent"], 255))
    draw.rectangle([(0, H-10), (W, H)], fill=(*COLORS["accent"], 255))

    texts = [
        ("⚽", 140, load_font(100), COLORS["white"]),
        ("THANKS FOR WATCHING!", 280, load_font(72, bold=True), COLORS["white"]),
        ("Daily Football Analytics", 390, load_font(48), COLORS["accent"]),
        (f"📅 {today_str}", 470, load_font(38), COLORS["gray"]),
        ("━━━━━━━━━━━━━━━━━━━━━━━", 540, load_font(28), COLORS["card_bg"]),
        ("Join our Telegram for daily updates:", 600, load_font(38), COLORS["gray"]),
        (channel_link, 670, load_font(44, bold=True), COLORS["green"]),
        ("👍 Like  •  🔔 Subscribe  •  📤 Share", 780, load_font(36), COLORS["gray"]),
    ]

    for text, y, font, color in texts:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, y), text, font=font, fill=(*color, 255))

    output = "temp/outro.png"
    img.save(output)
    return output

def create_video(script, audio_path, match_data=None, language="en", output_path=None):
    from config.settings import TELEGRAM_CHANNEL
    os.makedirs("temp", exist_ok=True)
    os.makedirs("temp/logos", exist_ok=True)

    if output_path is None:
        output_path = f"temp/final_video_{language}.mp4"

    today_str = datetime.now().strftime("%d %B %Y")
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    bg_path = get_background_video()
    if bg_path and os.path.exists(bg_path):
        bg_clip = VideoFileClip(bg_path).without_audio().loop(duration=duration).resize((W, H))
        # Dark overlay on background
        overlay = ColorClip(size=(W, H), color=(8, 15, 35)).set_opacity(0.75).set_duration(duration)
        bg_final = CompositeVideoClip([bg_clip, overlay])
    else:
        bg_final = ColorClip(size=(W, H), color=COLORS["bg_dark"], duration=duration)

    clips = [bg_final]
    time_cursor = 0

    # Per match intro + stats
    if match_data:
        per_match_time = min(6, duration * 0.15)
        for match in match_data[:3]:
            intro_img = create_intro_frame(match, today_str)
            intro_clip = (ImageClip(intro_img)
                         .set_start(time_cursor)
                         .set_duration(per_match_time)
                         .crossfadein(0.4))
            clips.append(intro_clip)
            time_cursor += per_match_time

            stats_img = create_stats_frame(match)
            stats_clip = (ImageClip(stats_img)
                         .set_start(time_cursor)
                         .set_duration(per_match_time)
                         .crossfadein(0.4))
            clips.append(stats_clip)
            time_cursor += per_match_time

    # Analysis chunks
    words = script.split()
    chunk_size = 30
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    remaining = duration - time_cursor - 5
    chunk_dur = max(3, remaining / len(chunks))

    for i, chunk in enumerate(chunks):
        img = create_analysis_frame(chunk, i+1, len(chunks))
        c = (ImageClip(img)
             .set_start(time_cursor)
             .set_duration(chunk_dur)
             .crossfadein(0.3))
        clips.append(c)
        time_cursor += chunk_dur

    # Outro
    outro_img = create_outro_frame(TELEGRAM_CHANNEL, today_str)
    outro_clip = (ImageClip(outro_img)
                 .set_start(max(time_cursor, duration-5))
                 .set_duration(5)
                 .crossfadein(0.5))
    clips.append(outro_clip)

    final = CompositeVideoClip(clips).set_audio(audio_clip)
    final.write_videofile(output_path, fps=30, codec="libx264",
                         audio_codec="aac", verbose=False, logger=None)
    print(f"✅ Video created: {output_path}")
    return output_path

def create_both_videos(script_en, script_bn, audio_en, audio_bn, match_data=None):
    en_video = create_video(script_en, audio_en, match_data, "en", "temp/video_en.mp4")
    bn_video = create_video(script_bn, audio_bn, match_data, "bn", "temp/video_bn.mp4")
    return en_video, bn_video