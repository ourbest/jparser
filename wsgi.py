import serv


def create_app():
    # 这个工厂方法可以从你的原有的 `__init__.py` 或者其它地方引入。
    app = serv.app
    return app


application = create_app()

if __name__ == '__main__':
    application.run()
