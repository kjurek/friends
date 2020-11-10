import os

SENTRY_URL = os.environ.get("SENTRY_URL")
SENTRY_TRACES_SAMPLE_RATE = float(os.environ.get("SENTRY_SAMPLE_RATE", 1.0))
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
DB_URL = os.environ["DB_URL"]
