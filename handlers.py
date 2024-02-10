from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler
from constants import TOKEN
from utils import check_space_for_token
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

logger = logging.getLogger(__name__)

TRENDING_POSITIONS_LIMIT = 15
STATIC_WALLET_ADDRESS = '123'  # Static wallet address provided by the user

async def start_command(update, context):
    chain_options = [
        InlineKeyboardButton("Solana", callback_data="select_chain_solana"),
        InlineKeyboardButton("Ethereum", callback_data="select_chain_ethereum"),
    ]
    reply_markup = InlineKeyboardMarkup([chain_options])
    await update.message.reply_text("Please select a chain:", reply_markup=reply_markup)

async def handle_chain_selection(update, context):
    query = update.callback_query
    selected_chain = query.data.split("_")[-1]
    await query.message.reply_text(f"You selected {selected_chain.capitalize()} chain. Please send me the token address.")
    context.user_data['selected_chain'] = selected_chain
    context.user_data['state'] = 'expecting_token_address'

async def handle_user_response(update, context):
    user_response = update.message.text
    if context.user_data.get('state') == 'expecting_token_address':
        context.user_data['token_address'] = user_response
        await update.message.reply_text("Please provide the Telegram group or portal for the token:")
        context.user_data['state'] = 'expecting_group_portal'
    elif context.user_data.get('state') == 'expecting_group_portal':
        context.user_data['group_portal'] = user_response
        plan_options = [
            InlineKeyboardButton("Basic: 1.5 SOL - 3 Hours", callback_data="select_plan_basic"),
            InlineKeyboardButton("Premium: 2.5 SOL - 6 Hours", callback_data="select_plan_premium"),
            InlineKeyboardButton("Pro: 4 SOL - 12 Hours", callback_data="select_plan_pro"),
            InlineKeyboardButton("VIP: 7.5 SOL - 24 Hours", callback_data="select_plan_vip"),
        ]
        reply_markup = InlineKeyboardMarkup([plan_options])
        await update.message.reply_text("Please select a plan:", reply_markup=reply_markup)
        context.user_data['state'] = 'expecting_plan_selection'
    elif context.user_data.get('state') in ['expecting_plan_selection', 'plan_selected']:
        pass
    else:
        pass

async def handle_plan_selection(update, context):
    query = update.callback_query
    selected_plan = query.data.split("_")[-1]
    if check_space_for_token():
        await query.message.reply_text(f"Please send {selected_plan.capitalize()} SOL to the following wallet address:\n{STATIC_WALLET_ADDRESS}")
        context.user_data['state'] = 'plan_selected'
    else:
        await query.message.reply_text("Sorry, there are no available trending positions at the moment. Please try again later.")

def setup_handlers(application):
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CallbackQueryHandler(handle_chain_selection))
    application.add_handler(MessageHandler(None, handle_user_response))
    application.add_handler(CallbackQueryHandler(handle_plan_selection))
