from datetime import datetime, timedelta, date

_VOUCHER_EXPIRY_DATE = 8
TIMEOUT_DURATION_IN_MINUTES = 3


def get_current_date():
    return date.today()


def get_current_date_in_d_m_y():
    date_today = get_current_date()

    return convert_date_to_d_m_y_format(date_today)


def get_current_time():
    return datetime.now().strftime("%H:%M:%S")


def get_current_day():
    return datetime.now().strftime('%A')


def convert_to_date_format(string_date):
    return datetime.strptime(string_date, '%Y-%m-%d').date()


def gen_expiry_date():
    expiry_date = datetime.now() + timedelta(weeks=_VOUCHER_EXPIRY_DATE)

    return expiry_date.strftime('%Y-%m-%d')


def gen_expiry_date_in_d_m_y():
    expiry_date_in_str_format = gen_expiry_date()

    expiry_date_in_date_format = convert_to_date_format(
        expiry_date_in_str_format)

    return convert_date_to_d_m_y_format(expiry_date_in_date_format)


def convert_date_to_d_m_y_format(date_in_date_format):
    return datetime.strftime(date_in_date_format, '%d/%m/%Y')
