import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your tokens from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN") or "7763630340:AAEm0mlYbvKtEfysdErTm_wEWhVK0lhrS0U"
REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY") or "2ZetAtqQdSxbC9m3wC5hCdEH"

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "হ্যালো!\n"
        "আমি Background Remover Bot।\n"
        "আপনি আমাকে ছবি পাঠান, আমি তার ব্যাকগ্রাউন্ড মুছে দিয়ে ফিরিয়ে দিব।"
    )

def remove_bg(image_url: str) -> bytes:
    """Send image URL to remove.bg API and get result image bytes."""
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        data={'image_url': image_url, 'size': 'auto'},
        headers={'X-Api-Key': REMOVE_BG_API_KEY},
        stream=True,
    )
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Remove.bg API error: {response.status_code} {response.text}")

def handle_photo(update: Update, context: CallbackContext):
    message = update.message
    photo_file = message.photo[-1].get_file()
    photo_url = photo_file.file_path

    try:
        update.message.reply_text("Processing your image, please wait...")
        result_image = remove_bg(photo_url)

        # Send back the result
        update.message.reply_photo(photo=result_image, caption="এটা আপনার ব্যাকগ্রাউন্ড মুছে ফেলা ছবি।")

    except Exception as e:
        logger.error(f"Error removing background: {e}")
        update.message.reply_text("দুঃখিত, ব্যাকগ্রাউন্ড মুছে ফেলা সম্ভব হয়নি। আবার চেষ্টা করুন।")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()