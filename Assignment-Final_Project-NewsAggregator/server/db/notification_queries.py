# SQL queries for NotificationRepository

DELETE_USER_NOTIFICATIONS = "DELETE FROM user_notifications WHERE user_id = %s"
INSERT_USER_NOTIFICATION = "INSERT INTO user_notifications (user_id, article_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
GET_USER = "SELECT * FROM users WHERE user_id = %s"
GET_USER_ENABLED_CATEGORIES = "SELECT category_id FROM user_categories WHERE user_id = %s AND is_enabled = TRUE"
GET_USER_ENABLED_KEYWORDS = "SELECT keyword FROM keywords WHERE user_id = %s AND is_enabled = TRUE"
GET_NOTIFICATIONS_BASE = '''
    SELECT DISTINCT a.article_id, a.title, a.source_url, a.date_published
    FROM articles a
    WHERE {conditions}
    ORDER BY a.date_published DESC
'''
