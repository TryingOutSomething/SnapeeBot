from src.managers import TimeManager, UserManager


def filter_expired_and_non_expired_vouchers(list_of_vouchers_owned_by_user, user_id):
    expired_voucher_list = []
    non_expired_voucher_list = []

    for voucher_info in list_of_vouchers_owned_by_user:
        voucher_expiry_date = voucher_info[8]

        if voucher_is_expired(voucher_expiry_date):
            voucher_id = voucher_info[1]
            user_asset_id = voucher_info[0]

            expired_voucher_list.append(voucher_info)

            remove_expired_voucher_from_db(user_id, user_asset_id, voucher_id)

            continue

        non_expired_voucher_list.append(voucher_info)

    filtered_list_of_vouchers = {
        'non_expired_vouchers': non_expired_voucher_list,
        'expired_vouchers': expired_voucher_list
    }

    return filtered_list_of_vouchers


def voucher_is_expired(voucher_expiry_date):
    date_today = TimeManager.get_current_date()

    result = voucher_expiry_date < date_today

    return result


def remove_expired_voucher_from_db(user_id, user_asset_id, voucher_id):

    UserManager.update_user_voucher_history(user_id,
                                            'expired',
                                            voucher_id)

    UserManager.delete_voucher_from_user_wallet(user_asset_id)
