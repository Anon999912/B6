from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from urllib.parse import urlparse


# Function to extract the base URL
def extract_base_url(url: str) -> str:
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Send me a URL and I will extract the base URL!')


# Message handler for URLs
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text

    # Check if URL is valid
    if message.startswith("http://") or message.startswith("https://"):
        try:
            base_url = extract_base_url(message)
            await update.message.reply_text(f"Base URL: {base_url}")
        except Exception as e:
            await update.message.reply_text(f"Error parsing URL: {str(e)}")
    else:
        await update.message.reply_text("Please send a valid URL starting with http:// or https://")


# Main function to run the bot
def main():
    bot_token = 'YOUR_BOT_TOKEN_HERE'  # Replace with your Telegram bot token

    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()


if __name__ == '__main__':
    main()
