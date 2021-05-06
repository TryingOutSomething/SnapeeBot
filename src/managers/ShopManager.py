from src.managers import DatabaseManager as db_manager, LoggerManager


def get_shop_by_code_entered(code_entered):
    query_statement = '''
                        select code 

                        from snapshop_property.shops

                        where code = %s
                      '''

    value = (code_entered,)

    try:
        return db_manager.query_database_with_conditions(query_statement, value)

    except Exception as e:
        LoggerManager.exception_logs(e)
