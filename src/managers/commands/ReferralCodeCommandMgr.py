from src.managers import LoggerManager, UserManager
from src.templates import MessageTemplates
from . import ReusableComponents


def referral_code_instruction_start(update, context):
    ReusableComponents.log_command_accessed_timing(update)

    user_id = update.message.from_user.id
    username = update.message.from_user.username

    referral_code = get_user_referral_code(user_id)

    if not referral_code:
        LoggerManager.general_logs(f"User {username} ({user_id} is not a member!")

        update.message.reply_text(MessageTemplates.new_user_found_message)

        return

    update.message.reply_text(MessageTemplates.referral_code_info_message)
    update.message.reply_text(MessageTemplates.gen_referral_code_instruction_template(referral_code),
                              disable_web_page_preview=True)

    ReusableComponents.prompt_user_next_action(update)


def get_user_referral_code(user_id):
    referral_code_result = UserManager.get_user_referral_code(user_id)

    if len(referral_code_result) <= 0:
        return False

    return referral_code_result[0][0]
