import pandas as pd
from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, Application,
    MessageHandler, filters, CallbackQueryHandler
)
from decimal import Decimal

import requests
import hmac
import hashlib
import time
import base64
import struct
import os
from dotenv import load_dotenv
load_dotenv()

MODES = ["info", "orders", "user"]

def generate_api_headers(api_key, api_secret_hex):
    """
    Generates the x-api-signature for Cube Exchange API requests.

    Args:
        api_key: Your Cube Exchange API key.
        api_secret_hex: Your Cube Exchange API secret key (in hex format).

    Returns:
        The base64 encoded API signature string.
    """
    timestamp = int(time.time())
 
    payload = b"cube.xyz" + struct.pack("<Q", timestamp)  # Little-endian 8-byte timestamp
    api_secret = bytes.fromhex(api_secret_hex)
    signature = hmac.new(api_secret, payload, hashlib.sha256).digest()
    signature_b64 = base64.b64encode(signature).decode("utf-8")

    header = {
        "x-api-key": api_key,
        "x-api-signature": signature_b64,
        "x-api-timestamp": str(timestamp),
    }
    
    return header

def get_info(crypto):
    try:
        response = requests.get(f'https://api.cube.exchange/md/v0/parsed/tickers')
        response.raise_for_status()
        result = response.json()
        df = pd.DataFrame(result.get('result'))
        data = df[df['base_currency'].str.lower() == crypto.lower()]
        return data
    except requests.exceptions.RequestException as err:
        print(f"Error fetching info: {err}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "Hello! I am Cub3 🤖💰. "
        "I can provide real-time data and order information. "
        "Use /info to get cryptocurrency info or /orders to view your orders."
    )
    await update.message.reply_text(welcome_message)
    
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["mode"] = "info"
    await update.message.reply_text("Enter a cryptocurrency symbol (e.g., BTC, ETH), or type /exit to exit.")

async def get_info_and_display(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get("mode") == "info":
        crypto = update.message.text
        data = get_info(crypto)
        if not data.empty:
            price = data["last_price"].iloc[0]
            base_currency = data["base_currency"].iloc[0]
            high = data["high"].iloc[0]
            low = data["low"].iloc[0]
            volume = data["quote_volume"].iloc[0]

            price_decimals = max(0, -Decimal(str(price)).as_tuple().exponent)
            high_decimals = max(0, -Decimal(str(high)).as_tuple().exponent)
            low_decimals = max(0, -Decimal(str(low)).as_tuple().exponent)
            volume_decimals = max(0, -Decimal(str(volume)).as_tuple().exponent)

            await update.message.reply_text(
                f'The current price of {base_currency} is {price:.{price_decimals}f}$\n'
                f"📈 24h:\n"
                f"--High: {high:.{high_decimals}f}$\n"
                f"--Low: {low:.{low_decimals}f}$\n"
                f"--Volume: {volume:.{volume_decimals}f} 💰"
            )

        else:
            await update.message.reply_text(f'Could not find data for {crypto}. Please check the symbol.')
    else:
        await update.message.reply_text("You are not in /info mode. Type /info to start.")

async def exit_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if "mode" in context.user_data:
        del context.user_data["mode"]
        await update.message.reply_text("Mode is exit.")
    else:
        await update.message.reply_text("You were not in any mode.")

async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    current_mode = context.user_data.get("mode")
    text = update.message.text

    if current_mode in MODES and text.startswith("/"):
        if text == f"/{current_mode}":
            if current_mode == "info":
                await get_info_and_display(update, context)
            elif current_mode == "orders":
                await orders(update, context)
        elif text == "/exit":
            await exit_mode(update, context)
        else:
            await update.message.reply_text(f"Invalid command in /{current_mode} mode. Please use /exit to exit.")
    else:
        if text.startswith("/"):
            await update.message.reply_text("Please choose a mode: /" + " or /".join(MODES))
        else:
            if current_mode == "info":
                await get_info_and_display(update, context)
            elif current_mode == "orders":
                await update.message.reply_text("You are in /orders mode. Type /info to switch to info mode.")
            else:
                await update.message.reply_text(f"Invalid command.")

async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["mode"] = "orders"
    url = "https://api.cube.exchange/os/v0/orders" 
    headers = generate_api_headers(os.getenv('API_KEY'), os.getenv('API_KEY'))
    response = requests.get(f'{url}', headers=headers, params={"subaccountId": 110125})
    response.raise_for_status()
    data = response.json()
    
    if data:
        await update.message.reply_text(f'{data}')
    else:
        await update.message.reply_text(f'Hah')

async def user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["mode"] = "user"
    keyboard = [
        [
            InlineKeyboardButton("👤 Account", callback_data='view_account'),
            InlineKeyboardButton("👥 Subaccounts", callback_data='view_subaccounts'),
            InlineKeyboardButton("🔑 API Keys", callback_data='view_api_keys'),
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data='settings'),
            InlineKeyboardButton("❓ Help", callback_data='help'),
            InlineKeyboardButton("🚪 Exit", callback_data='exit'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = await update.message.reply_text('Choose an action:', reply_markup=reply_markup)
    
    user_data = context.user_data
    user_data.setdefault('user_messages', {})
    user_data['user_messages'][update.effective_user.id] = message.message_id

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'view_account':
        # Handle viewing account information
        account_info = "Your account information..."  # Replace with actual account info
        await context.bot.send_message(chat_id=update.effective_chat.id, text=account_info, reply_to_message_id=context.user_data['user_messages'][update.effective_user.id])
    elif query.data == 'view_subaccounts':
        # Handle viewing subaccount information
        subaccount_info = "Your subaccount information..."  # Replace with actual subaccount info
        await query.reply_text(text=subaccount_info, reply_markup=query.message.reply_markup) 
    elif query.data == 'view_api_keys':
        # Handle viewing API keys
        api_key_info = "Your API key information..."  # Replace with actual API key info
        await query.reply_text(text=api_key_info, reply_markup=query.message.reply_markup) 
    elif query.data == 'settings':
        # Handle settings
        settings_info = "Your settings..."  # Replace with actual settings info
        await query.reply_text(text=settings_info, reply_markup=query.message.reply_markup)
    elif query.data == 'help':
        # Handle help
        help_info = "Instructions for using the bot..."  # Replace with actual help info
        await query.reply_text(text=help_info, reply_markup=query.message.reply_markup)
    elif query.data == 'exit':
        # Handle exiting USER_MODE
        if context.user_data.get("mode") == "user":
            del context.user_data["mode"]
            await query.reply_text(text="Exited USER_MODE.")
            
command_info = [
    BotCommand("start", "Say hello to the bot"),
    BotCommand("info", "Get the info of cryptocurrency "),
    BotCommand("orders", "Get orders of your account"),
    BotCommand("user", "Get more about your account"),
    BotCommand("exit", "Exit the current mode"),
]

async def post_init(application: Application) -> None:
    bot = application.bot
    await bot.set_my_commands(commands=command_info)

app = ApplicationBuilder().token(os.getenv('TELEGRAM_BOT_TOKEN')).post_init(post_init).build()


app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("info", info))
app.add_handler(CommandHandler("orders", orders))
app.add_handler(CommandHandler("exit", exit_mode))
app.add_handler(CommandHandler("user", user))
# app.add_handler(CallbackQueryHandler(button_callback))

app.run_polling()