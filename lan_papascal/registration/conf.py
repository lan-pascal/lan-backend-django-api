from enum import Enum

from easysettings.app import AppSettings


class AuthMethod(Enum):
    USERNAME = 1
    EMAIL = 2
    USERNAME_EMAIL = 3

class Settings(AppSettings):
    #This setting is important to raise a properly error on serializer validation
    AUTH_BACKEND_METHOD = AuthMethod.USERNAME_EMAIL

settings = Settings()