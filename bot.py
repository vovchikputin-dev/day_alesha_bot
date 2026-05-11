import os
import random

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from db import init_db, add_user, get_users

TOKEN = os.getenv("BOT_TOKEN")

TITLES = [
    "Алёша дня:",
    "Чебуречный сомелье:",
    "Сегодня останется трезвым:"
]

FUN_LINES = [
    "ушёл в графин и не вернулся",
    "официально подозрительно трезв",
    "опять заказал чебуреки на всех",
    "говорит, что только по пиву"
]


# сохраняем пользователей ПО ЧАТАМ
async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if user and chat:
        name = user.first_name or "Неизвестный"

        add_user(
            chat.id,
            user.id,
            name
        )


# команда /alesha
async def alesha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    users = get_users(chat.id)

    if len(users) < 1:
        await update.message.reply_text(
            "🍺 В кабаке пока тихо..."
        )
        return

    pool = users.copy()

    a = random.choice(pool)

    if a in pool:
        pool.remove(a)

    b = random.choice(pool) if pool else a

    if b in pool:
        pool.remove(b)

    c = random.choice(pool) if pool else a

 text = (
    f"🍺 Народный кабак «Алёша и графин» 🍺\n\n"

    f"{shuffled_titles[0]} {selected_users[0]}\n"
    f"— {random.choice(FUN_LINES)}\n\n"

    f"{shuffled_titles[1]} {selected_users[1]}\n"
    f"— {random.choice(FUN_LINES)}\n\n"

    f"{shuffled_titles[2]} {selected_users[2]}\n"
    f"— {random.choice(FUN_LINES)}"
)

    await update.message.reply_text(text)


if __name__ == "__main__":
    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            track
        )
    )

    app.add_handler(
        CommandHandler("alesha", alesha)
    )

    print("Bot started")

    app.run_polling()
