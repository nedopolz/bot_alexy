import os

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
DATABASE = os.getenv("DATABASE")
ip = os.getenv("ip")
aiogram_redis = {
    'host': ip,
}
redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}

# тут user_id админов бота
admins = [
    1501992580
]

# тут значения по дефолту
referral_reward = 10
site_reward = 20
tiktok_reward = 20
allowed_withdrawal_amount = 2000
