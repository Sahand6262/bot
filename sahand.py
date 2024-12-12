import firebase_admin
from firebase_admin import credentials, firestore
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Firebase setup
cred = credentials.Certificate('barber-c4424-firebase-adminsdk-meiwp-e73b31a900.json')  # Path to your Firebase JSON file
firebase_admin.initialize_app(cred)

db = firestore.client()

# Telegram Bot Token
TELEGRAM_TOKEN = '7757338138:AAEjSR7lj8sgsiN8kbrn7elT3WXgXlY5nxU'

# Set up logging to get more details about errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to fetch bookings for today and tomorrow
def fetch_bookings():
    from datetime import date, timedelta
    today = date.today()
    tomorrow = today + timedelta(days=1)

    today_formatted = today.strftime('%Y-%m-%d')
    tomorrow_formatted = tomorrow.strftime('%Y-%m-%d')

    bookings_ref = db.collection("bookings")
    query = bookings_ref.where("date", "in", [today_formatted, tomorrow_formatted])

    query_snapshot = query.stream()

    bookings = []
    for doc in query_snapshot:
        booking = doc.to_dict()
        bookings.append(booking)

    return bookings

# Function to send bookings to the Telegram chat
async def send_bookings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bookings = fetch_bookings()

    if not bookings:
        await update.message.reply_text("No bookings for today or tomorrow.")
        return

    message = "Bookings for Today & Tomorrow:\n\n"
    for booking in bookings:
        message += f"Name: {booking['firstName']} {booking['lastName']}\n"
        message += f"Email: {booking['email']}\n"
        message += f"Phone: {booking['phone']}\n"
        message += f"Date: {booking['date']}\n"
        message += f"Time Slot: {booking['timeSlot']}\n\n"

    await update.message.reply_text(message)

# Command handler for /getbookings
async def get_bookings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_bookings(update, context)

# Function to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /getbookings to get today's and tomorrow's bookings.")

# Main function to start the bot
def main():
    # Set up the application (replaces Updater in v20+)
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getbookings", get_bookings))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
