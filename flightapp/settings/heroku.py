import dj_database_url
from decouple import config

from .base import *

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}
