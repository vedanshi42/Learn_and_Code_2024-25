# SQL queries for UserRepository

GET_USER_BY_EMAIL = "SELECT * FROM users WHERE email = %s"
CREATE_USER = '''
    INSERT INTO users (username, email, password, role)
    VALUES (%s, %s, %s, %s) RETURNING user_id
'''
GET_USER_BY_EMAIL_AFTER_CREATE = "SELECT * FROM users WHERE email = %s"
EMAIL_EXISTS = "SELECT 1 FROM users WHERE email = %s"
GET_ALL_USERS = "SELECT * FROM users WHERE role != 'admin'"
