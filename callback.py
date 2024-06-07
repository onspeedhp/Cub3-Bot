

def view_subaccount_check(call, bot):
    account_info = "Your account information... 1"  # Replace with actual account info
    bot.send_message(call.message.chat.id, account_info)

def view_subaccount_positions(call, bot):
    account_info = "Your account information.. 2"  # Replace with actual account info
    bot.send_message(call.message.chat.id, account_info)

def view_subaccount_transfers(call, bot):
    account_info = "Your account information... 3"  # Replace with actual account info
    bot.send_message(call.message.chat.id, account_info)
    
def view_subaccount_deposits(call, bot):
    account_info = "Your account information... 4"  # Replace with actual account info
    bot.send_message(call.message.chat.id, account_info)
    
def view_subaccount_withdrawals(call, bot):
    account_info = "Your account information... 5"  # Replace with actual account info
    bot.send_message(call.message.chat.id, account_info)
    
def view_subaccount_orders(call, bot):
    account_info = "Your account information... 6"  # Replace with actual account info
    bot.send_message(call.message.chat.id, account_info)

def view_user_check(call, bot):
    account_info = "Your account information... 7"  # Replace with actual account info
    bot.send_message(call.message.chat.id, account_info)
    
def view_user_subaccounts(call, bot):
    account_info = "Your account information... 8"  # Replace with actual account info
    bot.send_message(call.message.chat.id, account_info)

def view_user_address(call, bot):
    account_info = "Your account information... 9"  # Replace with actual account info
    bot.send_message(call.message.chat.id, account_info)
    
def view_user_settings(call, bot):
    account_info = "Your account information... 10"  # Replace with actual account info
    bot.send_message(call.message.chat.id, account_info)
    
callback_handlers = {
    'user_check': view_user_check,
    'user_subaccounts': view_user_subaccounts,
    'user_address': view_user_address,
    'user_settings': view_user_settings,
    'subaccount_check': view_subaccount_check,
    'subaccount_positions': view_subaccount_positions,
    'subaccount_transfers': view_subaccount_transfers,
    'subaccount_deposits': view_subaccount_deposits,
    'subaccount_withdrawals': view_subaccount_withdrawals,
    'subaccount_orders': view_subaccount_orders,
}
