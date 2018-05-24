# 一般系统中，将数据库中的时间统一使用UTC时间，然后在展示之类处理时，转成当地时区
import pytz
from datetime import datetime

loc_tz = pytz.timezone('Asia/Shanghai')
utc_tz = pytz.timezone('UTC')

def now_dt(tzinfo=loc_tz):
    # datetime.now(tz)
    # tz.localize(datetime.now())
    # tz.localize(datetime.fromtimestamp(time.time()))
    # 这里先取当前utc时间，然后加上UTC时区，之后转成当前时区
    return datetime.utcnow().replace(tzinfo=utc_tz).astimezone(loc_tz)


def str_2_datetime_by_format(dt_str, dt_format='%Y-%m-%d %H:%M:%S'):
    return loc_tz.localize(datetime.strptime(dt_str, dt_format))


def datetime_2_str_by_format(dt, dt_format='%Y-%m-%d %H:%M:%S'):
    return dt.astimezone(loc_tz).strftime(dt_format)
