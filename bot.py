import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, Application, filters
from telegram import Update, BotCommand
from models import Catlog, User, Group
from dbhelper import Session
from commands import suggested_commands

# Load environment variables
load_dotenv()
TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_IDS = os.environ.get('ADMIN_IDS').split(',')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Admin check decorator
def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if str(update.message.from_user.id) in ADMIN_IDS:
            return await func(update, context)
        else:
            await update.message.reply_text("Sorry, but you aren't authorized to use this command.")
            return None
    return wrapper

async def set_commands(bot):
    COMMANDS = [BotCommand(key, val) for key, val in dict(suggested_commands).items()]
    await bot.set_my_commands(COMMANDS)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro_text = (
        f"Hello {update.effective_user.first_name}! 👋\n\n"
        "Welcome to the Group Message Collector Bot! 🤖\n\n"
        "This bot helps you keep track of all the messages and users in your group chats.\n\n"
        "To get started, just keep the bot in your group and it will automatically log messages and user information.\n\n"
        "You can use the following commands to interact with the bot:\n"
        "- Use `/help` to get a list of all available commands and learn how to use them.\n\n"
        "Enjoy using the bot! 😊"
    )
    await update.message.reply_text(intro_text)
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Available Commands:
    /start - Start interacting with the bot
    /all_users - (Admin) Get a list of all users
    /msgs <user_id> - (Admin) Get the last 4 messages of the specified user
    """
    await update.message.reply_text(help_text)

async def create_text_catlog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user = msg.from_user
    chat = msg.chat
    reply_to = msg.reply_to_message.id if msg.reply_to_message else None

    with Session() as session:
        try:
            user_record = session.query(User).filter(User.tg_user_id == user.id).first()
            if not user_record:
                user_record = User(tg_user_id=user.id, first_name=user.first_name, last_name=user.last_name, is_bot=user.is_bot, username=user.username)
                session.add(user_record)
                session.commit()

            group_record = session.query(Group).filter(Group.tg_group_id == chat.id).first()
            if not group_record:
                group_record = Group(tg_group_id=chat.id, title=chat.title, chat_type=chat.type, username=chat.username)
                session.add(group_record)
                session.commit()

            record = Catlog(msg_id=msg.message_id, text=msg.text, timestamp=msg.date, group_id=group_record.id, user_id=user_record.id, reply_to=reply_to)
            session.add(record)
            session.commit()
            logger.info(f"Added catalog entry: {record}")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to create text catalog: {e}")

async def create_chat_catlog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.new_chat_members:
        user = update.message.new_chat_members[0]
        with Session() as session:
            try:
                user_record = session.query(User).filter(User.tg_user_id == user.id).first()
                if not user_record:
                    user_record = User(tg_user_id=user.id, first_name=user.first_name, last_name=user.last_name, is_bot=user.is_bot, username=user.username, join_date=update.message.date)
                    session.add(user_record)
                    session.commit()
                    logger.info(f"Added new chat member: {user_record}")
            except Exception as e:
                session.rollback()
                logger.error(f"Failed to create chat catalog: {e}")

@admin_only
async def all_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = ""
    with Session() as session:
        users = session.query(User).all()
        for user in users:
            msg += f"<name: {user.first_name} {user.last_name or ''} (id: {user.tg_user_id})>\n"
    if msg:
        await update.message.reply_text(text=msg)
    else:
        await update.message.reply_text("No users found.")

@admin_only
async def msgs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        try:
            user_id = int(context.args[0])
            msg = ""
            with Session() as session:
                user = session.query(User).filter(User.tg_user_id == user_id).first()
                if user:
                    for i, catlog in enumerate(user.catlogs[-4:], start=1):
                        msg += f"msg {i}: {catlog.text}\n"
            if msg:
                await update.message.reply_text(msg)
            else:
                await update.message.reply_text("No messages found for the specified user.")
        except ValueError:
            await update.message.reply_text("Please provide a valid User ID.")
    else:
        await update.message.reply_text("Usage: /msgs <user_id>")

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(update)

def main():
    app = Application.builder().token(TOKEN).build()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_commands(app.bot))

    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, create_text_catlog))
    app.add_handler(MessageHandler(filters.CHAT & filters.ChatType.GROUPS, create_chat_catlog))

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('all_users', all_users, filters.ChatType.PRIVATE))
    app.add_handler(CommandHandler('msgs', msgs, filters.ChatType.PRIVATE))

    
    logger.info("Bot started")
    app.run_polling()

if __name__ == '__main__':
    main()
