from telegram.ext import ConversationHandler

from src.managers import IOassetsManager
from src.managers.commands import ReusableComponents
from src.templates import KeyboardTemplates, MessageTemplates


def mass_broadcast_start(update, context):
    admin_list = IOassetsManager.get_list_of_admins()

    user_id = str(update.message.from_user.id)

    if not admin_list or user_id not in admin_list:
        update.message.reply_text("You do not have access to this command!")

        ReusableComponents.prompt_user_next_action(update)

        return ConversationHandler.END

    update.message.reply_text(MessageTemplates.prompt_send_image_or_text_message,
                              reply_markup=KeyboardTemplates.message_type_keyboard)

    return 'SendOption'


def broadcast_choice(update, context):
    sender_choice = update.message.text

    if sender_choice == 'Text':
        update.message.reply_text(
            MessageTemplates.prompt_sender_to_enter_text_message)

        return 'SendMessage'

    if sender_choice == 'Photo':
        update.message.reply_text(
            MessageTemplates.prompt_sender_to_upload_image_message)

        return 'AskCaption'

    update.message.reply_text(MessageTemplates.invalid_response_message,
                              reply_markup=KeyboardTemplates.message_type_keyboard)

    return 'SendOption'
