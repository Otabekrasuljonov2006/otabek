


from telegram import Update
from telegram.ext import CommandHandler, Application, CallbackContext

# Tokeningizni o'zgartiring
TOKEN = "7911991526:AAGQDihTE5RLLhhbL9fwMBpszm3AH7hawGc"

# /start komandasi uchun callback funksiyasi
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Salom! Bot ishga tushdi!")

def main():
    """Botni ishga tushirish."""
    # Application yaratish (yangilangan versiya)
    application = Application.builder().token(TOKEN).build()

    # Dispatcher orqali handler qo'shish
    application.add_handler(CommandHandler("start", start))

    # Botni polling yordamida ishga tushurish
    application.run_polling()

if __name__ == '__main__':
    main()
