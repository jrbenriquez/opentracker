from .core import *
from decouple import config

DEBUG = config('DEBUG', cast=bool)
SECRET_KEY = config('SECRET_KEY')