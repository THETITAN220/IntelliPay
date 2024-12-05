import os
from mistralai import Mistral
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Set up the environment variable
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("API Key not found in environment variables")

# Initialize Mistral client
mistral_client = Mistral(api_key=api_key)
model = "mistral-large-latest"  # You can change the model if needed

# Telegram bot API key and username
API_KEY = "7580392807:AAFiy5dwqSlMbkoEwePhj1nLrndoN-ZCCqo"
BOT_USERNAME = '@IntelliPay_bot'

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to IntelliPay!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is the help section. Here are the available commands:\n"
                                    "/start - Start the bot\n"
                                    "/help - Display help information\n"
                                    "/custom - Custom command example")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command response.")

async def transaction_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You are a helpful transaction bot")

# Generate response using Mistral LLM
async def get_mistral_response(user_message: str):
    chat_response = mistral_client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": user_message}]
    )
    return chat_response.choices[0].message.content.strip()

# Define custom responses
custom_responses = {
    "What is your name?": "I am IntelliPay Bot, your assistant!",
    "Tell me a joke": "Why don't skeletons fight each other? They don't have the guts!",
    "What is AI?": "AI stands for Artificial Intelligence, a field of computer science focused on creating machines that can mimic human behavior.",
}

# Responses based on user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Check for custom responses
    response = custom_responses.get(text, None)
    
    # If no custom response is found, generate a response using Mistral
    if not response:
        response = await get_mistral_response(text)

    print('Bot:', response)
    if response:
        await update.message.reply_text(response)

# Error handling
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# MAIN
if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(API_KEY).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('transaction', transaction_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    app.add_error_handler(error)

    # Poll the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
