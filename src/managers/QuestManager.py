from src.managers import DatabaseManager as db_manager, LoggerManager


def get_list_of_available_quest_titles_for_the_week(date_today):
    query_statement = '''
                        select quest_title 

                        from snapshop_quest.quests 

                        where %s >= start_date and 
                            %s <= end_date
                    '''

    value = (date_today, date_today,)

    try:
        return db_manager.query_database_with_conditions(query_statement, value)

    except Exception as e:
        LoggerManager.exception_logs(e)


def get_list_of_available_quests_for_the_week(quest_title):
    query_statement = '''
                        select quest_description
                        
                        from snapshop_quest.quests 
                        
                        where quest_title = %s
                    '''

    value = (quest_title,)

    try:
        return db_manager.query_database_with_conditions(query_statement, value)

    except Exception as e:
        LoggerManager.exception_logs(e)
