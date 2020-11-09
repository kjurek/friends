from .config.settings import SENTRY_URL, SENTRY_TRACES_SAMPLE_RATE


def setup_sentry(app):
    if SENTRY_URL is None:
        return app

    import sentry_sdk
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
    sentry_sdk.init(SENTRY_URL, traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE)
    return SentryAsgiMiddleware(app)
