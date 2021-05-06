from telegram import ReplyKeyboardMarkup

start_keyboard = ReplyKeyboardMarkup(
    [['/wallet', '/exchange', '/promocode', '/quests']], one_time_keyboard=True)

claim_keyboard = ReplyKeyboardMarkup([['claim']], one_time_keyboard=True)

claim_type_keyboard = ReplyKeyboardMarkup(
    [['Promo', 'Wallet']], one_time_keyboard=True)

exchange_keyboard = ReplyKeyboardMarkup(
    [['/exchange']], one_time_keyboard=True)

confirm_keyboard = ReplyKeyboardMarkup(
    [['Yes!', 'No!']], one_time_keyboard=True)

message_type_keyboard = ReplyKeyboardMarkup(
    [['Text', 'Photo']], one_time_keyboard=True)

referral_prompt_keyboard = ReplyKeyboardMarkup(
    [['Enter now!', 'Skip']], one_time_keyboard=True)

referral_skip_keyboard = ReplyKeyboardMarkup(
    [['Yes', 'Back']], one_time_keyboard=True)

register_keyboard = ReplyKeyboardMarkup(
    [['/letsgo']], one_time_keyboard=True)

gender_keyboard = ReplyKeyboardMarkup(
    [['Female', 'Male']], one_time_keyboard=True)
