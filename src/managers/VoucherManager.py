from src.managers import DatabaseManager as db_manager, LoggerManager


def get_all_allocated_new_user_vouchers():
    query_statement = '''
                        select title, 
                               teleimageurl, 
                               couponid, 
                               businesshours, 
                               location, 
                               website, 
                               dailycoupon_table.id, 
                               phone

                        from snapshop_property.coupons coupon_table

                        inner join snapshop_property.dailycoupons dailycoupon_table
                            on coupon_table.id = dailycoupon_table.couponid
                        inner join snapshop_property.shops shop_table
                            on coupon_table.shopid = shop_table.id
                        
                        where dailycoupon_table.issueamount != dailycoupon_table.totalamount
                            and dailycoupon_table.action = 'new_user' 
                            and coupon_table.id >= 13
                            and isdeleted = 0
                      '''

    try:
        return db_manager.query_database_no_conditions(query_statement)

    except Exception as e:
        LoggerManager.exception_logs(e)


def get_weekly_allocated_voucher(voucher_id):
    query_statement = '''
                        select title, 
                               teleimageurl, 
                               couponid, 
                               businesshours, 
                               location, 
                               website, 
                               dailycoupon_table.id, 
                               phone
                        
                        from snapshop_property.coupons coupon_table

                        inner join snapshop_property.dailycoupons dailycoupon_table 
                            on coupon_table.id = dailycoupon_table.couponid
                        inner join snapshop_property.shops shop_table 
                            on coupon_table.shopid = shop_table.id
                        
                        where dailycoupon_table.issueamount != dailycoupon_table.totalamount
                            and dailycoupon_table.id = %s
                            and action = 'weekly_login'
                            and isdeleted = 0
                      '''
    value = (voucher_id,)

    try:
        return db_manager.query_database_with_conditions(query_statement, value)

    except Exception as e:
        LoggerManager.exception_logs(e)


def update_voucher_details(voucher_id, table, field):
    update_statement = f'''
                        update snapshop_property.{table}
                        set {field} = {field} + 1
                        where id = %s
                       '''

    value = (voucher_id,)

    try:
        return db_manager.update_database_table(update_statement, value)

    except Exception as e:
        LoggerManager.exception_logs(e)


def get_all_promo_code_vouchers(code_entered_by_user, date_today):
    query_statement = '''
                        select promo_code_table.id, 
                               coupon_table.id as coupon_id,
                               title, 
                               teleimageurl, 
                               businesshours, 
                               location, 
                               website, 
                               phone,
                               expireto

                        from snapshop_property.coupons coupon_table

                        inner join snapshop_property.shops shop_table 
                            on coupon_table.shopid = shop_table.id
                        inner join snapshop_property.promocoupon promo_coupon_table 
                            on promo_coupon_table.coupon_id = coupon_table.id
                        inner join snapshop_property.promocode promo_code_table 
                            on promo_code_table.id = promo_coupon_table.promo_code_id

                        where promo_code_table.code = %s
                            and promo_code_table.claimed_amount < promo_code_table.amount_claimable
                            and promo_code_table.end_date >= %s
                      '''

    values = (code_entered_by_user, date_today,)

    try:
        return db_manager.query_database_with_conditions(query_statement,
                                                         values)

    except Exception as e:
        LoggerManager.exception_logs(e)
