INSTALLED_APPS = [
    *'polls',*
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

from setuptools import setup, find_packages

setup(name='projet',
      version='1.0',
      packages=find_packages())
