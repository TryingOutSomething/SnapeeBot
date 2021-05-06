from src.managers import LoggerManager
from src.templates import KeyboardTemplates, MessageTemplates
from . import ReusableComponents

EMPTY_LIST = ReusableComponents.EMPTY_LIST_LENGTH


def start(update, context):
    # /start command handler method
    ReusableComponents.log_command_accessed_timing(update)

    update.message.reply_text(MessageTemplates.start_message)

    result = ReusableComponents.check_membership_status(update)

    generate_start_command_message(update, result)


def generate_start_command_message(update, result):
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    if len(result) == EMPTY_LIST:
        LoggerManager.general_logs(
            f"User: {username} ({user_id}) is not a member. Redirecting to registration now.")

        return update.message.reply_text(MessageTemplates.new_user_found_message)

    LoggerManager.general_logs(f"User: {username} ({user_id}) is a member.")

    message_to_send = MessageTemplates.welcome_back_message(update.message.from_user.username)

    update.message.reply_text(message_to_send,
                              disable_web_page_preview=True,
                              reply_markup=KeyboardTemplates.start_keyboard)
