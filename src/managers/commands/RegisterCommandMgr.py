import re

from telegram.ext import ConversationHandler

from src.managers import IOassetsManager, LoggerManager, RewardManager, TimeManager, UserManager
from src.templates import KeyboardTemplates, MessageTemplates
from . import ReusableComponents

REGEX_EMAIL_CHECKER = r"[^@]+@[^@]+\.[^@]+"
MALE_GENDER = 'Male'
FEMALE_GENDER = 'Female'
WANT_TO_SKIP_REFERRAL = 'Yes'
CHANGED_THEIR_MIND_ABOUT_SKIPPING_REFERRAL = 'Back'
EMPTY_SNAPCOIN_AMT = 0
SNAPCOIN_ASSET_TYPE = 'coin'
SNAPCOIN_ASSET_ID_IN_DB = 0


def new_user_reg_start(update, context):
    ReusableComponents.log_command_accessed_timing(update)

    result = ReusableComponents.check_membership_status(update)

    if len(result) != 0:
        LoggerManager.general_logs(
            f"User: {update.message.from_user.username} ({update.message.from_user.id}) is an existing member!")

        update.message.reply_text(MessageTemplates.existing_user_message)

        ReusableComponents.prompt_user_next_action(update)

        return ConversationHandler.END

    LoggerManager.general_logs(
        f"Starting registration for user: {update.message.from_user.username} ({update.message.from_user.id}) now.")

    message_to_send = MessageTemplates.ask_email_message + \
        MessageTemplates.new_user_turnback_message

    update.message.reply_text(message_to_send)

    return 'NewUserEmail'


def new_user_email(update, context):
    user_id = str(update.message.from_user.id)

    LoggerManager.general_logs(
        f"Checking if email is valid for User: {update.message.from_user.username} ({user_id}).")

    message_from_user = update.message.text

    if not re.match(REGEX_EMAIL_CHECKER, message_from_user):
        update.message.reply_text(MessageTemplates.invalid_email_message)

        return 'NewUserEmail'

    context.user_data.update({
        f'{user_id}': {'email': message_from_user}
    })

    update.message.reply_text(MessageTemplates.ask_gender_message,
                              reply_markup=KeyboardTemplates.gender_keyboard)

    return 'NewUserGender'


def new_user_gender(update, context):
    user_id = str(update.message.from_user.id)

    LoggerManager.general_logs(
        f"Checking gender info for User: {update.message.from_user.username} ({user_id}).")

    message_from_user = update.message.text

    if message_from_user != MALE_GENDER and message_from_user != FEMALE_GENDER:
        update.message.reply_text(MessageTemplates.invalid_response_message,
                                  reply_markup=KeyboardTemplates.gender_keyboard)

        return 'NewUserGender'

    context.user_data[user_id].update({
        'gender': message_from_user
    })

    update.message.reply_text(MessageTemplates.ask_referral_message)

    return 'NewUserReferralInput'


def new_user_referral_input(update, context):
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username

    LoggerManager.general_logs(
        f"Check if user: {username} ({user_id}) was referred by someone.")

    message_from_user = update.message.text

    referrer_telegram_id_and_snapcoin_amt = validate_referral_code(
        message_from_user)

    if not referrer_telegram_id_and_snapcoin_amt:
        update.message.reply_text(MessageTemplates.invalid_referrer_message)

        return 'NewUserReferralInput'

    award_referrer_referee(context,
                           user_id,
                           username,
                           referrer_telegram_id_and_snapcoin_amt)

    register_new_user(update, context)

    return ConversationHandler.END


def validate_referral_code(message_from_user):
    LoggerManager.general_logs(f"Verifying referral code {message_from_user}")

    referrer_telegram_id_and_snapcoin_amt = UserManager.is_valid_referral_code(
        message_from_user)

    if not referrer_telegram_id_and_snapcoin_amt:
        LoggerManager.exception_logs(
            f"Referral code: {message_from_user} is invalid! Prompting user to re-enter again.")

        return

    referrer_telegram_id = referrer_telegram_id_and_snapcoin_amt[0][0]
    referrer_snapcoin_amt = referrer_telegram_id_and_snapcoin_amt[0][1]

    LoggerManager.general_logs(
        f"Referral code found! Referrer's telegram id: {referrer_telegram_id} ({referrer_snapcoin_amt}) snapcoins.")

    return referrer_telegram_id_and_snapcoin_amt


