class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'rootuser'
    MYSQL_DB = 'inventory_management'
    MYSQL_CURSORCLASS = 'DictCursor'
    PERMANENT_SESSION_LIFETIME = 30 * 60  # 30 minutes