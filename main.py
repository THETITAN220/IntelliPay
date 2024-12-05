import os
from mistralai import Mistral
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from web3 import Web3

# Set up the environment variable
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("API Key not found in environment variables")

# Initialize Mistral client
mistral_client = Mistral(api_key=api_key)
model = "mistral-large-latest"  # You can change the model if needed

# Initialize Web3 for Ethereum interaction
web3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/a4ce2d986f46429db51f1a2f60549dbd'))

# Telegram bot API key and username
API_KEY = "7580392807:AAFiy5dwqSlMbkoEwePhj1nLrndoN-ZCCqo"
BOT_USERNAME = '@IntelliPay_bot'

# User data storage
user_data = {}

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to IntelliPay! I can help you with crypto transactions.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is the help section. Here are the available commands:\n"
                                    "/start - Start the bot\n"
                                    "/help - Display help information\n"
                                    "/custom - Custom command example\n"
                                    "/check_balance - Check your crypto balance\n"
                                    "/make_transaction - Make a crypto transaction")

# Generate response using Mistral LLM
async def get_mistral_response(user_message: str):
    chat_response = mistral_client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": user_message}]
    )
    return chat_response.choices[0].message.content.strip()

# Handle checking balance
async def check_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    if user_id in user_data and user_data[user_id].get("crypto_address"):
        address = user_data[user_id]["crypto_address"]
        balance = web3.eth.get_balance(address)
        balance_in_ether = web3.fromWei(balance, 'ether')
        await update.message.reply_text(f"Your balance is {balance_in_ether} ETH.")
    else:
        await update.message.reply_text("Please provide your crypto address first using /set_address.")

# Handle making a transaction
async def make_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    if user_id in user_data and user_data[user_id].get("crypto_address"):
        await update.message.reply_text("Please provide the recipient's crypto address.")
        user_data[user_id]["awaiting_recipient"] = True
    else:
        await update.message.reply_text("Please provide your crypto address first using /set_address.")

# Set the user's crypto address
async def set_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    crypto_address = update.message.text.strip()

    if web3.isAddress(crypto_address):
        user_data[user_id] = {"crypto_address": crypto_address}
        await update.message.reply_text(f"Your crypto address has been set to {crypto_address}.")
    else:
        await update.message.reply_text("That is not a valid Ethereum address. Please try again.")

# Handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Check for custom responses
    response = None
    if text.lower() == "what is your name?":
        response = "I am IntelliPay Bot, your assistant!"
    elif text.lower() == "tell me a joke":
        response = "Why don't skeletons fight each other? They don't have the guts!"
    elif text.lower() == "what is ai?":
        response = "AI stands for Artificial Intelligence, a field of computer science focused on creating machines that can mimic human behavior."

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
    app.add_handler(CommandHandler('set_address', set_address))  # New command to set address
    app.add_handler(CommandHandler('check_balance', check_balance))  # Command to check balance
    app.add_handler(CommandHandler('make_transaction', make_transaction))  # Command to make a transaction

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    app.add_error_handler(error)

    # Poll the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
