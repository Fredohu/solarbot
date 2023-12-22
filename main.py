from ast import And
import re
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton)
from lib_dev.lib_dev import SolEnd

### CBXTEvYqLZtBGSWwJcD7w7oCPGdR38TGmv8yAM3gQ1qL devnet1
### 9Rfo6MyLtpka9SzxqbQEWYEyaRvXRMJzt9Npo1mg9skX devnet2
### H2hFezqB6JNVUixUMttJogFr3KvhTDX4bLvT8Rq4eJwW mainnet1
### AddjSTX6VdJCgp2B36ioVnyHw57sSjqfewiBXYywwEoc mainnet2

API_ID = "20395432"
API_HASH = "e6a83af58a0d8319e5efe3416256f9de"
BOT_TOKEN = "6531081629:AAH-A0PKhf8zsyzKYmMVUoUMEROoI2KXU14"
App = Client("SolgramWalletBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
back = SolEnd()
Solana_Client = back.connect()

@App.on_message(filters.command('start'))
def start(client, message):
    back.users_profile[message.from_user.username] = {'reg_flag': False}
    text = f'Hey! Welcome to Solar NFTS bot. ' \
           f'SolarBot allows you to view and buy NFTs conveniently and quickly on Telegram.' \
           f'You need to connect your wallet to make the most use out of our application.' \
           f' Please, share your public key and we’ll connect it to your Telegram ID.'

    message.reply(text, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    'Registration',
                    callback_data='registration'
                ),
                InlineKeyboardButton(
                    'Skip',
                    callback_data='menu'
                )
            ]
        ]
    ))


@App.on_callback_query()
def start(client, query):
    if query.data == 'menu':
        App.send_message(query.from_user.username, 'Selection function', reply_markup=ReplyKeyboardMarkup(
            [
                ["/my_collection", "/my_balance", "/my_bids"],
                ["/show_collection", "/show_balance"]
            ],
            resize_keyboard=True  # Make the keyboard smaller
        ))
    elif query.data == 'registration':
        back.users_profile[query.from_user.username]['reg_flag'] = True
        back.users_profile[query.from_user.username]['func_data'] = 'registration'
        App.send_message(query.from_user.username, 'Please input public key')
    elif query.data == 'bind':
        # Access the relevant data using the 'query' object
        binder = query.data.get('binder')
        holder = query.data.get('holder')
        token_address = query.data.get('token_address')
        back.bind(binder, holder, token_address)

@App.on_message(filters.command('my_balance'))
def raw(client, message):
    bal = back.balance(back.addr_to_nick[message.from_user.username], back.connect())
    new_bal = bal["result"]["value"]
    new_bal = round(new_bal / 1000000000, 2)
    sol_bal = round((new_bal * back.price_in_usdt()), 2)
    print(f'{new_bal} SOL / {sol_bal} USDT')
    message.reply(f'{new_bal} SOL = {sol_bal} USD')


@App.on_message(filters.command('my_collection'))
def drop(client, message):
    wallet = back.addr_to_nick[message.from_user.username]
    print(wallet)
    for address in back.get_tokens(wallet):
        try:
            metadata = back.get_nft_metadata(address)
            uri = back.get_uri_token(metadata)
            App.send_photo(message.from_user.username, back.request_img(uri), caption=back.request_data(uri))
        except:
            print(address)


@App.on_message(filters.command('show_balance'))
def raw(client, message):
    back.users_profile[message.from_user.username]['reg_flag'] = True
    back.users_profile[message.from_user.username]['func_data'] = {
        'func_name':"show_balance",
        'chat_id': str(message.chat.id)
        }
    print(message.chat.id)
    message.reply("Please input public key:")

@App.on_message(filters.command('show_collection'))
def drop(client, message):
    back.users_profile[message.from_user.username]['reg_flag'] = True
    back.users_profile[message.from_user.username]['func_data'] = {
        'func_name':"show_collection",
        'chat_id': str(message.chat.id)
        }
    print(message.chat.id)
    message.reply("Please input your public key:")
   
@App.on_message(filters.command('help'))
def helper(client, message):
    message.reply(
        "This bot helps you to surf and trade Solana NFTs:\n"\
        "/reg + publicKey - registrate your public address, so you dont need to paste it later\n"\
        "/my_collection - shows your NFTs with names and descriptions\n"\
        "/my_balance - shows your SOL balance\n"\
        "/show_collection + user_publicKey - shows user NFTs with names and descriptions\n"\
        "/show_balance + user_publicKey - shows user SOL balance"
    )
# @App.on_message(filters.command('buy'))

@App.on_callback_query()
def bind(client, query):
    data = query["data"]
    back.bind(query.from_user.username,data[1]["holder"],data[1]["nft_address"])
    App.send_message("Offer your price (bid). It will be shared with the owner. "\
        "If approved, you will be charged and become the owner.")

@App.on_message()
def other(client, message):
    user = message.from_user.username
    # chat_id = back.users_profile[user]['func_data']['chat_id']
    chat_id = user
    if back.users_profile[user]['reg_flag'] and back.users_profile[user]['func_data'] == "registration":
        back.users_profile[user]['reg_flag'] = False
        back.addr_to_nick[user] = message.text
        print(back.addr_to_nick)
        App.send_message(chat_id,"Registration succesful. Now you can use bot functions."\
                      "Use /help for more information")

    elif back.users_profile[user]['reg_flag'] and back.users_profile[user]['func_data']['func_name'] == "show_collection" :
        back.users_profile[user]['reg_flag'] = False
        wallet = message.text
        print(wallet)
        holder = "@Okari1n"
        for address in back.get_tokens(wallet):
            keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        'Buy',
                        callback_data='buy'
                    ),
                    InlineKeyboardButton(
                        'Bid',
                        callback_data = 'bid',
                        #     'function_name': 'bind',
                        #     'binder' : 'message.from_user.user',
                        #     'token_address': address,
                        #     'holder': holder}
                    )
                ]
            ]
            )
            try:
                metadata = back.get_nft_metadata(address)
                uri = back.get_uri_token(metadata)
                print(user)
                App.send_photo(user,
                    back.request_img(uri),
                    caption=back.request_data(uri),
                    reply_markup = keyboard)
            except:
                print(address)

    elif back.users_profile[user]['reg_flag'] and back.users_profile[user]['func_data']['func_name'] == "show_balance" :
        bal = back.balance(message.text, back.connect())
        new_bal = bal["result"]["value"]
        new_bal = round(new_bal / 1000000000, 2)
        sol_bal = round((new_bal * back.price_in_usdt()), 2)
        print(f'{new_bal} SOL / {sol_bal} USDT')
        message.reply(f'{new_bal} SOL = {sol_bal} USD') #

App.run()
