from hashids import Hashids

from src.managers import DatabaseManager as db_manager, LoggerManager


# /start and /letsgo dependent commands
def is_a_member(telegram_id):
    query_statement = '''select telegram_username 
                         
                         from snapshop_wallet.transfer 
                         
                         where telegram_id = %s;'''
    value = (telegram_id,)

    try:
        return db_manager.query_database_with_conditions(query_statement, value)

    except Exception as e:
        LoggerManager.exception_logs(e)


def is_valid_referral_code(message_from_user):
    query_statement = '''
                        select user_table.telegram_id, 
                               asset_value 
                        
                        from snapshop_wallet.transfer_assets user_asset_table

                        inner join snapshop_wallet.transfer user_table 
                            on user_table.telegram_id = user_asset_table.telegram_id
                        
                        where referralcode = binary %s and asset_type = 'coin'
                      '''

    value = (message_from_user,)

    try:
        return db_manager.query_database_with_conditions(query_statement, value)

    except Exception as e:
        LoggerManager.exception_logs(e)


def update_referrer_snapcoin_amt(referrer_id, updated_snapcoin_amt):
    update_statement = '''
                        update snapshop_wallet.transfer_assets

                        set asset_value = %s

                        where telegram_id = %s
                      '''

    value = (updated_snapcoin_amt, referrer_id,)

    try:
        return db_manager.update_database_table(update_statement, value)

    except Exception as e:
        LoggerManager.exception_logs(e)


def update_user_referal_history_table(referrer_id, referee_id):
    insert_statement = '''
                        insert into snapshop_auth.referralhistory(
                            referrer_telegram,
                            referee_telegram
                        )

                        values(
                            %s,
                            %s
                        )
                       '''

    values = (referrer_id, referee_id,)

    try:
        return db_manager.update_database_table(insert_statement,
                                                values)

    except Exception as e:
        LoggerManager.exception_logs(e)


def gen_referral_code():
    query_statement = '''select count(id) from snapshop_wallet.transfer'''

    try:
        total_number_of_users = db_manager.query_database_no_conditions(
            query_statement)

        hashids = Hashids(min_length=5)

        return hashids.encode(total_number_of_users[0][0] + 1)

    except Exception as e:
        LoggerManager.exception_logs(e)


def register_new_user(new_user_entry):
    insert_transfer_statement = '''
                                    insert into snapshop_wallet.transfer(
                                        telegram_id, telegram_username,
                                        email, gender, 
                                        referralcode
                                    )

                                    values(
                                        %s, %s,
                                        %s, %s, 
                                        %s
                                    );
                                '''
    insert_transfer_values = (
        new_user_entry['user_id'], new_user_entry['telegram_username'],
        new_user_entry['email'], new_user_entry['gender'],
        new_user_entry['referral_code']
    )

    insert_transfer_asset_statement = '''
                                        insert into snapshop_wallet.transfer_assets(
                                            telegram_id, asset_type, 
                                            asset_id, asset_value
                                        )

                                        values(
                                            %s, %s,
                                            %s, %s
                                        );
                                      '''
    insert_transfer_asset_values = (
        new_user_entry['user_id'], new_user_entry['asset_type'],
        new_user_entry['asset_id'], new_user_entry['asset_value'],
    )

    try:
        db_manager.update_database_table(insert_transfer_statement,
                                         insert_transfer_values)

        return db_manager.update_database_table(insert_transfer_asset_statement,
                                                insert_transfer_asset_values)

    except Exception as e:
        LoggerManager.exception_logs(e)


# /open related commands
def get_new_user_login_details(user_telegram_id):
    query_statement = '''
                        select newuserbonustracker, 
                               newuserlogindate
                        
                        from snapshop_wallet.transfer
                        
                        where snapshop_wallet.transfer.telegram_id = %s;
                      '''

    value = (user_telegram_id,)

    try:
        return db_manager.query_database_with_conditions(query_statement,
                                                         value)

    except Exception as e:
        LoggerManager.exception_logs(e)


def get_user_weekly_login_details(user_telegram_id):
    query_statement = '''
                        select date_claimed
                        
                        from snapshop_wallet.weeklyloginhistory 
                        
                        where telegram_id = %s
                            and yearweek(date_claimed, 7) = YEARWEEK(now(), 7)

                        order by date_claimed desc;
                      '''

    value = (user_telegram_id,)

    try:
        return db_manager.query_database_with_conditions(query_statement,
                                                         value)

    except Exception as e:
        LoggerManager.exception_logs(e)


def get_user_allocated_bonus(user_telegram_id):
    query_statement = '''
                       select bonustype
                        
                       from snapshop_wallet.transfer
                        
                       where telegram_id = %s;
                      '''

    value = (user_telegram_id,)

    try:
        return db_manager.query_database_with_conditions(query_statement,
                                                         value)

    except Exception as e:
        LoggerManager.exception_logs(e)


def update_user_snapcoin_amt(amount_to_update, arithmetic_operator, user_id):
    update_statement = f'''
                        update snapshop_wallet.transfer_assets

                        set asset_value = asset_value {arithmetic_operator} %s
                        
                        where telegram_id = %s and asset_type = 'coin'
                       '''
    values = (amount_to_update, user_id,)

    try:
        return db_manager.update_database_table(update_statement, values)

    except Exception as e:
        LoggerManager.exception_logs(e)


