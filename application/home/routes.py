print(__name__)
#from flask import current_app as app
from flask import render_template
#from flask import request
from flask import Blueprint
#from application.app import framework
from application.app import database
from application.app import strategies

page = 'home'
# bp_{page}
bp_home = Blueprint(
    f'bp_{page}',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path=f'/{page}/static',
)

#@bp_{page}
#def {page}():
@bp_home.route('/home')
def home():
    db = database.Database()
    db.update_historic_data()
    return render_template(
        'page.html',
        db=db,
    )


#@bp_{page}
#def {page}():
@bp_home.route('/')
def initialize():
    db = database.Database()
    if db.file_exists:
        return render_template(
            'page.html',
            db=db,
            strategies=strategies.inventory,
        )
    else:
        return render_template(
            'initialize.html',
        )

