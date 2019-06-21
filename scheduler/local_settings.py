DEBUG = False
API_KEY = '4NNhOzwHv42V9NDEWqxgtwK%2ByG8alZCPfxyVk%2FCM9M%2FoZN1z2kchtGdrZ0qI8rm6R8sEIQaVFjUJA0S%2FlBFBFw%3D%3D'
DATABASE_NAME = 'schedule_prod'
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'whgusdnr12'
DATABASE_HOST = 'playgillround.cwadawgcd2ch.ap-northeast-2.rds.amazonaws.com'
FCM_API_KEY = "AAAAW0k8NHw:APA91bEu3tbtpFWJ-To-Cd0Z4SVAMDKHDf8Bj68KkI_T295C0kH9uPmz3HZzC-JoyGL_yZsvgp6AWItn2JMS6t46urReIMFFQhKkUQqwMFl6FuZx97oueUyCHnsWmZ9MLpZLadjV-LPH"

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
