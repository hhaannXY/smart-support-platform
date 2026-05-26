import os

def init_sentry():
    dsn = os.environ.get('SENTRY_DSN')
    if not dsn:
        return
    try:
        import sentry_sdk
        sentry_sdk.init(dsn)
    except Exception:
        pass
