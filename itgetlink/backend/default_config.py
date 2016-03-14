from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

CELERY_IMPORTS = (
    
)
CELERY_ACCEPT_CONTENT = ["json", "msgpack"]
CELERY_TASK_SERIALIZER = "json"
# CELERY_BROKER_URL = "redis://:@localhost:6379/0"
# CELERY_RESULT_BACKEND = "redis://:@localhost:6379/0"
CELERY_TASK_RESULT_EXPIRES = 1 * 60 * 60
CELERY_IGNORE_RESULT = True
CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
SEND_FILE_MAX_AGE_DEFAULT = 0

'''
KEEN_PROJECT_ID = "54360439709a395ba8f9b9ba"
KEEN_WRITE_KEY = "08f5135532e0ce51dbbf957f0e0a0e8d763c2976a582ce6767d154c109207b7b8269a278b659b8179d9a3262920431a3afeb5395f05acff9d394d144a7c1568d85094c996b0db0022d447691b1ccbf032c6b0252920f9dac7964dafd5ac302bb0401688c122874232d52c53f7df128bf"
KEEN_READ_KEY = "a451a60ce19ff593c7429a79f7f203debf19853029cd4b266c2b056f4c0c25ea3a6339429dd1ced2a90ef0d64ca754e8b4d14eaaa67bfc4f11abe25e14a2fc34c226fc738476fb37cfc280482c222fb574efd138a964f5b68acbba202b0f830e0542989d30eecc667b92a2ca78f2e10f"
'''
SQLALCHEMY_DATABASE_URI = "postgres://dev:postgres@localhost:5432/procurement"
SQLALCHEMY_NATIVE_UNICODE = True
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_POOL_TIMEOUT = 10
SQLALCHEMY_MAX_OVERFLOW = 10

FORWARD_MO_TZ = "Asia/Jakarta"

FORWARD_MO_URL = "https://manage.8villages.com/messages/inboundmessage"

SPECIAL_KEYWORD_CHOICES = ("ikuti",)
VIP_CHOICES = ("payau", "bayer", "bidan", "brilian", "rpp", "lisa",)

PROFILE_API_URL = "http://127.0.0.1"
CONVERSATION_API_URL = "http://127.0.0.1"

MO_ALLOWED_ADDRS = (
    "127.0.0.1",
    "202.53.250.218",   # Andalabs and Kisel
    "112.215.81.34",    # XL
    "202.155.150.40",   # IklanStore
    "180.222.216.228",  # new XL
    "114.4.68.143",     # new indosat
)

DN_ALLOWED_ADDRS = (
    "127.0.0.1",
    "202.53.250.218",   # Andalabs and Kisel
    "112.215.81.34",    # XL
    "202.155.150.40",   # IklanStore
)

MT_ALLOWED_ADDRS = (
    "127.0.0.1",
    "103.5.51.138",     # backward-compat for client.8villages.com
    "103.5.51.140",     # backward-compat for client.8villages.com
    "10.20.10.8",       # manage.8villages.com
    "10.20.10.6",       # message.8villages.com
)

KISEL_USERNAME = ""
KISEL_PASSWORD = ""
KISEL_PUSH_USERNAME = ""
KISEL_PUSH_PASSWORD = ""
KISEL_MT_URL = ("http://202.53.250.218:29005/sms_gateway"
                "/engine/mt_receiver/mt_spooler.php")
KISEL_MT_PUSH_URL = ("http://222.124.13.76/ussd/hitme.php")

ANDALABS_USERNAME = ""
ANDALABS_PASSWORD = ""
ANDALABS_MT_URL = ("http://202.53.250.218:29005/sms_gateway"
                   "/engine/mt_receiver/mt_spooler.php")
ANDALABS_MT_PUSH_URL = ("http://202.53.250.219:29016/sms_gateway"
                        "/engine/bulk_receiver_api/bulk_mt_receiver.php")

IKLANSTORE_USERNAME = ""
IKLANSTORE_PASSWORD = ""
IKLANSTORE_BASE_URL = "http://api.iklanstore.net:9900"

# indosat
ISAT_MSISDN_PREFIX = (
    '62816', '62815', '62858', '62856', '62857', '62814', '62855',
)

# XL
XL_MSISDN_PREFIX = (
    '62817', '62819', '62818', '62859', '62877', '62878', '62879',
)

# telkomsel
TSEL_MSISDN_PREFIX = (
    '62811', '62812', '62813', '62821', '62822', '62852', '62853', '62823',
    'SHDC-',
)

# SENTRY_DSN = "udp://10ac92926acf4ea3bef836e198b99ae4:f11516d4381e403581d5457ad0d11318@10.20.10.11:9001/3"

SANDBOX_SUFFIX = "_sb"
SANDBOX_MT_URL = "http://127.0.0.1/message/mt"

XL_MT_URL = "https://112.215.81.34:443/webpush/push.jsp"
XL_MT_APP_ID = ""
XL_MT_APP_PWD = ""
XL_MT_SHORTNAME = ""
XL_MT_PUSH_URL = "https://112.215.81.34:443/webpush/push.jsp"
XL_MT_PUSH_APP_ID = ""
XL_MT_PUSH_APP_PWD = ""
XL_MT_PUSH_SHORTNAME = ""

DEBUG=True
