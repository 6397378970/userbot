from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import random
import re
from config import Config
from ai_handler import AIHandler

app = Client("userbot", session_string=Config.STRING_SESSION)
ai = AIHandler()

# Store user's DM status (group joined or not)
dm_status = {}

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.reply(f"👋 Hi! I'm {Config.BOT_NAME}, a {Config.BOT_GENDER} bot.\n\nPlease join our group first: {Config.REQUIRED_GROUP}")

@app.on_message(filters.private & ~filters.command("start"))
async def private_chat(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # Check if user joined the group
    try:
        member = await client.get_chat_member(Config.REQUIRED_GROUP.split("/")[-1], user_id)
        if member:
            # User joined, reply normally
            response = ai.get_ai_response(message.text, user_name)
            await message.reply(response)
    except:
        # User hasn't joined
        await message.reply(f"❌ Please join our group first to chat with me!\n\n{Config.REQUIRED_GROUP}")

@app.on_message(filters.group | filters.channel)
async def group_chat(client, message):
    # Ignore bot's own messages
    if message.from_user and message.from_user.id == app.me.id:
        return
    
    user_name = message.from_user.first_name if message.from_user else "Someone"
    should_reply = False
    reply_text = None
    
    # 1️⃣ Check if @mentioned
    if message.mentioned:
        should_reply = True
    
    # 2️⃣ Check if replied to bot
    if message.reply_to_message and message.reply_to_message.from_user.id == app.me.id:
        should_reply = True
    
    # 3️⃣ Check if bot name mentioned in text
    if message.text and Config.BOT_NAME.lower() in message.text.lower():
        should_reply = True
    
    # 4️⃣ Random reply (30% chance) - Random bande ko reply
    if random.random() < 0.3 and not should_reply:
        should_reply = True
    
    # 5️⃣ Handle stickers - Reply with same sticker
    if message.sticker:
        await message.reply_sticker(message.sticker.file_id)
        return
    
    # If should reply, generate response
    if should_reply and message.text:
        # Check if it's a command or query
        response = ai.get_ai_response(message.text, user_name)
        
        # Sometimes add flirty responses if user is flirting
        flirty_words = ['love', 'baby', 'cutie', 'handsome', 'beautiful', 'sexy']
        if any(word in message.text.lower() for word in flirty_words):
            flirty_responses = [
                f"😉 Aap bhi na {user_name}",
                f"{user_name} ji, itna mat boliye 🥰",
                f"Arre {user_name}, shy kar diya aapne 😊",
                f"Main toh {Config.BOT_GENDER} hoon, par aapke liye special 😘"
            ]
            if random.random() < 0.5:
                response = random.choice(flirty_responses)
        
        await asyncio.sleep(random.uniform(1, 3))  # Human-like delay
        await message.reply(response)

@app.on_message(filters.private & filters.sticker)
async def private_sticker(client, message):
    # Reply with same sticker in DM
    await message.reply_sticker(message.sticker.file_id)

@app.on_message(filters.group & filters.sticker)
async def group_sticker(client, message):
    # Reply with same sticker if someone sends sticker in group
    if random.random() < 0.4:  # 40% chance to reply with same sticker
        await asyncio.sleep(random.uniform(1, 2))
        await message.reply_sticker(message.sticker.file_id)

if __name__ == "__main__":
    print(f"🤖 {Config.BOT_NAME} UserBot Started!")
    print(f"📌 Gender: {Config.BOT_GENDER}")
    print(f"🤖 AI Provider: {Config.ACTIVE_AI}")
    print("✅ Bot is running...")
    app.run()
