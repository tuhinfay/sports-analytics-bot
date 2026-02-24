from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def generate_script(matches, language="en"):
    """Match data niye AI script banabe"""
    
    if not matches:
        return None
    
    # Match data text e convert koro
    match_text = ""
    for match in matches:
        match_text += f"""
Match: {match['home_team']} vs {match['away_team']}
League: {match['league']}
Venue: {match['venue']}
Home Form (last 5): {match['home_form']}
Away Form (last 5): {match['away_form']}
"""

    if language == "bn":
        prompt = f"""
তুমি একজন বিশেষজ্ঞ ফুটবল বিশ্লেষক। নিচের ম্যাচগুলো নিয়ে বাংলায় একটি আকর্ষণীয় ভিডিও স্ক্রিপ্ট লেখো।

ম্যাচের তথ্য:
{match_text}

স্ক্রিপ্টে অবশ্যই থাকবে:
- আকর্ষণীয় ইন্ট্রো
- প্রতিটি ম্যাচের বিশ্লেষণ (ফর্ম, শক্তি, দুর্বলতা)
- আজকের সেরা ম্যাচ কোনটি
- আউট্রো

স্ক্রিপ্ট ৩০০-৪০০ শব্দের মধ্যে রাখো। শুধু স্ক্রিপ্ট লেখো, অন্য কিছু না।
"""
    else:
        prompt = f"""
You are an expert football analyst. Write an engaging video script in English about today's matches.

Match Data:
{match_text}

Script must include:
- Catchy intro
- Analysis of each match (form, strengths, weaknesses)
- Best match of the day
- Outro

Keep script between 300-400 words. Write only the script, nothing else.
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7
    )
    
    return response.choices[0].message.content

def generate_title_and_description(script, language="en"):
    """Video title and description banabe"""
    
    if language == "bn":
        prompt = f"""
এই স্ক্রিপ্টের জন্য YouTube এর জন্য লেখো:
1. একটি আকর্ষণীয় টাইটেল (৬০ অক্ষরের মধ্যে)
2. একটি description (১৫০ শব্দ)
3. ১০টি tags (কমা দিয়ে আলাদা)

স্ক্রিপ্ট: {script[:500]}

Format:
TITLE: ...
DESCRIPTION: ...
TAGS: ...
"""
    else:
        prompt = f"""
For this script write for YouTube:
1. An engaging title (under 60 chars)
2. A description (150 words)
3. 10 tags (comma separated)

Script: {script[:500]}

Format:
TITLE: ...
DESCRIPTION: ...
TAGS: ...
"""
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7
    )
    
    return response.choices[0].message.content
