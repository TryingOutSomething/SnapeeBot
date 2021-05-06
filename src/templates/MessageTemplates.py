from src.managers import TimeManager

TIMEOUT_DURATION_IN_MINUTES = TimeManager.TIMEOUT_DURATION_IN_MINUTES
MINIMUM_SNAPCOINS_AMT = 1000
MINIMUM_REFERRAL_SNAPCOINS_AMT = 500
_NO_BLOCKED_USERS = 0

# General specific messages
ask_user_action_message = "What would you like to do next? 😄"
loading_message = "Please give me a moment to retrieve the information 😊"
feedback_message = "\nEncountered a bug or have a suggestion? \nLet us know here: @snapeeassistant"
error_message = "OMG you found something! 🎉 \n\npm @snapeeassistant to find out more 😉"
invalid_response_message = "Please enter a valid response!"
cancel_option_message = "Click /cancel to cancel the current action."
cancel_action_message = "Current action cancelled! \n\nPlease select your option:"
invalid_input_message = f"Your input does not match any of the vendors. Please try again. \n{cancel_option_message}"
auto_cancel_message = f"\nAuto cancel in {TIMEOUT_DURATION_IN_MINUTES} mins!"
action_auto_cancelled_message = "Previous action has been cancelled ~"

# /start message specific messages
start_message = "Welcome onboard my fellow voucher hunter! I'm Snapee, your hunting buddy."
new_user_found_message = f"This journey will be filled with exciting games, quests and attractive vouchers! " \
                         f"\n\nClick /signup to kickstart your journey to the land of amazing deals. " \
                         f"\n\n🔥 pm @snapeeassistant for more info 🔥 \n{feedback_message} "


def welcome_back_message(username):
    return f"Welcome back {username}! \n{feedback_message}"


def gen_referrer_bonus_message(referee_username):
    return f"Congratulations! Your friend {referee_username} referred you during their registration. You got 500 " \
           f"SnapCoins! "


def gen_welcome_new_user_message(username):
    return f'Welcome aboard {username}!\n\n' + basic_info()


def basic_info():
    return ("Basic Info:\n" +
            "🔻 /wallet access to your vouchers and rewards. \n" +
            "🔻 /exchange list of vouchers & prizes available to redeem with snapcoins. \n" +
            "🔻 /promocode enter unique code from event or partner. \n" +
            "🔻 /quests send photos, receipts & answer polls to earn snapcoins weekly. \n\n" +
            "🔻 /referralcode refer a friend to get 500 snapcoins. \n\n" +
            "How to redeem my vouchers? \n" +
            "1. Open /wallet \n" +
            "2. Select the ow of the voucher \n" +
            "3. Enter partner’s 4-digit code \n\n" +
            "Are you ready? Let's start hunting! 🎉"
            )


# /signup specific messages
ask_email_message = "What\'s your email address?"
ask_gender_message = "Next, can you tell me your gender?"
skip_referral_message = "Click /skip to proceed without referral code"
ask_referral_message = "Enter referral code \n\nIf you were introduced by your friend, enter their referral code to " \
                       "get additional rewards! 😊 \n\n" + skip_referral_message
congratulate_referee_message = "Congratulations! You and your friend will both receive 500 SnapCoins!"
new_user_create_message = "Thank you! Give me a moment while I register you!"
new_reward_message = "🎉 SURPRISE BOX FOR NEW USER! 🎉 \n\nEvery surprise box contains voucher(s) or " \
                     "snapcoins from our merchants. \n\n/open to get your gift! 😉 "
invalid_email_message = "Please enter an email address!"
invalid_referrer_message = "Invalid referral code. Please enter again!\n\n" + \
                           skip_referral_message
new_user_turnback_message = "\n\nClick /cancel if you don't want to get amazing vouchers from us 😢"
ask_referral_confirm_skip_message = "Are you sure, you can't enter it again!~"
registration_cancel_message = "Oh man... Are you sure? You will miss out all the vouchers and brands that you like 😞" \
                              "\n\nJoin us again by clicking /signup "
existing_user_message = f"You are already an existing user! \n{feedback_message}"

# /open specific messages
already_claimed_weekly_bonus_message = "You have already claimed your login bonus for this week! Please check again " \
                                       "next Monday!\n" + feedback_message
weekend_message = f"You are only able to claim your login bonus on weekdays! Please check again next Monday!" \
                  f"\n{feedback_message}"


def gen_new_user_coin_message(snapcoin_amount, no_of_days_as_new_user):
    return f"You have received: \n{snapcoin_amount} snapcoins" \
           f"\n\nFor logging in for {no_of_days_as_new_user} day(s)!\n\n"


def gen_weekly_bonus_snapcoin_message(snapcoin_amount):
    return f"You have received {snapcoin_amount} snapcoins for this week! {feedback_message}"


# /exchange specific messages
not_enough_snapcoin_to_exchange_message = "You have insufficient snapcoins! Please enter another number. \n\n" \
                                          f"{cancel_option_message} {auto_cancel_message}"

no_vouchers_claimable_message = "All vouchers are fully exchanged. Please check again later."


