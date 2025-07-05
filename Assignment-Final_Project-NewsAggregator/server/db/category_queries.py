# SQL queries for CategoryRepository

ADD_CATEGORY = "INSERT INTO categories (name) VALUES (%s) ON CONFLICT DO NOTHING"
GET_ALL_CATEGORIES = "SELECT name FROM categories"
GET_ALL_CATEGORIES_WITH_STATUS = '''
    SELECT DISTINCT c.name,
        (CASE WHEN c.is_enabled_by_admin IS TRUE THEN 'Enabled'
            ELSE 'Disabled'
            END) AS status
    FROM categories c
    LEFT JOIN user_categories uc ON uc.category_id = c.category_id
    ORDER BY c.name
'''
ADD_IF_NOT_EXISTS = '''
    INSERT INTO categories (name)
    VALUES (%s)
    ON CONFLICT DO NOTHING
'''
GET_USER = "SELECT * FROM users WHERE user_id = %s"
GET_CATEGORY_ID = "SELECT category_id FROM categories WHERE name = %s"
SUBSCRIBE_USER_TO_CATEGORY = '''
    INSERT INTO user_categories (user_id, category_id)
    VALUES (%s, %s)
    ON CONFLICT DO NOTHING
'''
GET_ADMIN_DISABLED_CATEGORIES = "SELECT name FROM categories WHERE is_enabled_by_admin IS FALSE"
TOGGLE_USER_CATEGORY = '''
    UPDATE user_categories
    SET is_enabled = NOT is_enabled
    WHERE user_id = %s
    AND category_id = (SELECT category_id FROM categories WHERE name = %s)
'''
GET_USER_CATEGORIES_BY_ID = '''
    SELECT c.name, uc.is_enabled FROM user_categories uc
    JOIN categories c ON uc.category_id = c.category_id
    WHERE uc.user_id = %s AND uc.is_enabled = TRUE
'''
GET_CATEGORY_ID_BY_NAME = "SELECT category_id FROM categories WHERE name = %s"
DISABLE_CATEGORY = '''
    UPDATE categories
    SET is_enabled_by_admin = NOT is_enabled_by_admin
    WHERE category_id = %s
'''
DISABLE_USER_CATEGORY = '''
    UPDATE user_categories
    SET is_enabled = NOT is_enabled
    WHERE category_id = %s
'''
