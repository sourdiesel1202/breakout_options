print(__name__)
from application.app import init_app

app = init_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
elif __name__ != '__main__':
    import logging
    from logging.config import fileConfig
    fileConfig('log.conf')