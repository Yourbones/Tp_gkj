# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from multiprocessing import Process, Queue
#multiprocessing是Python的标准模块
#Process模块用来创建子进程，是核心模块
#Queue模块用来控制进程安全


"""
Django settings for Tp_gkj project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '30&878#xmg2*(bd-1-5z7xal3^v5&s(9ykl!6%a2&osw%t5m^6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

MACHINE_CODE = 'HZA3'  #每台工控机的唯一设备号   PS：#TODO: 设备号要更改

SEND_STATE_URL = 'http://192.168.8.102:12345/notify/ter/state' #TODO:URL为测试服地址

STOP_WASHING_TYPE = 2 # 1、STOP后可以有复位及重新开始等后续操作 2、STOP 即结束订单，不提供复位重新启动（只保留停止按键）

PLC_TYPE = 'DELTA'  # 'SIEMENS'

# PLC 程序关键参数
PLC_KWARGS = {
    'DELTA': {
        'RECEIVE_DATA_SLEEP_TIME': 0.05,
        'MACHINE': {'send_data': [0x01, 0x02, 0x08, 0x5a, 0x00, 0x08, 0x5b, 0xbf], 'receive_data_count': 6,
                    'read_timeout': 3},
        'ACTION': {'send_data': [0x01, 0x02, 0x08, 0xa0, 0x00, 0x18, 0x7a, 0x42], 'receive_data_count': 8,
                   'read_timeout': 1},
        'MALFUNCTION': {'send_data': [0x01, 0x02, 0x08, 0x78, 0x00, 0x18, 0xFA, 0x79], 'receive_data_count': 8,
                        'read_timeout': 1},
    },
    'SIEMENS': {
        'RECEIVE_DATA_SLEEP_TIME': 0.2,
        'MACHINE': {'send_data': [0x08, 0x03, 0x00, 0x10, 0x00, 0x0A, 0xC4, 0x91], 'receive_data_count': 25,
                    'read_timeout': 5},
        'ACTION': {'send_data': [0x08, 0x03, 0x00, 0x10, 0x00, 0x0A, 0xC4, 0x91], 'receive_data_count': 25,
                   'read_timeout': 2},
        'MALFUNCTION': {'send_data': [0x08, 0x03, 0x00, 0x10, 0x00, 0x0A, 0xC4, 0x91], 'receive_data_count': 25,
                        'read_timeout': 2}
    }
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',                    # django提供的rest框架
    'rest_framework.authtoken',          # 不明白为什么添加到应用列表，而不是随时调用
    'rest_framework_swagger',            # 使得API接口可视化
    'apps.wash_machine',
    'common'
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware'
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'common.middleware.SignMiddleware'             # 验签中间件
]

ROOT_URLCONF = 'Tp_gkj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Tp_gkj.wsgi.application'

# 设置缓存
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmen.LocMemCache',              # 选择缓存模式为本地内存缓存
        'LOCATION': 'unique-snowflake',                                          # 注明本地缓存的存储位置，只有一个内存缓存时可以忽略
        'TIMEOUT': None,                                                         # 表示超时时间，单位时秒。超过指定时间缓存就会整体刷新清空掉。
    }
}

# 密码验证
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-HANS'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

#静态资源的配置
STATIC_URL = '/manage/static/'                                           #？此处manage不知在哪，static也没有对应文件夹
STATIC_ROOT = os.path.join(BASE_DIR, "static/").replace('\\', '/')       # os.path.jon()返回的路径间隔符都是'\\',需要更改为'/'


STATIC_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',               #? 这里具体配置没懂
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/").replace('\\', '/')


QAUTH2_PROVIDER = {
    #this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}     # 表示申请的权限范围
}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': BASE_DIR + '/Tp_gkj/my_dev.cnf',
        },
        'ATOMIC_REQUESTS': True,                                       #这里不懂,先放着
    }
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT _PERMISSION_CLASSES':(
        #’rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',               # 非登录用户只读
        #'rest_framework.permissions.DjangoObjectPermissions',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': '1.0',
    'ALLOWED_VERSIONS': None,
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',
                                'rest_framework.filters.OrderingFilter',
                                'rest_framework.filters.SearchFilter',),
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'rest_framework.authentication.TokenAuthentication',
        # 'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    'NON_FIELD_ERRORS_KEY': 'errors',
    #datetime数据输出格式
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',

    #   请求频率设置
    'DEFAULT_THROTTLE_CLASSES':(
        'rest_framework.throttling.ScopedRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',

        #'helper.throttling.ChargeRateThrottle',
    ),
    'DEFAULT-THROTTLE-RATES':{
        'anon': '300/minute',
        'user': '600/minute',
        'charge': '20/minute',
        'feedback': '10/minute',
        'group_check': '6/minute',
    }
}


LOGGING_PREFIX = 'prod'                  # 日志文件的前缀

#日志配置
LOGGING = {
    'version': 1,                        # 日志版本
    'disable_existing_loggers': True,    # disable原有日志相关配置
    'formatters': {                      # 日志格式
        'standard': {                    # 标准格式
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {                         #日志过滤器
    },
    'handlers': {                        # 日志处理器
        'default': {                     # 默认处理器
            'level': 'DEBUG',            # 日志级别 (DEBUG < INFO < WARN < ERROR < FATAL)
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志输出文件
            'filename': os.path.join(BASE_DIR + '/logs/',
                                     LOGGING_PREFIX + '_washing.log'),
            #'maxBytes': 1024 * 1024 *1,   # 文件大小
            'backupCount': 100,            # 备份份数
            'formatter': 'standard',       # 使用哪种formatters日志格式
        },
        'error': {                         # 错误处理器
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR + '/logs/',
                                     LOGGING_PREFIX + '_error.log'),
            #'maxBytes': 1024 * 1024 *1,
            'backupCount': 100,
            'formatter': 'standard',
        },
        'console': {                       # 控制器handler，DEBUG级别以上的日志都要standard格式输出到控制台
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard'
        },
        'request_handler': {               # 请求处理器
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR + '/logs/',
                                     LOGGING_PREFIX + '_request.log'),
            #'maxBytes': 1024 * 1024 *1,
            'backupCount': 100,
            'formatter': 'standard',
        },
        'scripts_handler': {                # 脚本处理器
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR + '/logs/',
                                     LOGGING_PREFIX + '_script.log'),
            #'maxBytes': 1024 * 1024 * 1,
            'backupCount': 100,
            'formatter': 'standard',
        },
        'task_handler': {                   # 任务处理器
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR + '/logs/',
                                     LOGGING_PREFIX + '_task.log'),
            #'maxBytes': 1024 * 1024 * 1,
            'backupCount': 100,
            'formatter': 'standard',
        },
    },
    'loggers': {                                     # 日志记录器
        'django': {
            'handlers': ['scripts_handler', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'scripts': {
            'handlers': ['scripts_handler', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'apps': {
            'handlers': ['task_handler', 'console'],
            'level': 'DEBUG',      # 正式环境修改为INFO
            'propagate': False,
        },
        'task': {
            'handlers': ['task_handler', 'console'],
            'level': 'DEBUG',     # 正式环境修改为INFO
            'propagate':False,
        },
    }
}