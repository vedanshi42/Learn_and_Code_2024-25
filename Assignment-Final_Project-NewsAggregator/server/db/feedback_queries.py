# SQL queries for FeedbackService/Repository

SELECT_FEEDBACK_TYPE = '''
    SELECT feedback_type FROM user_article_feedback
    WHERE user_id = %s AND article_id = %s
'''

UPDATE_USER_FEEDBACK = '''
    UPDATE user_article_feedback
    SET feedback_type = %s
    WHERE user_id = %s AND article_id = %s
'''

INSERT_USER_FEEDBACK = '''
    INSERT INTO user_article_feedback (user_id, article_id, feedback_type)
    VALUES (%s, %s, %s)
'''

INSERT_OR_UPDATE_FEEDBACK = '''
    INSERT INTO feedback (article_id, {column})
    VALUES (%s, %s)
    ON CONFLICT (article_id) DO UPDATE
    SET {column} = feedback.{column} + %s
'''
