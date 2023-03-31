import os
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

class Config:
    '''flask config'''
    SECRET_KEY = 'secretkey' #session 암호화ㅏ
    SESSION_COOKIE_NAME = 'gogglekaap'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3307/gogglekaap?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_DOC_EXPANSION= 'list'
    USER_STATIC_BASE_DIR = 'user_imges'
    
class DevelopmentConfig(Config):
    '''flask config for dev'''
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = 1
    WTF_CSRF_ENABLED= False #개발환경에서는 csrf error 무시

class TestingConfig(DevelopmentConfig):
    __test__ = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_PATH, "sqlite_test.db")}'
    
class ProductionConfig(Config):
    pass
    