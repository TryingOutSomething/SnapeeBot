from random import randrange, choice

from src.managers import VoucherManager, LoggerManager

_new_user_login_coin_list = [100, 200, 300, 400]
_weekly_login_coin_list = [100, 300, 500, 700]

REFERRAL_BONUS_AMT = 500


def get_new_user_reward_of_the_day(login_day):
    if login_day == 1:
        return get_random_new_user_voucher()

    index_for_snapcoin_reward = login_day - 2
    return _new_user_login_coin_list[index_for_snapcoin_reward]


def get_random_new_user_voucher():
    vouchers = VoucherManager.get_all_allocated_new_user_vouchers()

    if len(vouchers) == 0:
        LoggerManager.exception_logs(
            "There are not vouchers allocated for new user bonus!")

    if len(vouchers) > 1:
        random_voucher_index = randomize_voucher_index(len(vouchers))

    else:
        random_voucher_index = 0

    return vouchers[random_voucher_index]


def randomize_voucher_index(voucher_list_length):
    return randrange(voucher_list_length - 1)


def get_random_weekly_snapcoin_amt():
    return choice(_weekly_login_coin_list)


# def get_random_weekly_voucher():
#     vouchers = VoucherManager.get_all_allocated_vouchers('weekly_login')

#     if len(vouchers) == 0:
#         LoggerManager.exception_logs(
#             "There are not vouchers allocated for weekly login bonus!")
#         return

#     if len(vouchers) > 1:
#         random_voucher_index = randomize_voucher_index(len(vouchers))
#     else:
#         random_voucher_index = 0

#     return vouchers[random_voucher_index]
