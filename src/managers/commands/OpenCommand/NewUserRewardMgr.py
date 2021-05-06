from src.managers import LoggerManager, RewardManager, TimeManager, UserManager
from src.templates import MessageTemplates
from . import SharedFunctions

MAX_NO_OF_DAYS_AS_NEW_USER = 5


def handle_new_user_reward(update, user_id, username):
    result = UserManager.get_new_user_login_details(user_id)

    if user_does_not_exists(result, update):
        return False

    if not claimed_new_user_bonus_before(result, user_id, username):
        reward_of_the_day = give_new_user_bonus_reward(result,
                                                       user_id,
                                                       username)

        inform_new_user_reward_received(update, result, reward_of_the_day)

    return True


def user_does_not_exists(user_login_details, update):
    if len(user_login_details) <= 0:
        LoggerManager.general_logs(
            f"User: {update.message.from_user.username} ({update.message.from_user.id}) " +
            "is not an existing member! Redirecting to sign up now!")

        update.message.reply_text(MessageTemplates.new_user_found_message)

        return True

    return False


def claimed_new_user_bonus_before(user_login_details, user_id, username):
    LoggerManager.general_logs(
        f"Checking login details of user {username} ({user_id}).")

    no_of_days_as_new_user = user_login_details[0][0]
    last_new_user_login_date = user_login_details[0][1]

    date_today = TimeManager.get_current_date()

    if no_of_days_as_new_user > MAX_NO_OF_DAYS_AS_NEW_USER or last_new_user_login_date >= date_today:
        LoggerManager.general_logs(
            f"User {username} ({user_id}) has already claimed new user bonus before. " +
            f"{no_of_days_as_new_user} times, latest date: {last_new_user_login_date}")

        return True

    LoggerManager.general_logs(
        f"User {username} ({user_id}) has not claimed new user bonus for today. Receiving day {no_of_days_as_new_user} "
        f"reward today")


def give_new_user_bonus_reward(user_login_details, user_id, username):
    no_of_days_as_new_user = user_login_details[0][0]

    reward_of_the_day = RewardManager.get_new_user_reward_of_the_day(
        no_of_days_as_new_user)

    response_result = give_reward_base_on_type(reward_of_the_day,
                                               user_id,
                                               username)

    updated_no_of_days_as_new_user = no_of_days_as_new_user + 1
    date_today = TimeManager.get_current_date()
    UserManager.update_new_user_tracker(updated_no_of_days_as_new_user,
                                        date_today,
                                        user_id)

    if response_result:
        return reward_of_the_day


def give_reward_base_on_type(reward_of_the_day, user_id, username):
    logging_message = f"Updating user {username} ({user_id})'s wallet"

    response_result = False

    if reward_is_voucher(reward_of_the_day):
        voucher_info = reward_of_the_day

        LoggerManager.general_logs(
            f"{logging_message}. Adding voucher {voucher_info[0]} into the wallet")

        response_result = SharedFunctions.add_voucher_to_user_wallet(voucher_info,
                                                                     user_id,
                                                                     username)

    elif reward_is_snapcoin(reward_of_the_day):
        snapcoin_amount = reward_of_the_day

        LoggerManager.general_logs(
            f"{logging_message}. Adding {snapcoin_amount} snapcoins into the wallet")

        response_result = SharedFunctions.add_coin_to_user_wallet(snapcoin_amount,
                                                                  '+',
                                                                  user_id,
                                                                  username)

    else:
        LoggerManager.exception_logs(
            f"Unknown reward. Error occurred somewhere")

    return response_result


def inform_new_user_reward_received(update, user_login_details, reward_of_the_day):
    if not reward_of_the_day:
        update.message.reply_text(MessageTemplates.error_message)
        return

    if isinstance(reward_of_the_day, tuple):
        SharedFunctions.send_voucher_to_user(update, reward_of_the_day)

        return

    no_of_days_as_new_user = user_login_details[0][0]

    message_to_send = MessageTemplates.gen_new_user_coin_message(reward_of_the_day,
                                                                 no_of_days_as_new_user)

    update.message.reply_text(message_to_send)


def reward_is_voucher(reward_earned):
    return isinstance(reward_earned, tuple)


def reward_is_snapcoin(reward_earned):
    return isinstance(reward_earned, int)
