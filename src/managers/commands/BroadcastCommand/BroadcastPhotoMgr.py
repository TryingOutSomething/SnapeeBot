import telegram
from telegram.ext import ConversationHandler
from telegram.ext.dispatcher import run_async

from src.managers import GoogleSheetManager, IOassetsManager, LoggerManager
from src.managers.commands import ReusableComponents
from src.templates import KeyboardTemplates, MessageTemplates
from . import SharedFunctions

EMPTY_USER_LIST = ReusableComponents.EMPTY_LIST_LENGTH
EMPTY_USER_ID = ''
WANTS_TO_INCLUDE_CAPTION = 'Yes!'
DOES_NOT_WANT_TO_INCLUDE_CAPTION = 'No!'


def prompt_photo_caption(update, context):
    user_id = str(update.message.from_user.id)

    context.chat_data.update({
        f'{user_id}': {'photo_id': update.message.photo[0].file_id}
    })

    update.message.reply_text(MessageTemplates.prompt_sender_if_they_want_to_add_caption_to_image_message,
                              reply_markup=KeyboardTemplates.confirm_keyboard)

    return 'CaptionChoice'


def input_photo_caption(update, context):
    sender_choice = update.message.text

    if is_not_valid_choice(sender_choice):
        update.message.reply_text(MessageTemplates.invalid_response_message)

        return 'CaptionChoice'

    prompt_user_for_caption_to_send(update, context, sender_choice)

    return 'SendPhoto'


def is_not_valid_choice(sender_choice):
    return sender_choice != WANTS_TO_INCLUDE_CAPTION and sender_choice != DOES_NOT_WANT_TO_INCLUDE_CAPTION


def prompt_user_for_caption_to_send(update, context, sender_choice):
    user_id = str(update.message.from_user.id)

    if sender_choice == WANTS_TO_INCLUDE_CAPTION:
        context.chat_data[user_id].update({
            "include_caption_in_photo": True
        })

        update.message.reply_text(
            MessageTemplates.prompt_sender_to_enter_caption_text_message)

    else:
        context.chat_data[user_id].update({
            "include_caption_in_photo": False
        })

        update.message.reply_text(
            MessageTemplates.prompt_sender_to_enter_anything_message)


def broadcast_photo(update, context):
    user_id = str(update.message.from_user.id)

    target_users_list = GoogleSheetManager.get_user_telegram_id_from_google_sheet()

    if SharedFunctions.target_user_list_is_empty(target_users_list):
        update.message.reply_text(MessageTemplates.empty_user_list_message)

    else:
        image_information = {
            'photo_id': context.chat_data[user_id]['photo_id'],
            'include_caption_in_photo': context.chat_data[user_id]['include_caption_in_photo']
        }

        initialize_broadcast_photo_to_users(update, context, image_information, target_users_list)

    del update.message.photo[:]
    context.chat_data[user_id].clear()

    ReusableComponents.prompt_user_next_action(update)

    return ConversationHandler.END


@run_async
def initialize_broadcast_photo_to_users(update, context, image_information, target_users_list):
    SharedFunctions.inform_sender_no_of_users_to_broadcast(update, target_users_list)

    message_from_sender = update.message.text
    photo_id = image_information['photo_id']

    caption_to_send = image_includes_caption(image_information, message_from_sender)

    error_occurred_while_sending_to_users_dict = broadcast_photo_to_users(
        context, caption_to_send, photo_id, target_users_list)

    # if error_exists_while_sending_to_user(error_occurred_while_sending_to_users_dict):
    IOassetsManager.generate_error_list(error_occurred_while_sending_to_users_dict)

    SharedFunctions.send_broadcast_report_to_sender(update, error_occurred_while_sending_to_users_dict)


def broadcast_photo_to_users(context, caption_to_send, photo_id, target_users_list):
    blocked_users_list, unreachable_users_list, unexpected_error_occurred_users_list = [], [], []

    for user_id in target_users_list:
        try:
            if user_id == EMPTY_USER_ID:
                continue

            context.bot.send_photo(chat_id=user_id, photo=photo_id, caption=caption_to_send)

        except telegram.error.Unauthorized:
            blocked_users_list.append(user_id)

        except telegram.error.BadRequest:
            unreachable_users_list.append(user_id)

        except Exception as e:
            error_message = MessageTemplates.gen_error_message_while_sending_to_user(
                user_id)

            LoggerManager.exception_logs(e)
            LoggerManager.exception_logs(error_message)

            unexpected_error_occurred_users_list.append(user_id)

    error_occurred_while_sending_to_users_dict = SharedFunctions.gen_broadcast_error_for_users_report(
        blocked_users_list, unreachable_users_list, unexpected_error_occurred_users_list)

    return error_occurred_while_sending_to_users_dict


def image_includes_caption(image_information, message_from_sender):
    if image_information['include_caption_in_photo']:
        return message_from_sender


def error_exists_while_sending_to_user(error_occurred_while_sending_to_users_dict):
    length_of_blocked_users = len(
        error_occurred_while_sending_to_users_dict['blocked_users'])

    length_of_unreachable_users = len(
        error_occurred_while_sending_to_users_dict['unreachable_users'])

    length_of_unexpected_error_while_sending_to_users = len(
        error_occurred_while_sending_to_users_dict['unexpected_errors'])

    total_numbers_of_users_affected_by_error = length_of_blocked_users + \
                                               length_of_unreachable_users + \
                                               length_of_unexpected_error_while_sending_to_users

    return total_numbers_of_users_affected_by_error > EMPTY_USER_LIST
