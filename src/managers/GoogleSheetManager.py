from src.managers import IOassetsManager


def _connect_to_target_users_google_sheet():
    google_sheet_client = IOassetsManager.authorize_google_sheet_access()
    target_google_sheet_url = IOassetsManager.get_target_google_sheet_url()
    target_google_sheet_name = IOassetsManager.get_target_google_sheet_name()

    spreadsheet_to_be_used = google_sheet_client.open_by_url(target_google_sheet_url)

    return spreadsheet_to_be_used.worksheet(target_google_sheet_name)


def get_user_telegram_id_from_google_sheet():
    target_user_sheet = _connect_to_target_users_google_sheet()

    target_users_list = target_user_sheet.col_values(1)[1:]

    return target_users_list
