from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
API_TOKEN = env.str('API_TOKEN')
MAX_HOTELS = 100
MAX_PHOTOS = 10
LOADING_ANIMATION = True
NOTIFY_ADMINS = False