DEBUG = True
API_KEY = 'e545a89a-eeda-4769-aade-8afad754bece'
DATABASE_NAME = 'schedule_prod'
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'whgusdnr12'
DATABASE_HOST = 'playgillround.cwadawgcd2ch.ap-northeast-2.rds.amazonaws.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
