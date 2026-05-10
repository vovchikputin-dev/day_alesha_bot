import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from db import init_db, add_user, get_users

TOKEN = os.getenv("BOT_TOKEN")

TITLES = [
    "Алёша дня:",
    "Чебуречный сомелье:",
    "Сегодня останется трезвым:"
]

# сохраняем всех кто пишет
async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user:
        name = user.first_name or "Неизвестный"
        add_user(user.id, name)


async def alesha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = get_users()

    if len(users) < 1:
        await update.message.reply_text("В баре пока тишина... напишите что-нибудь 🍻")
        return

    # выбираем без повторов в одной выдаче
    pool = users.copy()

    a = random.choice(pool)
    pool.remove(a)

    b = random.choice(pool) if pool else a

    pool = users.copy()
    if a in pool:
        pool.remove(a)
    if b in pool:
        pool.remove(b)

    c = random.choice(pool) if pool else random.choice(users)

    text = (
        f"🍺 Бар «Алёша и графин» 🍺\n\n"
        f"{TITLES[0]} {a}\n"
        f"{TITLES[1]} {b}\n"
        f"{TITLES[2]} {c}"
    )

    await update.message.reply_text(text)


if __name__ == "__main__":
    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track))
    app.add_handler(CommandHandler("alesha", alesha))

    print("Bot started")
    app.run_polling()