def add_user_voucher(user_voucher_info):
    insert_statement = '''
                        insert into snapshop_wallet.transfer_assets(
                            telegram_id, asset_type, 
                            asset_id, asset_value,
                            expiry_date
                        )

                        values(
                            %s, %s,
                            %s, %s,
                            %s
                        );
                       '''

    insert_value = (
        user_voucher_info['telegram_id'], user_voucher_info['asset_type'],
        user_voucher_info['asset_id'], user_voucher_info['asset_value'],
        user_voucher_info['expiry_date'],
    )

    try:
        return db_manager.update_database_table(insert_statement,
                                                insert_value)

    except Exception as e:
        LoggerManager.exception_logs(e)


def update_new_user_tracker(updated_no_of_days, date_today, user_id):
    LoggerManager.general_logs(f"Updating new user tracker for user {user_id}")

    update_statement = '''
                        update snapshop_wallet.transfer 

                        set newuserbonustracker = %s, 
                            newuserlogindate = %s

                        where telegram_id = %s
                       '''

    values = (updated_no_of_days, date_today, user_id,)

    try:
        return db_manager.update_database_table(update_statement,
                                                values)

    except Exception as e:
        LoggerManager.exception_logs(e)


def update_weekly_bonus_tracker(date_today, user_id):
    LoggerManager.general_logs(
        f"Updating weekly bonus tracker for user {user_id}")

    update_statement = '''
                        insert into snapshop_wallet.weeklyloginhistory(
                            telegram_id, date_claimed
                        )

                        values(%s, %s)
                       '''

    values = (user_id, date_today,)

    try:
        return db_manager.update_database_table(update_statement,
                                                values)

    except Exception as e:
        LoggerManager.exception_logs(e)


# /exchange related commands
def get_user_exchangeable_vouchers_and_snapcoin_amt(user_id):
    query_statement = '''
                        select asset_value, 
                               coupon_table.id, 
                               title, 
                               teleimageurl, 
                               businesshours, 
                               location, 
                               website, 
                               phone, 
                               exchange_table.id as exchange_coupon_id,
                               exchangefee

                        from snapshop_property.coupons coupon_table

                        inner join snapshop_property.shops shop_table 
                            on coupon_table.shopid = shop_table.id
                        inner join snapshop_property.exchangecoupons exchange_table 
                            on coupon_table.id = exchange_table.couponid
                        inner join snapshop_wallet.transfer_assets user_assets_table

                        where user_assets_table.asset_type = 'coin'
                            and user_assets_table.telegram_id = %s
                            and curdate() >= exchange_table.startdate
                            and curdate() <= exchange_table.enddate
                            and exchange_table.issueamount < exchange_table.totalamount
                      '''

    value = (user_id,)

    try:
        return db_manager.query_database_with_conditions(query_statement,
                                                         value)

    except Exception as e:
        LoggerManager.exception_logs(e)


def update_user_voucher_history(user_id, user_action, voucher_id_in_db):
    insert_statement = '''
                        insert into snapshop_wallet.usercouponhistory(
                            telegram_id, from_action, 
                            coupon_id
                        )

                        values(
                            %s, %s,
                            %s
                        );
                       '''

    insert_values = (
        user_id, user_action,
        voucher_id_in_db,
    )

    try:
        return db_manager.update_database_table(insert_statement,
                                                insert_values)

    except Exception as e:
        LoggerManager.exception_logs(e)


# /promocode related commands
def user_claimed_promo_code_before(code_entered_by_user, user_id):
    query_statement = '''
                        select *
                        
                        from snapshop_wallet.usercouponhistory

                        where telegram_id = %s and from_action = %s
                      '''

    values = (user_id, code_entered_by_user,)

    try:
        return db_manager.query_database_with_conditions(query_statement,
                                                         values)

    except Exception as e:
        LoggerManager.exception_logs(e)


# /wallet related commands
def get_all_vouchers_owned_by_user(user_id):
    query_statement = '''
                        select user_assets_table.id, 
                               coupon_table.id as coupon_id, 
                               title, 
                               teleimageurl, 
                               businesshours, 
                               location, 
                               website, 
                               phone,
                               expiry_date

                        from snapshop_property.coupons coupon_table

                        inner join snapshop_property.shops shop_table 
                            on coupon_table.shopid = shop_table.id
                        inner join snapshop_wallet.transfer_assets user_assets_table 
                            on user_assets_table.asset_id = coupon_table.id
                        inner join snapshop_wallet.transfer user_table 
                            on user_table.telegram_id = user_assets_table.telegram_id

                        where user_table.telegram_id = %s
                        
                        order by expiry_date
                      '''

    value = (user_id,)

    try:
        return db_manager.query_database_with_conditions(query_statement,
                                                         value)

    except Exception as e:
        LoggerManager.exception_logs(e)


def get_user_snap_coin_amount(user_id):
    query_statement = '''
                       select asset_value

                        from snapshop_wallet.transfer_assets

                        where telegram_id = %s
                            and asset_type = 'coin'
                      '''

    value = (user_id,)

    try:
        return db_manager.query_database_with_conditions(query_statement,
                                                         value)

    except Exception as e:
        LoggerManager.exception_logs(e)


def delete_voucher_from_user_wallet(user_asset_id):
    delete_statement = '''  
                        delete from snapshop_wallet.transfer_assets

                        where id = %s
                       '''

    value = (user_asset_id,)

    try:
        return db_manager.update_database_table(delete_statement,
                                                value)

    except Exception as e:
        LoggerManager.exception_logs(e)


# /referralcode related command
def get_user_referral_code(user_telegram_id):
    query_statement = '''
                        select referralcode 
                        
                        from snapshop_wallet.transfer 
                        
                        where telegram_id = %s
                      '''
    value = (user_telegram_id,)

    try:
        return db_manager.query_database_with_conditions(query_statement,
                                                         value)

    except Exception as e:
        LoggerManager.exception_logs(e)
