import os

TRANSLATE_URL = 'https://translate.api.cloud.yandex.net/translate/v2/translate'
ASYNC_API_URL = os.getenv('ASYNC_API_URL')
SENTRY_URL = os.getenv('SENTRY_URL')
FOLDER_ID = os.getenv('FOLDER_ID')
TRANSLATE_API_KEY = os.getenv('TRANSLATE_API_KEY')
STATE_RESPONSE_KEY = 'session_state'
STATE_REQUEST_KEY = 'session'
