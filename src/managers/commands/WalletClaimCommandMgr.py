from telegram.ext import ConversationHandler

from src.managers import ExpiryManager, LoggerManager, ShopManager, TimeManager, UserManager
from src.templates import MessageTemplates
from . import ReusableComponents

EMPTY_LIST_LENGTH = ReusableComponents.EMPTY_LIST_LENGTH
MINIMUM_VOUCHER_INDEX_RANGE = 0


def wallet_profile_start(update, context):
    ReusableComponents.log_command_accessed_timing(update)

    update.message.reply_text(MessageTemplates.loading_message)

    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username

    dict_of_vouchers_owned_by_user = get_all_vouchers_owned_by_user(user_id,
                                                                    username)

    user_snapcoin_amount = UserManager.get_user_snap_coin_amount(
        user_id)

    if len(user_snapcoin_amount) == EMPTY_LIST_LENGTH:
        LoggerManager.general_logs(
            f"User: {username} ({user_id}) is not an existing member! Redirecting to sign up now!")

        update.message.reply_text(MessageTemplates.new_user_found_message)

        return ConversationHandler.END

    send_user_profile_message(update, dict_of_vouchers_owned_by_user, user_snapcoin_amount)

    if (not dict_of_vouchers_owned_by_user or
            len(dict_of_vouchers_owned_by_user['non_expired_vouchers']) == EMPTY_LIST_LENGTH):

        ReusableComponents.prompt_user_next_action(update)

        return ConversationHandler.END

    context.user_data.update({
        f'{user_id}': {'claimable_vouchers': dict_of_vouchers_owned_by_user['non_expired_vouchers']}
    })

    return 'ViewVoucher'


def get_all_vouchers_owned_by_user(user_id, username):
    list_of_vouchers_owned_by_user = UserManager.get_all_vouchers_owned_by_user(
        user_id)

    if len(list_of_vouchers_owned_by_user) == EMPTY_LIST_LENGTH:
        LoggerManager.general_logs(
            f"User {username} ({user_id}) does not have any vouchers in their wallet.")

        return

    filtered_list_of_vouchers = ExpiryManager.filter_expired_and_non_expired_vouchers(
        list_of_vouchers_owned_by_user, user_id)

    return filtered_list_of_vouchers


def send_user_profile_message(update, dict_of_vouchers_owned_by_user, user_snapcoin_amount):
    if not dict_of_vouchers_owned_by_user:
        dict_of_vouchers_owned_by_user = {}

    expired_voucher_message, message_to_send = MessageTemplates.gen_user_profile_message(dict_of_vouchers_owned_by_user,
                                                                                         user_snapcoin_amount)

    if expired_voucher_message:
        update.message.reply_text(expired_voucher_message)

    update.message.reply_text(message_to_send)


def view_selected_voucher(update, context):
    user_choice = update.message.text
    user_id = str(update.message.from_user.id)

    user_selected_voucher = is_valid_choice(user_choice, context, user_id)

    if not user_selected_voucher:
        update.message.reply_text(MessageTemplates.invalid_input_message)

        return 'ViewVoucher'

    context.user_data[user_id].update({
        'user_selected_voucher': user_selected_voucher
    })

    send_confirmation_voucher_to_user(update, user_selected_voucher)

    return 'ClaimVoucher'


def is_valid_choice(user_choice_str_format, context, user_id):
    try:
        user_choice = int(user_choice_str_format) - 1
        user_selected_voucher = ""

        if user_choice >= MINIMUM_VOUCHER_INDEX_RANGE:
            user_selected_voucher = context.user_data[user_id]['claimable_vouchers'][user_choice]

            return user_selected_voucher

    except Exception as e:
        LoggerManager.exception_logs(e)


def send_confirmation_voucher_to_user(update, user_selected_voucher):
    chosen_voucher_image_path = user_selected_voucher[3]
    voucher_info = get_voucher_info(user_selected_voucher)

    caption_to_send = MessageTemplates.gen_voucher_info(voucher_info, True)

    ReusableComponents.dispatch_voucher(update,
                                        chosen_voucher_image_path,
                                        caption_to_send)

    update.message.reply_text(MessageTemplates.confirm_claim_message)


def get_voucher_info(user_selected_voucher):
    chosen_voucher_title = user_selected_voucher[2]
    chosen_voucher_business_hours = "-" if not user_selected_voucher[4] else user_selected_voucher[4]
    chosen_voucher_location = "-" if not user_selected_voucher[5] else user_selected_voucher[5]
    chosen_voucher_website = "-" if not user_selected_voucher[6] else user_selected_voucher[6]
    chosen_voucher_phone_no = "-" if not user_selected_voucher[7] else user_selected_voucher[7]
    chosen_voucher_expiry_date = user_selected_voucher[8]
    chosen_voucher_expiry_date_in_d_m_y = TimeManager.convert_date_to_d_m_y_format(
        chosen_voucher_expiry_date)

    voucher_info = {
        'voucher_name': chosen_voucher_title,
        'expiry_date': chosen_voucher_expiry_date_in_d_m_y,
        'business_hours': chosen_voucher_business_hours,
        'location': chosen_voucher_location,
        'website': chosen_voucher_website,
        'phone': chosen_voucher_phone_no,
    }

    return voucher_info


def claim_voucher(update, context):
    user_response = update.message.text

    if is_invalid_shop_code(user_response):
        update.message.reply_text(MessageTemplates.invalid_shop_code_message)

        return 'ClaimVoucher'

    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username

    LoggerManager.general_logs(
        f"User {username} ({user_id}) wants to claim their voucher!")

    update.message.reply_text(MessageTemplates.loading_message)

    response_result = delete_voucher_from_user_wallet(context,
                                                      username,
                                                      user_id)

    if not response_result:
        update.message.reply_text(MessageTemplates.error_message)

    else:
        user_selected_voucher_title = context.user_data[user_id]['user_selected_voucher'][2]
        inform_user_claim_successful(update, user_selected_voucher_title)

    ReusableComponents.prompt_user_next_action(update)

    context.user_data[user_id].clear()

    return ConversationHandler.END


def is_invalid_shop_code(user_response):
    response_from_db = ShopManager.get_shop_by_code_entered(user_response)

    if len(response_from_db) <= 0:
        return True

    return False


def delete_voucher_from_user_wallet(context, username, user_id):
    LoggerManager.general_logs(
        f"Removing voucher from user {username} ({user_id})'s wallet now")

    user_selected_voucher_id_in_wallet = context.user_data[user_id]['user_selected_voucher'][0]

    response_result = UserManager.delete_voucher_from_user_wallet(
        user_selected_voucher_id_in_wallet)

    if not response_result:
        return

    voucher_id_in_db = context.user_data[user_id]['user_selected_voucher'][1]

    response_result = UserManager.update_user_voucher_history(user_id,
                                                              'claimed',
                                                              voucher_id_in_db)
    if not response_result:
        return

    LoggerManager.general_logs(
        f"Voucher removed from user {username} ({user_id})'s wallet!")

    return True


def inform_user_claim_successful(update, user_selected_voucher_title):
    message_to_send = MessageTemplates.gen_claimed_message(
        user_selected_voucher_title)

    update.message.reply_text(message_to_send)
