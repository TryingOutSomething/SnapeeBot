from telegram.ext import ConversationHandler

from src.managers import LoggerManager, TimeManager, UserManager, VoucherManager
from src.templates import MessageTemplates
from . import ReusableComponents

EMPTY_LIST_LENGTH = ReusableComponents.EMPTY_LIST_LENGTH
MINIMUM_VOUCHER_INDEX_RANGE = 0


def exchange_start(update, context):
    ReusableComponents.log_command_accessed_timing(update)

    update.message.reply_text(MessageTemplates.loading_message)

    user_id = update.message.from_user.id
    username = update.message.from_user.username

    if is_not_a_registered_member(update):
        LoggerManager.general_logs(
            f"User: {username} ({user_id}) is not a member. Redirecting to registration now.")

        update.message.reply_text(MessageTemplates.new_user_found_message)

        return ConversationHandler.END

    exchangeable_voucher_list = UserManager.get_user_exchangeable_vouchers_and_snapcoin_amt(user_id)

    if len(exchangeable_voucher_list) <= EMPTY_LIST_LENGTH:
        LoggerManager.general_logs(f"No vouchers to exchange currently.")

        update.message.reply_text(MessageTemplates.no_vouchers_claimable_message)
        ReusableComponents.prompt_user_next_action(update)

        return ConversationHandler.END

    send_exchangeable_message_to_user(update, context, exchangeable_voucher_list)

    return 'ExchangeInput'


def is_not_a_registered_member(update):
    result = ReusableComponents.check_membership_status(update)
    return len(result) <= EMPTY_LIST_LENGTH


def send_exchangeable_message_to_user(update, context, exchangeable_voucher_list):
    user_id = str(update.message.from_user.id)

    context.chat_data.update({
        f'{user_id}': {'exchangeable_vouchers_record': exchangeable_voucher_list}
    })

    exchangeable_vouchers_message = MessageTemplates.gen_exchangeable_vouchers_message(
        exchangeable_voucher_list)

    update.message.reply_text(exchangeable_vouchers_message)


def exchange_input(update, context):
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username

    user_choice = update.message.text

    user_selected_voucher = is_valid_choice(user_choice, context, user_id)

    if not user_selected_voucher:
        update.message.reply_text(MessageTemplates.invalid_input_message)

        return "ExchangeInput"

    if user_is_not_able_to_afford_voucher(user_selected_voucher):
        update.message.reply_text(MessageTemplates.not_enough_snapcoin_to_exchange_message)

        return "ExchangeInput"

    send_confirmation_voucher_to_user(update, user_selected_voucher)

    response_result = add_voucher_to_user_wallet(user_selected_voucher,
                                                 user_id,
                                                 username)

    if not response_result:
        update.message.reply_text(MessageTemplates.error_message)

    else:
        inform_exchange_result_to_user(update, user_selected_voucher)

    ReusableComponents.prompt_user_next_action(update)

    context.chat_data[user_id].clear()

    return ConversationHandler.END


def is_valid_choice(user_choice, context, user_id):
    if not user_choice.isdigit():
        return None

    user_choice_in_int = int(user_choice) - 1
    list_of_exchangeable_vouchers = context.chat_data[user_id]['exchangeable_vouchers_record']

    if user_choice_in_int > len(list_of_exchangeable_vouchers) or user_choice_in_int < 0:
        return None

    return list_of_exchangeable_vouchers[user_choice_in_int]


def user_is_not_able_to_afford_voucher(user_selected_voucher):
    user_snapcoin_amt = user_selected_voucher[0]
    voucher_cost = user_selected_voucher[9]

    if user_snapcoin_amt < voucher_cost:
        return True

    return False


def send_confirmation_voucher_to_user(update, user_selected_voucher):
    chosen_voucher_title = user_selected_voucher[2]
    message_to_send = MessageTemplates.gen_user_chosen_voucher_message(
        chosen_voucher_title)

    update.message.reply_text(message_to_send)


def add_voucher_to_user_wallet(user_selected_voucher, user_id, username):
    expiry_date = TimeManager.gen_expiry_date()
    voucher_id_in_db = user_selected_voucher[1]
    voucher_title = user_selected_voucher[2]
    exchange_fee = user_selected_voucher[9]

    voucher_to_be_added_into_db = {
        'telegram_id': user_id,
        'asset_type': 'coupon',
        'asset_id': voucher_id_in_db,
        'asset_value': 1,
        'expiry_date': expiry_date
    }

    result = UserManager.add_user_voucher(voucher_to_be_added_into_db)

    if result:
        exchange_voucher_id_to_be_updated = user_selected_voucher[8]

        VoucherManager.update_voucher_details(
            exchange_voucher_id_to_be_updated, 'exchangecoupons', 'issueamount')

        UserManager.update_user_snapcoin_amt(exchange_fee, '-', user_id)
        UserManager.update_user_voucher_history(user_id,
                                                'exchanged',
                                                voucher_id_in_db)

        return True

    LoggerManager.exception_logs(
        f"Error occurred while adding {voucher_title} voucher to user {username} ({user_id})'s wallet!")


def inform_exchange_result_to_user(update, user_selected_voucher):
    voucher_info = get_voucher_info(user_selected_voucher)

    caption_to_send = MessageTemplates.gen_voucher_info(voucher_info)

    voucher_path = user_selected_voucher[3]

    ReusableComponents.dispatch_voucher(update, voucher_path, caption_to_send)


def get_voucher_info(user_selected_voucher):
    voucher_title = user_selected_voucher[2]
    expiry_date = TimeManager.gen_expiry_date_in_d_m_y()
    business_hours = "-" if not user_selected_voucher[4] else user_selected_voucher[4]
    location = "-" if not user_selected_voucher[5] else user_selected_voucher[5]
    website = "-" if not user_selected_voucher[6] else user_selected_voucher[6]
    phone = "-" if not user_selected_voucher[7] else user_selected_voucher[7]

    voucher_info = {
        'voucher_name': voucher_title,
        'expiry_date': expiry_date,
        'business_hours': business_hours,
        'location': location,
        'website': website,
        'phone': phone,
    }

    return voucher_info
