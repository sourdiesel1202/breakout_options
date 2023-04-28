print(__name__)
#from flask import current_app as app
from flask import render_template
#from flask import request
from flask import Blueprint
#from application.app import framework
from application.app import database
from application.app import toolbox
from application.app import strategies

page = 'breakout_mod'
page_name = 'Breakout (Longer Term)'
page_url = f'/strategy/{page}'
# bp_{page}
bp_breakout_mod = Blueprint(
    f'bp_{page}',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path=f'/{page}/static',
)

#@bp_{page}
#def {page}():
@bp_breakout_mod.route(f'/strategy/loading_{page}')
def loading_breakout_mod():
    return render_template(
        f'loading_{page}.html',
        strategy_name=page_name,
        strategy_url=page_url,
    )

#@bp_{page}
#def {page}():
@bp_breakout_mod.route(f'/strategy/{page}')
def breakout_mod():
    db = database.Database()
    db.load_data()
    picks = toolbox.find_todays_breakout(
        db.df.copy(),
        strategies.get_breakout_mod,
        days=3,
    )
    return render_template(
        f'{page}.html',
        db=db,
        picks=picks,
        strategy_name=page_name,
    )