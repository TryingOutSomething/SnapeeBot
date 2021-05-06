import telegram
from telegram.ext import ConversationHandler
from telegram.ext.dispatcher import run_async

from src.managers import GoogleSheetManager, IOassetsManager, LoggerManager
from src.managers.commands import ReusableComponents
from src.templates import MessageTemplates
from . import SharedFunctions

EMPTY_USER_LIST = ReusableComponents.EMPTY_LIST_LENGTH
EMPTY_USER_ID = ''


def broadcast_message(update, context):
    target_users_list = GoogleSheetManager.get_user_telegram_id_from_google_sheet()

    if SharedFunctions.target_user_list_is_empty(target_users_list):
        update.message.reply_text(MessageTemplates.empty_user_list_message)

    else:
        initialize_broadcast_message_to_users(update, context, target_users_list)

    ReusableComponents.prompt_user_next_action(update)

    return ConversationHandler.END


@run_async
def initialize_broadcast_message_to_users(update, context, target_users_list):
    SharedFunctions.inform_sender_no_of_users_to_broadcast(update, target_users_list)

    broadcast_message = update.message.text

    error_occurred_while_sending_to_users_dict = broadcast_message_to_users(context,
                                                                            broadcast_message,
                                                                            target_users_list)

    IOassetsManager.generate_error_list(error_occurred_while_sending_to_users_dict)

    SharedFunctions.send_broadcast_report_to_sender(update, error_occurred_while_sending_to_users_dict)


def broadcast_message_to_users(context, broadcast_message, target_users_list):
    blocked_users_list, unreachable_users_list, unexpected_error_occurred_users_list = [], [], []

    for user_id in target_users_list:
        try:
            if user_id == EMPTY_USER_ID:
                continue

            context.bot.send_message(chat_id=user_id, text=broadcast_message)

        except telegram.error.Unauthorized:
            blocked_users_list.append(user_id)

        except telegram.error.BadRequest:
            unreachable_users_list.append(user_id)

        except Exception as e:
            error_message = MessageTemplates.gen_error_message_while_sending_to_user(user_id)

            LoggerManager.exception_logs(e)
            LoggerManager.exception_logs(error_message)

            unexpected_error_occurred_users_list.append(user_id)

    error_occurred_while_sending_to_users_dict = SharedFunctions.gen_broadcast_error_for_users_report(
        blocked_users_list, unreachable_users_list, unexpected_error_occurred_users_list)

    return error_occurred_while_sending_to_users_dict
