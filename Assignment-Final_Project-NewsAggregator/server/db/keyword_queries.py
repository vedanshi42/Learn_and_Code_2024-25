# SQL queries for KeywordRepository

ADD_KEYWORD_FOR_USER = '''
    INSERT INTO keywords (user_id, keyword, is_enabled)
    VALUES (%s, %s, TRUE) ON CONFLICT DO NOTHING
'''

GET_ADMIN_DISABLED_KEYWORDS = "SELECT keyword FROM keywords WHERE is_enabled_by_admin IS FALSE"
TOGGLE_KEYWORD = '''
    UPDATE keywords
    SET is_enabled = NOT is_enabled
    WHERE user_id = %s
    AND keyword = %s
'''

GET_KEYWORDS_FOR_USER = '''
    SELECT keyword, is_enabled FROM keywords
    WHERE user_id = %s AND is_enabled = TRUE
'''

GET_ALL_KEYWORDS_WITH_STATUS = '''
    SELECT keyword,
        (CASE WHEN is_enabled_by_admin IS TRUE THEN 'Enabled'
            ELSE 'Disabled'
            END) AS status
    FROM keywords
    ORDER BY keyword
'''

DISABLE_KEYWORD_GLOBALLY = '''
    UPDATE keywords
    SET is_enabled_by_admin = NOT is_enabled_by_admin
    WHERE keyword = %s
'''

DISABLE_KEYWORD_FOR_ALL_USERS = '''
    UPDATE keywords
    SET is_enabled = NOT is_enabled
    WHERE keyword = %s
'''
