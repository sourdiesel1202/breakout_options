print(__name__)
from flask import Flask

#from application.frameworks import *
from application.frameworks import strategies
from application.frameworks import database
from application.frameworks import toolbox
#db = database.Database()

def init_app():
    app = Flask(__name__, instance_relative_config=False)
    #app.config.from_object('config.ProdConfig')
    
    with app.app_context():
        from .home import routes as home
        from .api import routes as api
        from .strategy import routes as strategy
        
        app.register_blueprint(home.bp_home)
        app.register_blueprint(api.bp_api)
        app.register_blueprint(strategy.bp_strategy)
        
    return app