def gen_exchangeable_vouchers_message(exchangeable_vouchers_info):
    user_current_snapcoin_amount = exchangeable_vouchers_info[0][0]
    exchangeable_voucher_list = []

    for i, voucher in enumerate(exchangeable_vouchers_info):
        voucher_title = voucher[2]
        voucher_fee = voucher[9]
        voucher_number = f"{i + 1}. {voucher_title} ({voucher_fee})\n\n"

        exchangeable_voucher_list.append(voucher_number)

    exchangeable_voucher_list_in_str_format = ''.join(
        exchangeable_voucher_list)

    message = (
            f"🎟 EXCHANGE 🎟 \n" +
            f"You have {user_current_snapcoin_amount} snapcoins to exchange for vouchers! 🧐 \n\n" +
            f"{exchangeable_voucher_list_in_str_format} \n" +
            f"To exchange the voucher, type the row number! 🎊 \n\n{cancel_option_message} {auto_cancel_message}"
    )

    return message


# /wallet specific messages
confirm_claim_message = f"Enter the 4-digit code from our partners to complete the claim." \
                        f"\n\n{cancel_option_message} {auto_cancel_message}"
invalid_shop_code_message = f"The 4-digit code is incorrect. Please enter again! " \
                            f"\n\n{cancel_option_message} {auto_cancel_message}"


def gen_user_profile_message(dict_of_vouchers_owned_by_user, user_snapcoin_amount):
    user_snapcoin_amt = user_snapcoin_amount[0][0]

    claimable_voucher_message, expired_voucher_message = gen_voucher_list_message(
        dict_of_vouchers_owned_by_user)

    message = (
            f"👛 MY WALLET 👛 \n"
            f"You have {user_snapcoin_amt} snapcoins. \n\n" +
            f"My Vouchers 🎟 \n{claimable_voucher_message}"
    )

    return expired_voucher_message, message


def gen_voucher_list_message(dict_of_vouchers_owned_by_user):
    expired_vouchers_list = None
    non_expired_vouchers_list = None

    if 'expired_vouchers' in dict_of_vouchers_owned_by_user:
        expired_vouchers_list = dict_of_vouchers_owned_by_user['expired_vouchers']

    if 'non_expired_vouchers' in dict_of_vouchers_owned_by_user:
        non_expired_vouchers_list = dict_of_vouchers_owned_by_user['non_expired_vouchers']

    claimable_voucher_message = gen_claimable_voucher_message(
        non_expired_vouchers_list)

    expired_voucher_message = gen_expired_voucher_message(
        expired_vouchers_list)

    return claimable_voucher_message, expired_voucher_message


def gen_claimable_voucher_message(non_expired_vouchers_list):
    claimable_voucher_message = ""

    if not non_expired_vouchers_list:
        return "You do not have any vouchers to claim"

    for i, voucher_info in enumerate(non_expired_vouchers_list):
        voucher_title = voucher_info[2]
        voucher_expiry_date = voucher_info[8]
        voucher_expiry_date_in_d_m_y_format = TimeManager.convert_date_to_d_m_y_format(
            voucher_expiry_date)

        voucher_number = f"{i + 1}. {voucher_title} (Expires {voucher_expiry_date_in_d_m_y_format})\n\n"

        claimable_voucher_message += voucher_number

    additional_message = ("\n" +
                          "To claim the voucher, type the row number! E.g \"1\" \n\n" +
                          f"{cancel_option_message} \n {auto_cancel_message}"
                          )

    claimable_voucher_message += additional_message

    return claimable_voucher_message


def gen_expired_voucher_message(expired_vouchers_list):
    expired_voucher_message = "The following voucher(s) are expired: \n"

    if not expired_vouchers_list:
        return

    for i, voucher_info in enumerate(expired_vouchers_list):
        voucher_title = voucher_info[2]
        voucher_number = f"{i + 1}. {voucher_title}\n\n"

        expired_voucher_message += voucher_number

    return expired_voucher_message


def gen_claimed_message(user_selected_voucher_title):
    date_today = TimeManager.get_current_date_in_d_m_y()
    current_time = TimeManager.get_current_time()

    message = (
            f"🎉 CLAIM SUCCESSFUL 🎉 \n\n{user_selected_voucher_title} \n\n" +
            f"🔻 Date of claim: {date_today} \n🔻 Time of claim: {current_time}\n\n" +
            "Flash this message to our merchant to verify! 😉"
    )

    return message


def gen_voucher_info(voucher_info, is_claim=False):
    voucher_name = voucher_info['voucher_name']
    expiry_date = voucher_info['expiry_date']
    website = voucher_info['website']
    location = f"📍 {voucher_info['location']}"
    business_hours = f"⏰ {voucher_info['business_hours']}"
    phone = f"📞 {voucher_info['phone']}"

    message = (
            f"{voucher_name}! \nExpires on {expiry_date}\n\n" +
            f"📝 Terms & Conditions\n" +
            f"{website} \n" +
            f"{location} \n" +
            f"{business_hours} \n" +
            f"{phone}"
    )

    if is_claim:
        return f"You have selected {message}"

    return f"You received {message}"


