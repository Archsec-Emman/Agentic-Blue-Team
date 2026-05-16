import random
import string
from datetime import datetime, timezone, timedelta

now = datetime.now(timezone.utc)
past_5m = now - timedelta(minutes=5)
past_10m = now - timedelta(minutes=10)
past_15m = now - timedelta(minutes=15)
past_30m = now - timedelta(minutes=30)
past_1h = now - timedelta(hours=1)
past_2h = now - timedelta(hours=2)
past_3h = now - timedelta(hours=3)
past_6h = now - timedelta(hours=6)
past_12h = now - timedelta(hours=12)
past_24h = now - timedelta(hours=24)
past_2d = now - timedelta(days=2)
past_3d = now - timedelta(days=3)
past_4d = now - timedelta(days=4)
past_5d = now - timedelta(days=5)
past_6d = now - timedelta(days=6)
past_7d = now - timedelta(days=7)
past_1d_18h = now - timedelta(days=1, hours=18)
past_2d_6h = now - timedelta(days=2, hours=6)
past_3d_12h = now - timedelta(days=3, hours=12)
past_4d_20h = now - timedelta(days=4, hours=20)
past_5d_8h = now - timedelta(days=5, hours=8)
past_6d_15h = now - timedelta(days=6, hours=15)


def gen_hash(length=64):
    return ''.join(random.choices(string.hexdigits[:16], k=length))


def gen_uuid():
    return f"{gen_hash(8)}-{gen_hash(4)}-{gen_hash(4)}-{gen_hash(4)}-{gen_hash(12)}"


def gen_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
