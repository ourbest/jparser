from raven.contrib.flask import Sentry

sentry = None


def init_sentry(app):
    global sentry
    sentry = Sentry(app,
                    dsn='http://f0c276b7792144fb9efba0c000f979ce:6bc75bbb12764b16b2ff6d35d465b737@10.9.144.173:9000/14')
