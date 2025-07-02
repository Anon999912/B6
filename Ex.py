from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from urllib.parse import urlparse


# Function to extract the base URL
def extract_base_url(url: str) -> str:
    parsed_url = urlparse(url)
    if parsed_url.scheme and parsed_url.netloc:
        return f"{parsed_url.scheme}://{parsed_url.netloc}"
    else:
        return None


# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome! Send me a URL and I will extract the base URL.\n"
        "Or use /mass followed by multiple URLs separated by spaces."
    )


# Single URL message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text.strip()

    if message.startswith("http://") or message.startswith("https://"):
        base_url = extract_base_url(message)
        if base_url:
            await update.message.reply_text(f"Base URL: {base_url}")
        else:
            await update.message.reply_text("Could not parse the URL.")
    else:
        await update.message.reply_text("Please send a valid URL starting with http:// or https://")


# /mass command handler
async def mass(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args

    if not args:
        await update.message.reply_text("Please provide URLs after the command. Example:\n/mass url1 url2 url3")
        return

    base_urls = []
    for url in args:
        if url.startswith("http://") or url.startswith("https://"):
            base = extract_base_url(url)
            if base:
                base_urls.append(base)
            else:
                base_urls.append(f"Invalid URL: {url}")
        else:
            base_urls.append(f"Invalid URL: {url}")

    response = "Base URLs:\n" + "\n".join(base_urls)
    await update.message.reply_text(response)


# Main function to run the bot
def main():
    bot_token = 'YOUR_BOT_TOKEN_HERE'  # Replace with your Telegram bot token

    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mass", mass))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()


if __name__ == '__main__':
    main()
