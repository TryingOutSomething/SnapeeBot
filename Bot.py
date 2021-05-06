from telegram.ext import Updater

# Import sub directories into the main script
# Required in order to use them within the sub directories
from src.managers import IOassetsManager, TelegramHandlers, LoggerManager

_TOKEN = IOassetsManager.retrieve_token()
_PORT = IOassetsManager.get_server_port()
_WEBHOOK_URL = IOassetsManager.get_webhook_base_url()


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register handlers to dispatcher
    # On different commands - answer in Telegram
    TelegramHandlers.initialize_dispatchers(dispatcher)

    # Start the Bot
    current_environment_type = IOassetsManager.get_project_environment()

    if current_environment_type == 'development':
        updater.start_polling()

    elif current_environment_type == 'production':
        updater.start_webhook(listen="127.0.0.1", port=_PORT, url_path=_TOKEN)
        updater.bot.setWebhook(f"{_WEBHOOK_URL}{_TOKEN}")

    else:
        raise EnvironmentError('Invalid project environment. Please set a valid environment!')

    LoggerManager.general_logs("Bot started!")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    LoggerManager.general_logs("Bot shutting down now...")


if __name__ == '__main__':
    main()
