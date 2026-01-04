import os
import sys
import glob
import time
import random
import asyncio
import datetime
import importlib
import urllib.request

# Import from CORE
from core import (
    client, register, CMD_LIST, 
    ROASTS, MOODS, ASCII_LIST, STARTUP_CAPTIONS, # Imported new list
    START_TIME, get_readable_time
)

# ==========================================
#  BASE COMMANDS
# ==========================================

@register(pattern=r"^\.ping$", help_text="Check bot latency")
async def ping_cmd(event):
    start = datetime.datetime.now()
    animation = ["**Pinging...**", "**Pinging.**", "**Pinging..**", "**PONG!** 🏓"]
    for frame in animation:
        await event.edit(frame)
        await asyncio.sleep(0.1)
    end = datetime.datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(f"**🏓 PONG!**\n\n`Latency: {ms}ms`\n\n_{random.choice(ROASTS)}_")

@register(pattern=r"^\.alive$", help_text="Check status")
async def alive_cmd(event):
    await event.edit("**ANARKY IS ONLINE...**")
    await asyncio.sleep(0.5)
    
    chosen_ascii = random.choice(ASCII_LIST)
    chosen_roast = random.choice(ROASTS)
    
    if os.path.exists('anarky.jpg'):
        await client.send_file(
            event.chat_id, 'anarky.jpg', 
            caption=f"**I am here.**\n\n_{chosen_roast}_\n\n`Status: LEGENDARY`"
        )
        await event.delete()
    else:
        await event.edit(f"```\n{chosen_ascii}\n```\n**SYSTEM STATUS: ONLINE**\n_{chosen_roast}_")

@register(pattern=r"^\.status$", help_text="System stats")
async def status_cmd(event):
    await event.edit("`Fetching Stats...`")
    uptime = get_readable_time(time.time() - START_TIME)
    status_msg = (
        f"**💀 ANARKY STATS**\n"
        f"━━━━━━━━━━━━━━\n"
        f"⏱ **Uptime:** `{uptime}`\n"
        f"🧠 **Mood:** `{random.choice(MOODS)}`\n"
        f"🐍 **Python:** `{sys.version.split()[0]}`\n"
        f"━━━━━━━━━━━━━━\n"
        f"_{random.choice(ROASTS)}_"
    )
    await event.edit(status_msg)

@register(pattern=r"^\.restart$", help_text="Reboot system")
async def restart_cmd(event):
    await event.edit(f"**⚠️ SYSTEM REBOOT INITIATED...**")
    os.execl(sys.executable, sys.executable, *sys.argv)

@register(pattern=r"^\.commands$", help_text="List all commands")
async def help_cmd(event):
    await event.edit("`Accessing Database...`")
    cmd_string = "**🏴‍☠️ ANARKY COMMAND LIST**\n\n"
    for cmd, desc in CMD_LIST.items():
        cmd_string += f"🔹 `{cmd}` : {desc}\n"
    cmd_string += f"\n_{random.choice(ROASTS)}_"
    await event.edit(cmd_string)

@register(pattern=r"^\.whois$", help_text="Get user info")
async def whois_cmd(event):
    if not event.reply_to_msg_id:
        await event.edit("`Reply to someone.`")
        return
    try:
        await event.edit("`Accessing criminal records...`")
        reply_msg = await event.get_reply_message()
        user = await client.get_entity(reply_msg.sender_id)
        info_text = (
            f"**🕵️‍♂️ TARGET IDENTIFIED**\n"
            f"━━━━━━━━━━━━━━\n"
            f"👤 **Name:** {user.first_name} {user.last_name or ''}\n"
            f"🆔 **ID:** `{user.id}`\n"
            f"🤖 **Bot:** {user.bot}\n"
            f"🔗 **Username:** @{user.username if user.username else 'None'}\n"
            f"━━━━━━━━━━━━━━\n"
            f"_{random.choice(ROASTS)}_"
        )
        await event.edit(info_text)
    except Exception as e:
        await event.edit(f"`Error: {e}`")

@register(pattern=r"^\.purge (\d+)$", help_text="Delete X messages")
async def purge_cmd(event):
    count = int(event.pattern_match.group(1))
    await event.delete()
    await client.delete_messages(event.chat_id, range(event.id - count, event.id))
    msg = await event.respond(f"**🗑 Purged {count} messages.**")
    await asyncio.sleep(3)
    await msg.delete()

@register(pattern=r"^\.mock$", help_text="mOcK tExT sTyLe")
async def mock_cmd(event):
    if not event.reply_to_msg_id:
        await event.edit("`Reply to a message.`")
        return
    reply_msg = await event.get_reply_message()
    text = reply_msg.text
    mock_text = "".join([c.lower() if i % 2 == 0 else c.upper() for i, c in enumerate(text)])
    await event.delete()
    await reply_msg.reply(mock_text)

# ==========================================
#  PLUGIN LOADER
# ==========================================

def load_plugins():
    print(">> SCANNING PLUGINS...")
    if not os.path.exists("plugins"):
        os.makedirs("plugins")
        print(">> Created 'plugins' folder.")

    plugin_files = glob.glob("plugins/*.py")
    for file_path in plugin_files:
        filename = os.path.basename(file_path)
        module_name = filename[:-3] 
        if module_name == "__init__": continue
        try:
            importlib.import_module(f"plugins.{module_name}")
            print(f"   [+] Loaded: {module_name}")
        except Exception as e:
            print(f"   [!] FAILED {module_name}: {e}")

# ==========================================
#  MAIN STARTUP (THE LOGIC YOU ASKED FOR)
# ==========================================

async def main():
    print(">> CONNECTING TO TELEGRAM...")
    await client.start()
    
    # 1. Image Check & Auto-Download
    if not os.path.exists('anarky.jpg') or os.path.getsize('anarky.jpg') < 1000:
        print(">> 'anarky.jpg' missing/corrupt. Attempting download...")
        try:
            url = "https://raw.githubusercontent.com/SUBHxTREM/ANARKY/main/anarky.jpg"
            urllib.request.urlretrieve(url, 'anarky.jpg')
            print(">> Download attempted.")
        except: pass

    # 2. Pick Random Assets
    random_ascii = random.choice(ASCII_LIST)
    random_caption = random.choice(STARTUP_CAPTIONS) # Roasts Marvel/DC + Praises Anarky
    
    # 3. Send Logic
    try:
        # CONDITION 1: Image Found -> Send Image + Text
        if os.path.exists('anarky.jpg') and os.path.getsize('anarky.jpg') > 0:
            await client.send_file(
                'me', 
                'anarky.jpg', 
                caption=random_caption
            )
            print(">> STARTUP: Image + Caption Sent.")
            
        # CONDITION 2: Image Not Found -> Send Text + ASCII Banner
        else:
            print(">> WARNING: Image missing. Sending ASCII Mode.")
            # Combine the ASCII art with the roasting text
            ascii_msg = f"```\n{random_ascii}\n```\n{random_caption}"
            await client.send_message('me', ascii_msg)
            
    except Exception as e:
        print(f">> FATAL ERROR sending startup msg: {e}")
        try:
            # Emergency Fallback
            await client.send_message('me', random_caption)
        except: pass

    print(">> ANARKY IS ALIVE. (Ctrl+C to stop)")
    await client.run_until_disconnected()

if __name__ == '__main__':
    load_plugins()
    client.loop.run_until_complete(main())