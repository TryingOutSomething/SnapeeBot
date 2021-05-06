import os

import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

from src.managers import LoggerManager, TimeManager

_admin_info_file_path = './assets/bot_related/admin_info.txt'
_blocked_user_file_path = './assets/bot_related/error_log_from_broadcast.txt'
_bonus_image_path = './assets/bot_related/surprise_box_compressed.jpeg'

load_dotenv()


def get_project_environment():
    return os.getenv("PYTHON_ENV")


def retrieve_token():
    return os.getenv("TELEGRAM_BOT_TOKEN")


def get_server_port():
    return os.getenv("SERVER_PORT")


def get_webhook_base_url():
    return os.getenv("WEBHOOK_BASE_URL")


def get_db_conn_details():
    HOST = os.getenv('SQL_CONNECTION_HOST')
    USERNAME = os.getenv('SQL_CONNECTION_USERNAME')
    PASSWORD = os.getenv('SQL_CONNECTION_PASSWORD')
    PORT = os.getenv('SQL_CONNECTION_PORT')

    return HOST, PORT, USERNAME, PASSWORD


def get_snapee_bonus_poster_path():
    return _bonus_image_path


def get_list_of_admins():
    try:
        with open(_admin_info_file_path, 'r') as file:
            return [line.strip() for line in file]
    except Exception as e:
        LoggerManager.exception_logs(e)
        LoggerManager.exception_logs("Error occurred while getting admin list")


def get_snapee_asst_id():
    return os.getenv("SNAPEE_ASSISTANT_ID")


def authorize_google_sheet_access():
    google_sheet_credential_path = os.getenv('GOOGLE_SHEET_CREDENTIAL_PATH')

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(google_sheet_credential_path, scope)

    return gspread.authorize(credentials)


def get_target_google_sheet_url():
    return os.getenv('TARGET_GOOGLE_SHEET_URL')


def get_target_google_sheet_name():
    return os.getenv('TARGET_GOOGLE_SHEET_NAME')


def generate_error_list(error_occurred_while_sending_to_users_dict):
    date_today = TimeManager.get_current_date()
    time_today = TimeManager.get_current_time()

    blocked_users_template = LoggerManager.gen_blocked_users_template(error_occurred_while_sending_to_users_dict,
                                                                      date_today,
                                                                      time_today)

    with open(_blocked_user_file_path, "a") as file:
        file.write(blocked_users_template)


def gen_voucher_path(voucher_path):
    root_dir = os.path.dirname(os.path.abspath(__name__))
    full_voucher_path = os.path.join(root_dir, voucher_path)
    absolute_voucher_path = os.path.abspath(full_voucher_path)

    return absolute_voucher_path
