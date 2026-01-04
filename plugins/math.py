import asyncio
import random
from core import register

# ==========================================
#  LIBRARY OF ROASTS (MARVEL/DC EDITION)
# ==========================================
MATH_ROASTS = [
    # CLASSICS
    "Tony Stark built a suit in a cave with scraps. You can't even type a formula. 🤖",
    "Dr. Strange viewed 14 million futures, and in none of them did this syntax work. 🔮",
    "You calculate like Thanos snapped away half your brain cells. 🫰",
    "Cyborg is processing... nope, your input is garbage. 🦾",
    "Shazam! You turned into an idiot. ⚡️",
    "Batman has a plan for everything, except your math skills. 🦇",
    "Even the Hulk knows 2+2. What is your excuse? 🟢",
    
    # NEW ADDITIONS
    "Even Groot has a better vocabulary than your math skills. I am Groot? 🌱",
    "Your logic is as invisible as Drax standing very still. 🗑️",
    "Professor X tried to read your mind but found a 404 Error. 🧠🚫",
    "You have the combined intelligence of the entire Suicide Squad... before they died. 💣",
    "Spider-Man's spider-sense is tingling... it detects pure stupidity. 🕷️",
    "Thor is worthy. You? You aren't even worthy of a calculator. 🔨",
    "Captain America was frozen for 70 years and still knows more math than you. 🧊",
    "Black Widow sacrificed herself for the Soul Stone, you sacrificed your brain for nothing. 🧗‍♀️",
    "Darkseid is searching for the Anti-Life Equation, you just found the Anti-Intelligence one. Ω",
    "Loki is the God of Mischief, you are the God of Mistakes. 🐍",
    "Deadpool is breaking the fourth wall just to laugh at this syntax. ⚔️",
    "Your brain is smaller than Ant-Man in the Quantum Realm. 🔬",
    "Wonder Woman's Lasso of Truth reveals... you have no idea what you're doing. 💫",
    "Daredevil can't see, but even he knows that syntax is wrong. 🦯",
    "Green Lantern needs willpower. You need a brain transplant. 💍",
    "Venom tried to bond with you but died of boredom. 🕷️",
    "The Riddler left a clue: 'Why are you so dumb?' ❓",
    "Bane broke the Bat, you just broke the bot. 🦇",
    "Alfred has more combat skills than you have math skills. ☕",
    "Star-Lord is an idiot, and even he is embarrassed for you. 🌌",
    "Rocket Raccoon wants to buy your brain... oh wait, it's worthless. 🦝",
    "Vision is an android with infinite knowledge. You are... well, you. 🤖",
    "Two-Face flipped a coin. Heads: You're dumb. Tails: You're stupid. 🪙",
    "Aquaman called. He wants his water back, your brain is drowning. 🌊",
    "Joker isn't laughing anymore. This is just sad. 🤡",
    "Superman is weak to Kryptonite. I am weak to your bad spelling. 💎",
    "Flash ran back in time to stop you from typing this... he failed. ⚡"
]

@register(pattern=r"^\.math(?: |$)(.*)", help_text="Solve math problems")
async def math_cmd(event):
    # 1. Get the input
    expression = event.pattern_match.group(1)
    
    # 2. Check for Missing Input (Error Handling)
    if not expression:
        # Pick a random roast from the huge list
        roast = random.choice(MATH_ROASTS)
        
        # Generate a "Smart" Random Example every time
        op = random.choice(['+', '-', '*', '/', '**'])
        n1 = random.randint(10, 999)
        n2 = random.randint(2, 9)
        example = f".math {n1} {op} {n2}"
        
        # Typing Animation (The "Smart" Feel)
        await event.edit("`Analyzing Syntax...`")
        await asyncio.sleep(0.5)
        await event.edit("`Detecting stupidity...`")
        await asyncio.sleep(0.5)
        
        # The Final Roast Message
        await event.edit(f"**⚠️ ERROR: BRAIN NOT FOUND**\n\n_{roast}_\n\n"
                         f"**Try this (Example):**\n`{example}`")
        return

    # 3. Execution Logic
    try:
        # Basic safety: remove dangerous keywords
        clean_exp = expression.replace("__", "").replace("import", "").replace("exec", "")
        
        # Evaluate the math
        result = eval(clean_exp)
        
        await event.edit(f"**🧮 ANARKY CALCULATOR**\n\n"
                         f"🔹 **Query:** `{expression}`\n"
                         f"🔹 **Result:** `{result}`")
                         
    except Exception as e:
        await event.edit(f"**❌ CALCULATION FAILED**\n\n"
                         f"Even J.A.R.V.I.S couldn't solve that.\n"
                         f"`Error: {e}`")
