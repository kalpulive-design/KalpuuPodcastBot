import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

API_ID = 22146561
API_HASH = "031377061c6714e885782314c414dcd1"
BOT_TOKEN = "8643810259:AAFOGKJ4kAT93Mofdx-DLvmgutI_7bc4dTU"

ADMIN_ID = 8766444295

bot = Client(
    "PomPomBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

db = sqlite3.connect("pompom.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER
)
""")

db.commit()

def add_user(user_id):
    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    data = cursor.fetchone()

    if data is None:
        cursor.execute(
            "INSERT INTO users VALUES(?)",
            (user_id,)
        )
        db.commit()

def get_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

@bot.on_message(filters.command("start"))
async def start(client, message):

    add_user(message.from_user.id)

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎙 Podcast",
                callback_data="podcast"
            )
        ],
        [
            InlineKeyboardButton(
                "💎 VIP Plans",
                callback_data="plans"
            )
        ],
        [
            InlineKeyboardButton(
                "👑 Admin Panel",
                callback_data="admin"
            )
        ]
    ])

    await message.reply_text(
        f"""
👋 Hello {message.from_user.first_name}

🎙 Welcome To PomPom Podcast Bot
        """,
        reply_markup=buttons
    )

@bot.on_callback_query()
async def callbacks(client, query):

    data = query.data

    if data == "podcast":

        await query.message.reply_text(
            "🎙 New Podcast Uploaded"
        )

    elif data == "plans":

        await query.message.reply_text(
            """
💎 VIP Plans

30 Days = ₹99
90 Days = ₹199
365 Days = ₹499
            """
        )

    elif data == "admin":

        if query.from_user.id != ADMIN_ID:
            return await query.answer(
                "❌ You Are Not Admin",
                show_alert=True
            )

        total_users = len(get_users())

        await query.message.reply_text(
            f"👥 Total Users: {total_users}"
        )

print("✅ Bot Started")
bot.run()
