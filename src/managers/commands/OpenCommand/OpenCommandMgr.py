from src.templates import MessageTemplates
from . import NewUserRewardMgr, WeeklyRewardMgr
from .. import ReusableComponents

MAX_NO_OF_DAYS_AS_NEW_USER = 5


def surprise_box_start(update, context):
    update.message.reply_text(MessageTemplates.loading_message)

    ReusableComponents.log_command_accessed_timing(update)

    user_id = update.message.from_user.id
    username = update.message.from_user.username

    surprise_box_handler(update, user_id, username)


def surprise_box_handler(update, user_id, username):
    reward_is_issued_successfully = NewUserRewardMgr.handle_new_user_reward(update, user_id, username)

    if not reward_is_issued_successfully:
        return

    WeeklyRewardMgr.handle_user_weekly_login_reward(update, user_id, username)

    ReusableComponents.prompt_user_next_action(update)
    # End of Surprise box command
