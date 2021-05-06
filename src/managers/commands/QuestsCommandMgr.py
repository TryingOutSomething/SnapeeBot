from telegram.ext import ConversationHandler

from src.managers import IOassetsManager, LoggerManager, QuestManager, TimeManager
from src.templates import MessageTemplates
from . import ReusableComponents


def send_quest_image_start(update, context):
    ReusableComponents.log_command_accessed_timing(update)

    user_id = update.message.from_user.id
    username = update.message.from_user.username

    if not user_is_a_member(update):
        LoggerManager.general_logs(
            f"User {username} ({user_id}) is not a member!")

        update.message.reply_text(MessageTemplates.new_user_found_message)

        return ConversationHandler.END

    list_of_available_quests = get_list_of_available_quests_for_the_week()

    if len(list_of_available_quests) <= 0:
        update.message.reply_text(MessageTemplates.error_message)

        ReusableComponents.prompt_user_next_action(update)

        return ConversationHandler.END

    context.chat_data["quest_titles"] = list_of_available_quests

    update.message.reply_text(
        MessageTemplates.send_quest_image_message(list_of_available_quests))

    return 'QuestDescription'


def user_is_a_member(update):
    return ReusableComponents.check_membership_status(update)


def get_list_of_available_quests_for_the_week():
    date_today = TimeManager.get_current_date()

    return QuestManager.get_list_of_available_quest_titles_for_the_week(date_today)


# QuestDescription state
def display_quest_description(update, context):
    user_choice = update.message.text

    if is_invalid_user_choice(user_choice, context):
        update.message.reply_text(MessageTemplates.invalid_response_message)
        return 'QuestDescription'

    # Get quest description from database
    parsed_user_choice = int(user_choice) - 1
    selected_quest_title = context.chat_data["quest_titles"][parsed_user_choice][0]
    quest_description = QuestManager.get_list_of_available_quests_for_the_week(selected_quest_title)

    if not quest_description:
        username = update.message.from_user.username
        user_id = update.message.from_user.id

        LoggerManager.general_logs(f"Error occurred while {username} ({user_id}) is viewing quest description")

        return ConversationHandler.END

    update.message.reply_text(MessageTemplates.gen_quest_description_message(selected_quest_title, quest_description),
                              disable_web_page_preview=True)

    return 'ImageResponse'


def is_invalid_user_choice(user_choice, context):
    if not user_choice.isdigit():
        return True

    if int(user_choice) > len(context.chat_data["quest_titles"]) or int(user_choice) <= 0:
        return True

    return False


# ImageResponse state
def after_send_quest_image(update, context):
    photo_id = update.message.photo[0].file_id

    snapee_asst_id = IOassetsManager.get_snapee_asst_id()

    response_status = send_message_to_snapee_assistant(update, context, snapee_asst_id, photo_id)

    inform_user_about_sending_photo_result(update, response_status)

    return ConversationHandler.END


def send_message_to_snapee_assistant(update, context, snapee_asst_id, photo_id):
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    LoggerManager.general_logs(
        f"Sending user {username} ({user_id})'s photo to snapeeassistant now.")

    try:
        context.bot.send_photo(snapee_asst_id,
                               photo=photo_id,
                               caption=f"User: {username} ({user_id})")
        return True

    except Exception as e:
        LoggerManager.exception_logs(e)
        LoggerManager.exception_logs(
            f"Something went wrong while sending user {username} ({user_id})'s photo to SnapeeAssistant")


def inform_user_about_sending_photo_result(update, response_status):
    if response_status:
        update.message.reply_text(MessageTemplates.quest_image_sent_message)

    else:
        update.message.reply_text(MessageTemplates.error_message)

    ReusableComponents.prompt_user_next_action(update)
