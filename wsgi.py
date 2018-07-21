import serv
import cutt_sd


def create_app():
    # 这个工厂方法可以从你的原有的 `__init__.py` 或者其它地方引入。
    app = serv.app
    try:
        cutt_sd.register('/url/article', 8388)
    except:
        app.logger.warning("Error register service", exc_info=1)
    return app


application = create_app()

if __name__ == '__main__':
    application.run()
