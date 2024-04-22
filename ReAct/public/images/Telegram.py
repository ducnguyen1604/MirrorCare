from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, CallbackQueryHandler

import secrets
import string

import serial
import time
import pygame
import os


SerialObj = serial.Serial('COM7') # COMxx  format on Windows
                  # ttyUSBx format on Linux
SerialObj.baudrate = 9600  # set Baud rate to 9600
SerialObj.bytesize = 8   # Number of data bits = 8
SerialObj.parity  ='N'   # No parity
SerialObj.stopbits = 1   # Number of Stop bits = 1



def generate_password(length=6):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


TOKEN: Final = '6676651967:AAHntg9dJq1a80Ik5ugyDw64U_JdAxiEURo'
BOT_USERNAME: Final = '@MirrorCareBot'

# Variable to store the user's next message
next_message: dict = {}

def play_mp3(filename):
    # Initialize pygame
    pygame.mixer.init()

        # Load the mp3 file
    pygame.mixer.music.load(filename)

        # Play the mp3 file
    pygame.mixer.music.play()

        # Wait until music has finished playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Reminder 1", callback_data='reminder1'),
            InlineKeyboardButton("Reminder 2", callback_data='reminder2')
        ],
        [
            InlineKeyboardButton("Video Call", callback_data='videocall'),
            InlineKeyboardButton("Analysis", callback_data='analysis')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Click on Any Inline Buttons', reply_markup=reply_markup)

async def reminder1_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please type your reminder message.')

    # Save the chat ID and set a flag to capture the next message
    chat_id = update.message.chat.id
    next_message[chat_id] = True
async def reminder2_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please type your second reminder message.')

    # Save the chat ID and set a flag to capture the next message
    chat_id = update.message.chat.id
    next_message[chat_id] = 2  # Set the flag to 2 for line 2

async def videocall_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = generate_password()
    videocall_link = "https://monumental-snickerdoodle-9c90a1.netlify.app/"
    # Send the videocall link as a new message
    await update.message.reply_text(videocall_link)
    save_password_to_file(password)
    await update.message.reply_text(password)
    
    # trigger ringtone when videocall is clicked
    #when care giver press /videocall, the ringtone will be played
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Name of the mp3 file to play
    mp3_file = "ringtone.mp3"
    
    # Path to the mp3 file
    mp3_path = os.path.join(current_dir, mp3_file)

    # Play the mp3 file
    play_mp3(mp3_path)

    

async def health_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    health_command = 'https://thingspeak.com/channels/2516394'
    # Send the videocall link as a new message
    await update.message.reply_text(health_command)


async def analysis_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Generating Analysis...')
    await update.message.reply_text('https://docs.google.com/spreadsheets/d/1yOmEXi-7S6PydeWj9mPBoQfhNda4Q8BtkMxB_40WkLs/edit#gid=0')
    
async def sorter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Loading...')
    time.sleep(1)
    SerialObj.write(b'A')    #transmit 'A' (8bit) to micro/Arduino

async def dispense_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Dispensing...')
    time.sleep(1)
    SerialObj.write(b'B')    #transmit 'B' (8bit) to micro/Arduino

def save_message_to_file(chat_id: int, line_number: int, text: str):
    # Read existing content from the file
    file_name = 'reminder.txt'
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    # If the file has fewer lines than the specified index, append empty lines
    while len(lines) < line_number:
        lines.append('\n')

    # Update the specified line with the latest message
    lines[line_number - 1] = text + '\n'

    # Write the updated content back to the file
    with open(file_name, 'w') as file:
        file.writelines(lines)

def save_password_to_file(text: str):
    file_name = 'password.txt'

    with open(file_name, 'w') as file:
        file.writelines(text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
        else:
            return
        
    # Check if the chat ID is in the next_message dictionary
    chat_id = update.message.chat.id
    if chat_id in next_message and next_message[chat_id]:
        line_number = next_message[chat_id]
        await update.message.reply_text('Your Message "'+ text +'" have been saved successfully!')
        # Save the message to a file and replace the specified line
        save_message_to_file(chat_id, line_number, "Reminder: " + text)
        # Reset the flag
        next_message[chat_id] = False

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

async def button_click(update: Update, context: CallbackContext):
    query: CallbackQuery = update.callback_query

    if query.data == 'reminder1':
        await reminder1_command(update, context)
    elif query.data == 'reminder2':
        await reminder2_command(update, context)
    elif query.data == 'videocall':
        await videocall_command(update, context)
    elif query.data == 'analysis':
        await analysis_command(update, context)

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('reminder1', reminder1_command))
    app.add_handler(CommandHandler('reminder2', reminder2_command))
    app.add_handler(CommandHandler('videocall', videocall_command))
    app.add_handler(CommandHandler('analysis', analysis_command))
    app.add_handler(CommandHandler('sorting', sorter_command))
    app.add_handler(CommandHandler('dispensing', dispense_command))
    app.add_handler(CommandHandler('health', health_command))
    

    # Messages
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=2)
