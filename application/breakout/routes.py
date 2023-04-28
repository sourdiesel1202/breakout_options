print(__name__)
#from flask import current_app as app
from flask import render_template
#from flask import request
from flask import Blueprint
#from application.app import framework
from application.app import database
from application.app import toolbox
from application.app import strategies

page = 'breakout'
page_name = 'Breakout'
page_url = f'/strategy/{page}'
# bp_{page}
bp_breakout = Blueprint(
    f'bp_{page}',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path=f'/{page}/static',
)

#@bp_{page}
#def {page}():
@bp_breakout.route(f'/strategy/loading_{page}')
def loading_breakout():
    return render_template(
        f'loading_{page}.html',
        strategy_name=page_name,
        strategy_url=page_url,
    )

#@bp_{page}
#def {page}():
@bp_breakout.route(f'/strategy/{page}')
def breakout():
    db = database.Database()
    db.load_data()
    picks = toolbox.find_todays_breakout(
        db.df.copy(),
        strategies.get_breakout,
        days=1,
    )
    return render_template(
        f'{page}.html',
        db=db,
        picks=picks,
        strategy_name=page_name,
    )