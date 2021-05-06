from src.managers import LoggerManager, RewardManager, TimeManager, UserManager, VoucherManager
from src.templates import MessageTemplates
from . import SharedFunctions

MAX_NO_OF_TIMES_CLAIMABLE = 2


def handle_user_weekly_login_reward(update, user_id, username):
    login_details = UserManager.get_user_weekly_login_details(user_id)

    result = not_claimed_weekly_bonus_before(login_details, user_id, username)

    if result == 'Claimed':
        update.message.reply_text(
            MessageTemplates.already_claimed_weekly_bonus_message)

        return

    response_result = give_weekly_login_bonus_reward(result,
                                                     user_id,
                                                     username)

    inform_weekly_reward_received(update, response_result)


def not_claimed_weekly_bonus_before(user_login_details, user_id, username):
    if not user_login_details:
        LoggerManager.general_logs(
            f"User {username} ({user_id}) has not claimed weekly login bonus for this week.")
        return UserManager.get_user_allocated_bonus(user_id)

    last_weekly_login_date = user_login_details[0][0]
    date_today = TimeManager.get_current_date()

    if len(user_login_details) < MAX_NO_OF_TIMES_CLAIMABLE and last_weekly_login_date < date_today:
        LoggerManager.general_logs(
            f"User {username} ({user_id}) has not fully claimed weekly login bonus for this week.")

        return UserManager.get_user_allocated_bonus(user_id)

    LoggerManager.general_logs(
        f"User {username} ({user_id}) has already claimed weekly login bonus for the week {len(user_login_details)} times. " +
        f"Last claimed on {last_weekly_login_date}")

    return 'Claimed'


def give_weekly_login_bonus_reward(user_login_details, user_id, username):
    bonus_type_allocated = user_login_details[0][0]

    logged_message = f"User {username} ({user_id}) is getting"

    response_result = False

    if bonus_type_allocated == 0:
        response_result = give_weekly_snapcoin_to_user(logged_message,
                                                       user_id,
                                                       username)

    else:
        response_result = give_weekly_voucher_to_user(bonus_type_allocated,
                                                      user_id,
                                                      username)

    date_today = TimeManager.get_current_date()
    UserManager.update_weekly_bonus_tracker(date_today, user_id)

    return response_result


def give_weekly_snapcoin_to_user(logged_message, user_id, username):
    snapcoin_amount = RewardManager.get_random_weekly_snapcoin_amt()

    LoggerManager.general_logs(
        f"{logged_message} {snapcoin_amount} snapcoins today!")

    response_result = SharedFunctions.add_coin_to_user_wallet(snapcoin_amount,
                                                              '+',
                                                              user_id,
                                                              username)
    if response_result:
        return snapcoin_amount


def give_weekly_voucher_to_user(allocated_voucher_id, user_id, username):
    voucher_info = VoucherManager.get_weekly_allocated_voucher(
        allocated_voucher_id)

    response_result = SharedFunctions.add_voucher_to_user_wallet(voucher_info[0],
                                                                 user_id,
                                                                 username)

    if response_result:
        return voucher_info[0]


def inform_weekly_reward_received(update, reward_result):
    if not reward_result:
        update.message.reply_text(MessageTemplates.error_message)
        return

    if isinstance(reward_result, int):
        message_to_send = MessageTemplates.gen_weekly_bonus_snapcoin_message(
            reward_result)

        update.message.reply_text(message_to_send)

        return

    SharedFunctions.send_voucher_to_user(update, reward_result)
