from telegram.ext import ConversationHandler

from src.templates import KeyboardTemplates, MessageTemplates
from src.managers import LoggerManager, UserManager

TIMEOUT_DURATION_IN_MINUTES = MessageTemplates.TIMEOUT_DURATION_IN_MINUTES
EMPTY_LIST_LENGTH = 0


def check_membership_status(update):
    user_id = update.message.from_user.id

    LoggerManager.general_logs(
        f"Checking if user {update.message.from_user.username} ({user_id}) is a member")

    return UserManager.is_a_member(user_id)


def log_command_accessed_timing(update):
    username = update.message.from_user.username
    user_id = update.message.from_user.id
    command_entered_by_user = update.message.text

    LoggerManager.init_command_log(username,
                                   user_id,
                                   command_entered_by_user)


def prompt_user_next_action(update):
    message_to_send = MessageTemplates.ask_user_action_message
    update.message.reply_text(message_to_send,
                              disable_web_page_preview=True,
                              reply_markup=KeyboardTemplates.start_keyboard)


def cancel_current_action(update, context):
    user_id = str(update.message.from_user.id)

    try:
        context.user_data[user_id].clear()
        context.chat_data[user_id].clear()
        del update.message.photo[:]

    except:
        pass

    update.message.reply_text(
        MessageTemplates.cancel_action_message, reply_markup=KeyboardTemplates.start_keyboard)

    return ConversationHandler.END


def dispatch_voucher(update, voucher_path, caption_to_send):
    try:
        LoggerManager.general_logs(
            f"Sending voucher to {update.message.from_user.username} ({update.message.from_user.id}) now")

        update.message.reply_photo(photo=open(voucher_path, 'rb'),
                                   caption=caption_to_send)

    except Exception as e:
        update.message.reply_text(MessageTemplates.error_message)
        LoggerManager.exception_logs(e)


def timeout_handler(update, context):
    LoggerManager.general_logs(f"No action performed after {context.effective_message.text} " +
                               f"by user {context.effective_message.chat.username} " +
                               f"({context.effective_message.chat.id})"
                               )

    context.message.reply_text(MessageTemplates.action_auto_cancelled_message,
                               reply_markup=KeyboardTemplates.start_keyboard)

    return ConversationHandler.END


def error(update, context):
    # Log errors caused by Updates.
    LoggerManager.telegram_error_logs(update, context)
