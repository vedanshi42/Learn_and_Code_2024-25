# SQL queries for ExternalAPIRepository

UPDATE_STATUS = '''
    UPDATE external_api_servers
    SET status = %s, last_accessed = %s
    WHERE api_name = %s
'''

GET_LAST_ACCESSED = "SELECT last_accessed FROM external_api_servers WHERE api_name = %s"
GET_ALL_STATUSES = "SELECT api_name, status, last_accessed FROM external_api_servers"
GET_ALL_KEYS = "SELECT api_name, api_key, last_accessed FROM external_api_servers"
UPDATE_API_KEY = "UPDATE external_api_servers SET api_key = %s WHERE api_name = %s"
GET_API_KEYS = "SELECT api_name, api_key FROM external_api_servers"