def award_referrer_referee(context, referee_id, referee_username, referrer_telegram_id_and_snapcoin_amt):
    referrer_id = referrer_telegram_id_and_snapcoin_amt[0][0]
    referrer_snapcoin_amt = referrer_telegram_id_and_snapcoin_amt[0][1]

    updated_snapcoin_amt = referrer_snapcoin_amt + \
        RewardManager.REFERRAL_BONUS_AMT

    LoggerManager.general_logs(
        f"Referrer {referrer_id} updated! Previously: {referrer_snapcoin_amt}, updated: {updated_snapcoin_amt}")

    UserManager.update_referrer_snapcoin_amt(referrer_id, updated_snapcoin_amt)

    send_message_to_referrer(context, referrer_id, referee_username)
    send_message_to_referee(context,  referee_id, referee_username)

    UserManager.update_user_referal_history_table(referrer_id, referee_id)


def send_message_to_referrer(context, referrer_id, referee_username):
    LoggerManager.general_logs(
        f"Sending notification to user {referrer_id} about referring now!")

    referrer_message_to_send = MessageTemplates.gen_referrer_bonus_message(
        referee_username)

    context.bot.send_message(chat_id=referrer_id,
                             text=referrer_message_to_send)


def send_message_to_referee(context, referee_id, referee_username):
    LoggerManager.general_logs(
        f"Awarding referee {referee_username} ({referee_id}) 500 snapcoins now.")

    context.user_data[referee_id].update({
        'referral_bonus': RewardManager.REFERRAL_BONUS_AMT
    })

    context.bot.send_message(chat_id=referee_id,
                             text=MessageTemplates.congratulate_referee_message)


def new_user_referral_skip_warning(update, context):
    update.message.reply_text(MessageTemplates.ask_referral_confirm_skip_message,
                              reply_markup=KeyboardTemplates.referral_skip_keyboard)

    return 'NewUserReferralSkip'


def new_user_referral_skip(update, context):
    user_choice_of_skipping_referral = update.message.text

    if user_choice_of_skipping_referral == WANT_TO_SKIP_REFERRAL:
        LoggerManager.general_logs(
            f"User: {update.message.from_user.id} does not want to enter referral code")

        register_new_user(update, context)

        return ConversationHandler.END

    if user_choice_of_skipping_referral == CHANGED_THEIR_MIND_ABOUT_SKIPPING_REFERRAL:
        LoggerManager.general_logs(
            f"User: {update.message.from_user.id} wants to enter referral code!")

        update.message.reply_text(MessageTemplates.ask_referral_message)

        return 'NewUserReferralInput'

    update.message.reply_text(MessageTemplates.invalid_response_message,
                              reply_markup=KeyboardTemplates.referral_skip_keyboard)

    return 'NewUserReferralSkip'


def register_new_user(update, context):
    update.message.reply_text(MessageTemplates.new_user_create_message)

    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username
    referral_code = UserManager.gen_referral_code()

    new_user_entry = get_new_user_entry(context,
                                        referral_code,
                                        user_id,
                                        username)

    LoggerManager.general_logs(
        f"Registering user {username} ({user_id}) into the database now.")

    registration_result = UserManager.register_new_user(new_user_entry)

    send_registration_result(update, context, registration_result)

    ReusableComponents.prompt_user_next_action(update)

    # Empty user_data dictionary after registration
    context.user_data[user_id].clear()
    # End of registration command


def get_new_user_entry(context, referral_code, user_id, username):

    new_user_entry = {
        'user_id': user_id,
        'telegram_username': username,
        'email': context.user_data[user_id]['email'],
        'gender': context.user_data[user_id]['gender'],
        'referral_code': referral_code,
        'asset_type': SNAPCOIN_ASSET_TYPE,
        'asset_id': SNAPCOIN_ASSET_ID_IN_DB
    }

    if 'referral_bonus' in context.user_data[user_id]:
        new_user_entry['asset_value'] = context.user_data[user_id]['referral_bonus']
    else:
        new_user_entry['asset_value'] = EMPTY_SNAPCOIN_AMT

    return new_user_entry


def send_registration_result(update, context, registration_result):
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    if not registration_result:
        LoggerManager.exception_logs(
            f"Error occurred while registering user {username} ({user_id})!")

        message_to_send = MessageTemplates.error_message

        update.message.reply_text(message_to_send)

        return

    LoggerManager.general_logs(
        f"User {username} ({user_id}) registered successfully!")

    message_to_send = MessageTemplates.gen_welcome_new_user_message(
        username)

    update.message.reply_text(message_to_send)

    send_new_user_bonus_notification(context, user_id)


def send_new_user_bonus_notification(context, user_id):
    snapee_bonus_image = IOassetsManager.get_snapee_bonus_poster_path()

    context.bot.send_photo(user_id,
                           photo=open(snapee_bonus_image, 'rb'),
                           caption=MessageTemplates.new_reward_message)


def cancel_registration(update, context):
    user_id = str(update.message.from_user.id)

    update.message.reply_text(MessageTemplates.registration_cancel_message)

    if f'{user_id}' in context.user_data:
        context.user_data[user_id].clear()

    return ConversationHandler.END
