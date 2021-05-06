from src.managers import LoggerManager, TimeManager, UserManager, VoucherManager
from src.templates import MessageTemplates
from .. import ReusableComponents


def add_coin_to_user_wallet(snapcoin_amount, arithmetic_operator, user_id, username):
    result = UserManager.update_user_snapcoin_amt(snapcoin_amount,
                                                  arithmetic_operator,
                                                  user_id)

    logging_message = f"{snapcoin_amount} to user {username} ({user_id})'s wallet!"

    if result:
        LoggerManager.general_logs(f"Successfully added {logging_message}")

        return True

    else:
        LoggerManager.exception_logs(
            f"Error occurred while adding {logging_message}")


def add_voucher_to_user_wallet(voucher_info, user_id, username):
    expiry_date = TimeManager.gen_expiry_date()
    voucher_id_in_db = voucher_info[2]

    voucher_to_be_added_into_db = {
        'telegram_id': user_id,
        'asset_type': 'coupon',
        'asset_id': voucher_id_in_db,
        'asset_value': 1,
        'expiry_date': expiry_date
    }

    result = UserManager.add_user_voucher(voucher_to_be_added_into_db)

    logging_message = f"{voucher_info[0]} voucher to user {username} ({user_id})'s wallet!"

    if result:
        LoggerManager.general_logs(f"Successfully added {logging_message}")

        voucher_id_to_be_updated = voucher_info[7]

        VoucherManager.update_voucher_details(voucher_id_to_be_updated,
                                              'dailycoupons',
                                              'issueamount'
                                              )

        return True

    else:
        LoggerManager.exception_logs(
            f"Error occurred while adding {logging_message}")


def send_voucher_to_user(update, reward_of_the_day):
    voucher_path = reward_of_the_day[1]
    voucher_info = get_voucher_info(reward_of_the_day)

    caption_to_send = MessageTemplates.gen_voucher_info(voucher_info)

    ReusableComponents.dispatch_voucher(update, voucher_path, caption_to_send)


def get_voucher_info(reward_of_the_day):
    voucher_title = reward_of_the_day[0]
    expiry_date = TimeManager.gen_expiry_date_in_d_m_y()
    business_hours = "-" if not reward_of_the_day[3] else reward_of_the_day[3]
    location = "-" if not reward_of_the_day[4] else reward_of_the_day[4]
    website = "-" if not reward_of_the_day[5] else reward_of_the_day[5]
    phone = "-" if not reward_of_the_day[7] else reward_of_the_day[7]

    voucher_info = {
        'voucher_name': voucher_title,
        'expiry_date': expiry_date,
        'business_hours': business_hours,
        'location': location,
        'website': website,
        'phone': phone,
    }

    return voucher_info
