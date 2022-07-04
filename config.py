from starlette.config import Config


config = Config('.env')
DATABASE_URL = config('DATABASE_URL', cast=str, default='')
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = 'HS256'
SECRET_KEY = config('SECRET_KEY', cast=str, default='ab9be59a91808afb')