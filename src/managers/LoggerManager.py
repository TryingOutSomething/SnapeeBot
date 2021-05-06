import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def init_command_log(username, id, command):
    logger.info(f"User: {username} ({id}) accessed {command} command")


def general_logs(message):
    logger.info(message)


def telegram_error_logs(update, context):
    logger.warning(f"Update {update} caused error {context.error}")


def exception_logs(error):
    logger.error(error)


def gen_blocked_users_template(error_occurred_while_sending_to_users_dict, date_today, time_today):
    blocked_users = '\n'.join(
        error_occurred_while_sending_to_users_dict['blocked_users'])

    unreachable_users = '\n'.join(
        error_occurred_while_sending_to_users_dict['unreachable_users'])

    unexpected_error_users = '\n'.join(
        error_occurred_while_sending_to_users_dict['unreachable_users'])

    template = (
        f"{date_today} {time_today} \n\n"
        f"Blocked Users: {blocked_users} \n\n" +
        f"Unreachable Users: {unreachable_users} \n\n"
        f"Unexpected Error Users: {unexpected_error_users}"
    )

    return template
