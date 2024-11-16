"""
Django settings for Overtoonz project.

Generated by 'django-admin startproject' using Django 5.0.7.
Documentation: https://docs.djangoproject.com/en/5.0/
"""

from pathlib import Path
import os

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = 'django-insecure-u6tcpui#(#mkkkr00u^evxzeq!0%olf#$+b7jy$=0j7=&a3vxj'  # Keep this secret!
DEBUG = False  # Ensure this is False in production
ALLOWED_HOSTS = ['overtoonz.onrender.com']

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend',
    'bootstrap5',
    'compressor',
    'django_mysql',
]

# Static files and Django Compressor
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Collected static files
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Project-level static files
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_ROOT = STATIC_ROOT  # Ensure compression happens within the static root
COMPRESS_ENABLED = True
COMPRESS_STORAGE = 'compressor.storage.CompressorFileStorage'
COMPRESS_OUTPUT_DIR = 'CACHE'

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL Configuration
ROOT_URLCONF = 'overtoonz.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Ensure templates directory exists
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'backend.context_processors.versioning',
                'backend.context_processors.user_details',
            ],
        },
    },
]

# WSGI Application
WSGI_APPLICATION = 'overtoonz.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'b6nkxtnj0xc6npzvhdel',
        'USER': 'usfqhv9skfkconeu',
        'PASSWORD': 'DdDh8usydIgZzGB6evC9',
        'HOST': 'b6nkxtnj0xc6npzvhdel-mysql.services.clever-cloud.com',
        'PORT': 3306,
    }
}

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Default Auto Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'backend.User'

# Sessions
SESSION_COOKIE_AGE = 604800  # One week
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
