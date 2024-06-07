import utils as utils
from telebot import TeleBot
import os
from telebot import types
from dotenv import load_dotenv
from constant import *
from callback import *
load_dotenv()
bot = TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

# User states
user_states = {}
user_data = {}

class User:
    def __init__(self):
        self.api_key = None
        self.secret_key = None
        
# Constants for states
STATE_NONE = "NONE"
STATE_INFO = "INFO"
STATE_USER = "USER"
STATE_SUBACCOUNT = "SUBACCOUNT"

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_message = (
        "Hello! I am Cub3 🤖💰. "
        "I can provide real-time data and order information. "
        "Use /info to get cryptocurrency info or /orders to view your orders."
    )
    bot.reply_to(message, welcome_message)

# Exit command
@bot.message_handler(commands=['exit'])
def handle_exit(message):
    user_id = message.from_user.id
    user_states[user_id] = STATE_NONE
    bot.reply_to(message, "You have exited the current state.")

# Info command
@bot.message_handler(commands=['info'])
def handle_info(message):
    user_id = message.from_user.id
    user_states[user_id] = STATE_INFO
    bot.reply_to(message, "Enter a cryptocurrency symbol (e.g., BTC, ETH), or type /exit to exit.")

# User command
@bot.message_handler(commands=['user'])
def handle_user(message):
    user_id = message.from_user.id
    user_states[user_id] = STATE_USER
    
    if user_id not in user_data:
        user_data[user_id] = User()
    
    user = user_data[user_id]
        
    if not user.api_key:
        bot.reply_to(message, "Please enter your API key:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(message, process_api_key)
    elif not user.secret_key:
        bot.reply_to(message, "Please enter your secret API key:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(message, process_secret_key)
    else:
        show_user_menu(message)
        
# User command
@bot.message_handler(commands=['subaccount'])
def handle_user(message):
    user_id = message.from_user.id
    user_states[user_id] = STATE_SUBACCOUNT
    
    if user_id not in user_data:
        user_data[user_id] = User()
    
    user = user_data[user_id]
        
    if not user.api_key:
        bot.reply_to(message, "Please enter your API key:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(message, process_api_key)
    elif not user.secret_key:
        bot.reply_to(message, "Please enter your secret API key:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(message, process_secret_key)
    else:
        show_subaccount_menu(message)
        
# Function to show the user menu
def show_user_menu(message):
    markup = types.InlineKeyboardMarkup()
    buttons = []
    
    for i, (text, callback_data) in enumerate(users_menu):
        button = types.InlineKeyboardButton(f"{text}", callback_data=f"user_{callback_data}")
        buttons.append(button)
        
        if (i + 1) % 2 == 0 or i == len(users_menu) - 1:  
            markup.row(*buttons)
            buttons = []

    bot.send_message(message.chat.id, "Press a button to get a number:", reply_markup=markup)
    
# Function to show the user menu
def show_subaccount_menu(message):
    markup = types.InlineKeyboardMarkup()
    buttons = []

    for i, (text, callback_data) in enumerate(subaccount_menu):
        button = types.InlineKeyboardButton(text, callback_data=f"subaccount_{callback_data}")
        buttons.append(button)
        
        if (i + 1) % 3 == 0 or i == len(subaccount_menu) - 1:  
            markup.row(*buttons)
            buttons = []

    bot.send_message(message.chat.id, "Choose option: ", reply_markup=markup)


# Handle user input based on state
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    state = user_states.get(user_id, STATE_NONE)

    if state == STATE_INFO:
        # Handle info state
        info = message.text
        response = utils.get_info_response(info)
        bot.reply_to(message, response)
        

# Handle inline button callback
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data in callback_handlers:
        callback_handlers[call.data](call, bot)
    
        
# Function to process API key
def process_api_key(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.api_key = message.text
    bot.reply_to(message, "API key saved successfully. Please enter your secret API key:")
    bot.register_next_step_handler(message, process_secret_key)

# Function to process secret API key
def process_secret_key(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.secret_key = message.text
    bot.reply_to(message, "Secret API key saved successfully.")
    show_user_menu(message)

# Start polling
command_info = [
    types.BotCommand("start", "Say hello to the bot"),
    types.BotCommand("info", "Get the info of cryptocurrency"),
    types.BotCommand("orders", "Get orders of your account"),
    types.BotCommand("user", "Get more about your account"),
    types.BotCommand("subaccount", "Get more about your subaccount"),
    types.BotCommand("exit", "Exit the current mode"),
]

if __name__ == '__main__':
    bot.set_my_commands(command_info)
    bot.infinity_polling()