def gen_user_chosen_voucher_message(chosen_voucher_title):
    return f"You have chosen: {chosen_voucher_title} \n\n{loading_message}"


# /promocode specific messages
prompt_enter_promo_code_message = f"🎉 PROMOCODE 🎉 \n" \
                                  f"Enter the unique code given by our partners or event organizers " \
                                  f"to get your exclusive rewards \n\n" \
                                  f"{cancel_option_message} {auto_cancel_message}"
promo_already_claim_message = f"You have claimed this code before! \nYou can only claim this promotional code once. " \
                              f"\n{feedback_message}"
invalid_promo_code_message = "Invalid promo code! Please enter again."

# /mass specific messages
prompt_send_image_or_text_message = "Do you want to send image or text?"
prompt_sender_to_enter_text_message = "Enter message to send:"
prompt_sender_to_upload_image_message = "Upload image to send:"
prompt_sender_if_they_want_to_add_caption_to_image_message = "Do you want to include caption in the image?"
prompt_sender_to_enter_caption_text_message = "Enter caption text:"
prompt_sender_to_enter_anything_message = "Got it! Input anything to send the image to user."
empty_user_list_message = "No users in the list!"


def gen_message_to_inform_sender(length_of_users):
    return f"Sending to {length_of_users} user(s) now."


def gen_error_message_while_sending_to_user(user_id):
    return f"Something went wrong while sending message to user {user_id}."


def gen_broadcast_report(error_occurred_while_sending_to_users_dict):
    length_of_blocked_users = len(
        error_occurred_while_sending_to_users_dict['blocked_users'])

    length_of_unreachable_users = len(
        error_occurred_while_sending_to_users_dict['unreachable_users'])

    length_of_unexpected_error_while_sending_to_users = len(
        error_occurred_while_sending_to_users_dict['unexpected_errors'])

    total_numbers_of_users_affected_by_error = length_of_blocked_users + \
                                               length_of_unreachable_users + \
                                               length_of_unexpected_error_while_sending_to_users

    report_message = "Done sending message!"

    if total_numbers_of_users_affected_by_error > _NO_BLOCKED_USERS:
        report_message += gen_error_while_broadcasting_to_users_message(length_of_blocked_users,
                                                                        length_of_unreachable_users,
                                                                        length_of_unexpected_error_while_sending_to_users,
                                                                        total_numbers_of_users_affected_by_error)

    else:
        report_message += gen_successful_broadcast_message_report()

    return report_message


def gen_successful_broadcast_message_report():
    return "\n\nMessage sent successfully!"


def gen_error_while_broadcasting_to_users_message(length_of_blocked_users,
                                                  length_of_unreachable_users,
                                                  length_of_unexpected_error_while_sending_to_users,
                                                  total_numbers_of_users_affected_by_error):
    message = (
            "\n\nREPORT SUMMARY:\n" +
            f"Unable to send to {total_numbers_of_users_affected_by_error} users in total! \n\n" +
            f"{length_of_blocked_users} users have blocked the bot or telegram block the bot for them. \n" +
            f"{length_of_unreachable_users} users have not initiated contact with the bot for some reason. \n" +
            f"Unable to send to {length_of_unexpected_error_while_sending_to_users} users due to unknown factors. "
            f"Please check with the dev team."
    )

    return message


# /quests specific messages
quest_image_sent_message = "Photo sent! 😊 \n\nIt will take awhile to verify the photo. In the meantime, " \
                           "complete more quests and games to win more rewards. "


def send_quest_image_message(list_of_available_quests):
    list_of_available_quests_to_string = ""
    quest_message = ""

    list_of_available_quests_to_string = "\n\n".join([f"{i + 1}. {quest}"
                                                      for i, row in enumerate(list_of_available_quests)
                                                      for quest in row])

    quest_message = (f"📸 QUEST TIME 📸 \n" +
                     f"Complete quests to earn rewards. Quests may change every week! \n\n" +
                     f"{list_of_available_quests_to_string}\n\n" +
                     "To view the quest, type the row number! E.g \"1\" \n\n" +
                     f"{cancel_option_message} {auto_cancel_message}"
                     )

    return quest_message


def gen_quest_description_message(quest_title, quest_description):
    return f"{quest_title} \n\n{quest_description[0][0]} \n\n\n{cancel_option_message} {auto_cancel_message}"


# /referralcode specific messages
referral_code_info_message = f"Forward the message below to your friends to earn {MINIMUM_REFERRAL_SNAPCOINS_AMT} " \
                             f"snapcoins for every signup 😊"


def gen_referral_code_instruction_template(user_referral_code):
    return (
            "Start your reward journey with Snapee! Collect vouchers and snapcoins " +
            "by completing quests and play weekly games. \n\n" +
            "To Sign-up: \n" +
            "1. Click 👉 @snapee_bot and click \"Start\" \n" +
            "2. Enter your email \n" +
            "3. Select your gender \n" +
            f"4. Enter the referral code: {user_referral_code} \n\n\n" +
            f"Get {MINIMUM_REFERRAL_SNAPCOINS_AMT} snapcoins as a head start 😍 \n\n" +
            "🌐 https://www.snapee.co/"
    )
