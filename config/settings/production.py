from .core import *

DEBUG = config('DEBUG', cast=bool)
SECRET_KEY = config('SECRET_KEY')