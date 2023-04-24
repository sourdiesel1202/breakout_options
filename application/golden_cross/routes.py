print(__name__)
#from flask import current_app as app
from flask import render_template
#from flask import request
from flask import Blueprint
#from application.app import framework
from application.app import db
from application.app import toolbox
from application.app import strategies

page = 'golden_cross'
# bp_{page}
bp_golden_cross = Blueprint(
    f'bp_{page}',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path=f'/{page}/static',
)

#@bp_{page}
#def {page}():
@bp_golden_cross.route(f'/strategy/{page}')
def golden_cross():
    picks = toolbox.find_todays_breakout(
        db.df.copy(),
        strategies.get_golden_cross,
        days=1,
    )
    return render_template(
        f'{page}.html',
        db=db,
        picks=picks,
    )