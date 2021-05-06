from telegram.ext import ConversationHandler

from src.managers import LoggerManager, TimeManager, UserManager, VoucherManager
from src.templates import MessageTemplates
from . import ReusableComponents

INVALID_PROMOCODE = 'Not Valid'
CLAIMED_BEFORE = 'Claimed'


def promo_code_start(update, context):
    ReusableComponents.log_command_accessed_timing(update)

    result = ReusableComponents.check_membership_status(update)

    if len(result) == 0:
        LoggerManager.general_logs(
            f"User: {update.message.from_user.username} ({update.message.from_user.id}) " +
            "is not an existing member! Redirecting to sign up now!")

        update.message.reply_text(MessageTemplates.new_user_found_message)

        return ConversationHandler.END

    update.message.reply_text(MessageTemplates.prompt_enter_promo_code_message)

    return 'PromoCodeInput'


def promo_code_input(update, context):
    update.message.reply_text(MessageTemplates.loading_message)

    user_id = update.message.from_user.id
    username = update.message.from_user.username
    code_entered_by_user = update.message.text

    vouchers_in_promo_code = validate_promo_code(code_entered_by_user, user_id, username)

    if vouchers_in_promo_code == INVALID_PROMOCODE:
        update.message.reply_text(MessageTemplates.invalid_promo_code_message)

        return 'PromoCodeInput'

    if vouchers_in_promo_code == CLAIMED_BEFORE:
        update.message.reply_text(MessageTemplates.promo_already_claim_message)

    else:
        inform_user_promo_code_result(update, code_entered_by_user, vouchers_in_promo_code)

    ReusableComponents.prompt_user_next_action(update)

    return ConversationHandler.END


def validate_promo_code(code_entered_by_user, user_id, username):
    if claimed_promo_code_before(code_entered_by_user, user_id, username):
        return CLAIMED_BEFORE

    date_today = TimeManager.get_current_date()

    vouchers_in_promo_code = VoucherManager.get_all_promo_code_vouchers(code_entered_by_user, date_today)

    if not vouchers_in_promo_code:
        LoggerManager.general_logs(
            f"Promo code {code_entered_by_user} entered by user {username} ({user_id}) is not valid!")

        return INVALID_PROMOCODE

    return vouchers_in_promo_code


def claimed_promo_code_before(code_entered_by_user, user_id, username):
    if UserManager.user_claimed_promo_code_before(code_entered_by_user, user_id):
        LoggerManager.general_logs(
            f"User {username} ({user_id}) has claimed the promo code {code_entered_by_user} before!")

        return True

    LoggerManager.general_logs(
        f"User {username} ({user_id}) has not claimed the promo code {code_entered_by_user} before! " +
        "Validating code now")

    return False


def inform_user_promo_code_result(update, code_entered_by_user, vouchers_in_promo_code):
    response_result = add_vouchers_to_user_wallet(code_entered_by_user, vouchers_in_promo_code, update)

    if not response_result:
        update.message.reply_text(MessageTemplates.error_message)

        return

    send_vouchers_to_user(update, vouchers_in_promo_code)


def add_vouchers_to_user_wallet(code_entered_by_user, vouchers_in_promo_code, update):
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    LoggerManager.general_logs(
        f"Inserting promo vouchers into user {username} ({user_id})'s wallet in db")

    for voucher in vouchers_in_promo_code:
        voucher_id_in_db = voucher[1]
        voucher_title = voucher[2]
        expiry_date = voucher[8]

        voucher_to_be_added_into_db = {
            'telegram_id': user_id,
            'asset_type': 'coupon',
            'asset_id': voucher_id_in_db,
            'asset_value': 1,
            'expiry_date': expiry_date
        }

        result = UserManager.add_user_voucher(voucher_to_be_added_into_db)

        if not result:
            LoggerManager.exception_logs(
                f"Error occurred while adding {voucher_title} into the db for user {username} ({user_id})")
            return

    promo_voucher_id = vouchers_in_promo_code[0][0]
    VoucherManager.update_voucher_details(promo_voucher_id, 'promocode', 'claimed_amount')

    UserManager.update_user_voucher_history(user_id, code_entered_by_user, None)

    return True


def send_vouchers_to_user(update, vouchers_in_promo_code):
    for voucher_info in vouchers_in_promo_code:
        voucher_path = voucher_info[3]

        voucher_info_to_send = get_voucher_info(voucher_info)

        caption_to_send = MessageTemplates.gen_voucher_info(
            voucher_info_to_send)

        ReusableComponents.dispatch_voucher(update, voucher_path, caption_to_send)


def get_voucher_info(voucher_info):
    voucher_title = voucher_info[2]
    business_hours = "-" if not voucher_info[4] else voucher_info[4]
    location = "-" if not voucher_info[5] else voucher_info[5]
    website = "-" if not voucher_info[6] else voucher_info[6]
    phone = "-" if not voucher_info[7] else voucher_info[7]
    expiry_date = voucher_info[8]

    voucher_info = {
        'voucher_name': voucher_title,
        'expiry_date': expiry_date,
        'business_hours': business_hours,
        'location': location,
        'website': website,
        'phone': phone,
    }

    return voucher_info
