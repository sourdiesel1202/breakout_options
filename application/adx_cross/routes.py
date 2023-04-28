print(__name__)
#from flask import current_app as app
from flask import render_template
#from flask import request
from flask import Blueprint
#from application.app import framework
from application.app import database
from application.app import toolbox
from application.app import strategies

page = 'adx_cross'
page_name = 'ADX Cross'
page_url = f'/strategy/{page}'
# bp_{page}
bp_adx_cross = Blueprint(
    f'bp_{page}',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path=f'/{page}/static',
)

#@bp_{page}
#def {page}():
@bp_adx_cross.route(f'/strategy/loading_{page}')
def loading_adx_cross():
    return render_template(
        f'loading_{page}.html',
        strategy_name=page_name,
        strategy_url=page_url,
    )

#@bp_{page}
#def {page}():
@bp_adx_cross.route(f'/strategy/{page}')
def adx_cross():
    db = database.Database()
    db.load_data()
    picks = toolbox.find_todays_breakout(
        db.df.copy(),
        strategies.get_adx_cross,
        days=1,
    )
    return render_template(
        f'{page}.html',
        db=db,
        picks=picks,
        strategy_name=page_name,
    )