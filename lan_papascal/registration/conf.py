from enum import Flag,auto

from easysettings.app import AppSettings


class AuthMethod(Flag):
    USERNAME = auto()
    EMAIL = auto()
    USERNAME_EMAIL = USERNAME & EMAIL
    
class Settings(AppSettings):
    #This setting is important to raise a properly error on serializer validation
    AUTH_BACKEND_METHOD = AuthMethod.USERNAME_EMAIL

settings = Settings()