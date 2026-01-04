import os
import sys
import time
from telethon import TelegramClient, events

# ==========================================
#  1. THE ANARKY ASCII LIBRARY (20+ Designs)
# ==========================================

ASCII_LIST = [
    # 1. The Classic OS
    """
      (  )   (   )  )
     ) (   )  (  (
     ( )  (    ) )
     _____________
    <  ANARKY_OS  >
     -------------
    """,
    # 2. Circle A
    """
         ___
       //   \\\\
      ((  A  ))
       \\\\___//
        || ||
      NO MASTERS
    """,
    # 3. Skull & Crossbones
    """
      NO FUTURE
      _.--""--._
     /  _    _  \\
    |  (o)  (o)  |
     \\    __    /
      `-.____.-'
       /      \\
    """,
    # 4. System Failure
    """
    [ SYSTEM FAILURE ]
    [ REBOOTING...   ]
    [ ERROR: 404     ]
    [ CHAOS: 100%    ]
    """,
    # 5. Biohazard
    """
       .   .
     '.  _  .'
    -=  ( )  =-
     .'  |  '.
       '   '
    [ TOXIC USER ]
    """,
    # 6. Glitch Text
    """
    A N A R K Y
    N A R K Y A
    A R K Y A N
    R K Y A N A
    K Y A N A R
    Y A N A R K
    """,
    # 7. Tombstone
    """
          /""\\
         /    \\
        | R.I.P |
        | ORDER |
        |_______|
    """,
    # 8. Middle Finger
    """
        ......
      .:      :.
    .:  CHAOS  :.
      ':.    .:'
         '::'
          ||
      F*CK THE SYSTEM
    """,
    # 9. Radioactive
    """
        _  _
       ( \/ )
       _\  /_
      (_/  \_)
     RADIOACTIVE
    """,
    # 10. Minimal Vibe
    """
    /// ANARKY ///
    /// ONLINE ///
    /// LEGEND ///
    """,
    # 11. Minimal A
    """
       /\\
      /  \\
     / /\\ \\
    / /  \\ \\
    \/    \/
    """,
    # 12. The Eye
    """
       .-.
      (o o)
      | O |
      \   /
       `-'
    I SEE YOU
    """,
    # 13. The Bomb
    """
         ,--.!,
      __/   -*-
    ,d08b.  '|`
    0088MM
    `9MMP'
    BOOM.
    """,
    # 14. The Mask
    """
      ,ad8888ba,
     d8"'    `"8b
    d8'        `8b
    88          88
    Y8,        ,8P
     Y8a.    .a8P
      `"Y8888Y"' 
    ANONYMOUS
    """,
    # 15. Binary Chaos
    """
    010101010101
    10 ANARKY 01
    010101010101
    [ HACKED ]
    """,
    # 16. The Flame
    """
        (
       . )
      ( (
       ) )
      ( (
    (_____)
    BURN IT
    """,
    # 17. The Spray Paint
    """
      ___________
     /           \\
    |   CHAOS     |
    |   REIGNS    |
     \___________/
         |||
         |||
    """,
    # 18. Broken Chain
    """
      __  __
     /  \/  \\
    |   ||   |
     \__/\__/
      BROKEN
    """,
    # 19. The Dagger
    """
        |
       |||
       |||
       |||
       |||
      \___/
     STRIKE
    """,
    # 20. The Crown (Inverted)
    """
     \ / \ /
      |___|
      KINGS
      MUST
      DIE
    """
]

# ==========================================
#  2. TEXT ASSETS (Startup Captions)
# ==========================================

STARTUP_CAPTIONS = [
    (
        "**ANARKY ONLINE** 💀\n\n"
        "Batman is just a rich furry with abandonment issues.\n"
        "Superman wears his underwear on the outside.\n"
        "**ANARKY is the only true philosophy.**\n\n"
        "System: `READY TO BURN`"
    ),
    (
        "**SYSTEM BREACHED** 🧨\n\n"
        "Iron Man died for a plot device.\n"
        "Captain America is a government puppet.\n"
        "**Only ANARKY brings true freedom.**\n\n"
        "Mode: `CHAOS`"
    ),
    (
        "**PROTOCOL: DESTRUCTION** 🔌\n\n"
        "Thanos was an amateur. I don't need a gauntlet to break things.\n"
        "The Justice League is just a PR stunt.\n"
        "**Hail ANARKY.**\n\n"
        "Status: `LEGENDARY`"
    ),
    (
        "**WAKE UP, SAMURAI** ⚔️\n\n"
        "Aquaman talks to fish because humans hate him.\n"
        "The Flash runs fast to escape his bad writers.\n"
        "**ANARKY is the cure.**\n\n"
        "Ping: `NEGATIVE`"
    )
]

CMD_LIST = {}
START_TIME = time.time()

# Simple Roasts for .alive command
ROASTS = [
    "Batman has more unresolved issues than this code.",
    "Superman is just a solar-powered Boy Scout.",
    "Iron Man is proof money can't buy a personality.",
    "The Flash runs fast to escape plot holes.",
    "Captain America is a glorified frisbee thrower.",
    "Thanos did nothing wrong.",
    "Joker isn't crazy, he's just WOKE.",
    "Deadpool wrote this line."
]

MOODS = [
    "Homicidal", "Plotting World Domination", "Craving Chaos", 
    "Debugging Reality", "Deleting Hope", "Trolling Heroes"
]

# ==========================================
#  3. CONFIG & CLIENT
# ==========================================

def get_config(name, prompt_msg):
    val = os.environ.get(name)
    if val: return val
    try:
        val = input(f"{prompt_msg}: ")
        if not val: sys.exit(1)
        return val
    except: sys.exit(1)

def get_readable_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return f"{int(d)}d {int(h)}h {int(m)}m {int(s)}s"

print(">> CORE: LOADING SYSTEM...")

try:
    API_ID = int(get_config("API_ID", "Enter API_ID"))
except: sys.exit(1)
API_HASH = get_config("API_HASH", "Enter API_HASH")

client = TelegramClient('anarky_session', API_ID, API_HASH)

def register(pattern, help_text):
    def decorator(func):
        cmd_name = pattern.replace('^\\.', '.').replace('$', '').split()[0]
        CMD_LIST[cmd_name] = help_text
        client.add_event_handler(func, events.NewMessage(outgoing=True, pattern=pattern))
        return func
    return decorator