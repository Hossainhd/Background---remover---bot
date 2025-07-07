import logging
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

import os
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY")

logging.basicConfig(level=logging.INFO)

def remove_bg(image_bytes):
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': image_bytes},
        data={'size': 'auto'},
        headers={'X-Api-Key': REMOVE_BG_API_KEY}
    )
    return response

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_data = requests.get(file.file_path).content

    await update.message.reply_text("⏳ ব্যাকগ্রাউন্ড রিমুভ করা হচ্ছে...")

    result = remove_bg(image_data)

    if result.status_code == 200:
        await update.message.reply_photo(photo=result.content, caption="✅ ব্যাকগ্রাউন্ড কাটা হয়েছে!")
    else:
        await update.message.reply_text(f"❌ ব্যর্থ: {result.status_code} - {result.text}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
