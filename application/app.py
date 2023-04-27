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
        from .golden_cross import routes as golden_cross
        from .adx_cross import routes as adx_cross
        from .breakout import routes as breakout
        from .breakout_mod import routes as breakout_mod
        from .api import routes as api
        
        app.register_blueprint(home.bp_home)
        app.register_blueprint(golden_cross.bp_golden_cross)
        app.register_blueprint(adx_cross.bp_adx_cross)
        app.register_blueprint(breakout.bp_breakout)
        app.register_blueprint(breakout_mod.bp_breakout_mod)
        app.register_blueprint(api.bp_api)
        
    return app