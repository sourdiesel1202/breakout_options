print(__name__)
#from flask import current_app as app
from flask import render_template
#from flask import request
from flask import Blueprint
#from application.app import framework
from application.app import db
from application.app import toolbox
from application.app import strategies

page = 'breakout'
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
@bp_breakout.route(f'/strategy/{page}')
def breakout():
<<<<<<< HEAD
    picks = toolbox.find_todays_breakout(
        db.df.copy(),
        strategies.get_breakout,
        days=1,
    )
=======
    picks = toolbox.find_breakout(strategies.get_breakout, db.df)
>>>>>>> 34fb129045927e8ba565f3feccdacd3b0fd9d588
    return render_template(
        f'{page}.html',
        db=db,
        picks=picks,
    )