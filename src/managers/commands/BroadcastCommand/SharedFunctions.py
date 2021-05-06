from src.managers import LoggerManager
from src.managers.commands import ReusableComponents
from src.templates import MessageTemplates

EMPTY_USER_LIST = ReusableComponents.EMPTY_LIST_LENGTH


def target_user_list_is_empty(target_users_list):
    if len(target_users_list) == EMPTY_USER_LIST or not target_users_list:
        LoggerManager.general_logs(
            "User list is empty! No users to broadcast message to.")
        return True

    else:
        LoggerManager.general_logs(
            "User list is not empty! Preparing to send to users.")


def send_broadcast_report_to_sender(update, error_occurred_while_sending_to_users_dict):
    message_to_send_to_sender = MessageTemplates.gen_broadcast_report(
        error_occurred_while_sending_to_users_dict)

    update.message.reply_text(message_to_send_to_sender)


def gen_broadcast_error_for_users_report(blocked_users_list, unreachable_users_list,
                                         unexpected_error_occurred_users_list):
    error_occurred_while_sending_to_users_dict = {
        'blocked_users': blocked_users_list,
        'unreachable_users': unreachable_users_list,
        'unexpected_errors': unexpected_error_occurred_users_list
    }

    return error_occurred_while_sending_to_users_dict


def inform_sender_no_of_users_to_broadcast(update, target_users_list):
    length_of_target_users = len(target_users_list)

    LoggerManager.general_logs(
        f"Broadcasting message to {length_of_target_users} user(s) now")

    message_to_inform_sender = MessageTemplates.gen_message_to_inform_sender(length_of_target_users)

    update.message.reply_text(message_to_inform_sender)
