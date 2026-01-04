import os
import requests
import asyncio
import random
from core import register, client

# ==========================================
#  ROASTS: VISION & MEDIA EDITION
# ==========================================
MEDIA_ROASTS = [
    "Daredevil is blind and even he can see you didn't reply to an image. 🦯",
    "Heimdall sees everything in the Nine Realms, but even he can't find the file. 👁️",
    "Are you trying to upload the Invisible Woman? Because I see nothing. 👻",
    "You are hallucinating files like Mysterio is tricking you. Reply to an actual image. 🔮",
    "Jarvis scan complete: 0% Media found, 100% Stupidity detected. 🤖",
    "Your brain is lagging harder than Cyberpunk on launch day. REPLY TO MEDIA. 💿",
    "Batman is the World's Greatest Detective, and even he is confused by your incompetence. 🦇",
    "Did Thanos snap away the image? Or did you just forget it? 🫰",
    "You possess the wisdom of Solomon (Shazam), yet you forgot to reply to a photo. ⚡",
    "Star-Lord dropped the Orb. You dropped the ball. Reply to something! 🌌",
    "Ultron decided humanity must be destroyed after seeing this attempt. 🦾",
    "Spider-Man used his web-shooters... but you have nothing to attach to. 🕸️",
    "Loki is casting illusions, or you just forgot how to use a bot. 🐍",
    "I can do this all day (Captain America), but I'd prefer if you actually replied to an image. 🛡️"
]

@register(pattern=r"^\.telegraph(?: |$)(.*)", help_text="Convert image to URL")
async def telegraph_cmd(event):
    # 1. Check if user replied to a message
    if not event.reply_to_msg_id:
        await handle_error(event, "Target Missing")
        return

    reply_msg = await event.get_reply_message()

    # 2. Check if the reply actually has media (Photo/Sticker/Gif)
    if not reply_msg.media:
        await handle_error(event, "Invalid Media Type")
        return

    # 3. Execution: Download & Upload
    try:
        await event.edit("`Downloading asset...`")
        
        # Download media to local server
        file_path = await client.download_media(reply_msg)
        
        await event.edit("`Uploading to Cloud...`")
        
        # Upload to Telegraph
        upload_url = upload_to_telegraph(file_path)
        
        # Cleanup (Delete local file to save space)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Success Message
        await event.edit(f"**🔗 ANARKY CLOUD UPLOAD**\n\n"
                         f"🔹 **Status:** `Online`\n"
                         f"🔹 **Link:** [Click Here]({upload_url})\n\n"
                         f"`{upload_url}`")
                         
    except Exception as e:
        await event.edit(f"**❌ UPLOAD FAILED**\n\n`Error: {e}`")

# ==========================================
#  HELPER FUNCTIONS
# ==========================================

async def handle_error(event, error_type):
    """The Roast & Guide Logic"""
    roast = random.choice(MEDIA_ROASTS)
    
    # Typing Animation
    await event.edit(f"`Analyzing {error_type}...`")
    await asyncio.sleep(0.5)
    await event.edit("`Searching for brain cells...`")
    await asyncio.sleep(0.5)
    
    # Final Message
    await event.edit(f"**⚠️ ERROR: {error_type.upper()}**\n\n"
                     f"_{roast}_\n\n"
                     f"**Guide:**\n"
                     f"1. Find an Image/Sticker.\n"
                     f"2. Reply to it.\n"
                     f"3. Type `.telegraph`")

def upload_to_telegraph(file_path):
    """Uploads file to telegra.ph and returns URL"""
    url = "https://telegra.ph/upload"
    files = {'file': ('file', open(file_path, 'rb'), 'image/jpeg')}
    
    # Requests library handles the multipart upload
    response = requests.post(url, files=files)
    key = response.json()[0]['src']
    return f"https://telegra.ph{key}"
