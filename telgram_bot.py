import nest_asyncio
nest_asyncio.apply()

import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import random
import string

TOKEN = "7482564575:AAE3OIzjltY51VB9O3DpHvyK-zJZWC2Jf-Y"

# Sessiya ma'lumotlari
sessions = {}

async def create_session(update: Update, context: CallbackContext):
    session_id, session_password = generate_session()
    user_id = update.message.chat.id

    sessions[session_id] = {
        "owner": user_id,
        "password": session_password,
        "guest": None
    }

    await update.message.reply_text(
        f"Sessiya yaratildi!\n\nHavola: https://t.me/virt_meetbot?start={session_id}\n"
        f"Parol: {session_password}\n"
        "Parolni shaxsiy ravishda ulashishingizni maslahat beramiz."
    )

def generate_session():
    session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    session_password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return session_id, session_password

async def join_session(update: Update, context: CallbackContext):
    user_input = context.args[0] if context.args else None
    if user_input:
        if user_input in sessions:
            session = sessions[user_input]

            if session["guest"] is None:
                await update.message.reply_text("Parolni kiriting:")
                context.user_data["pending_session"] = user_input
            else:
                await update.message.reply_text("Bu sessiya allaqachon band qilingan.")
        else:
            await update.message.reply_text("Noto'g'ri havola yoki sessiya mavjud emas.")
    else:
        await update.message.reply_text(
            "Xush kelibsiz! Sessiyaga qo'shilish uchun havola bilan /start komandasini ishlating."
        )

async def check_password(update: Update, context: CallbackContext):
    if "pending_session" in context.user_data:
        session_id = context.user_data["pending_session"]
        session = sessions[session_id]

        if update.message.text == session["password"]:
            session["guest"] = update.message.chat.id
            await update.message.reply_text("Sessiyaga muvaffaqiyatli ulandingiz!")
        else:
            await update.message.reply_text("Noto'g'ri parol. Qayta urinib ko'ring.")

async def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("create", create_session))
    application.add_handler(CommandHandler("start", join_session))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_password))

    await application.run_polling(timeout=60)

if __name__ == '__main__':
    asyncio.run(main())
