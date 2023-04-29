print(__name__)
#from flask import current_app as app
import os
import importlib
from flask import render_template
from flask import request
from flask import Blueprint
#from application.app import framework
from application.app import database
from application.app import toolbox
#from application.app import strategies

page = 'strategy'
page_name = 'X'
page_url = f'/strategy/{page}'
# bp_{page}
bp_strategy = Blueprint(
    f'bp_{page}',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path=f'/{page}/static',
)

#@bp_{page}
#def {page}():
@bp_strategy.route(f'/loading')
def loading_strategy_page():
    args = request.args
    strategy = args.get('strategy', 'none')
    full_path = os.path.join('strategy_files', f'{strategy}.py')
    if not os.path.isfile(full_path):
        return 'Does not exist'
    fn = importlib.import_module(f'strategy_files.{strategy}')
    return render_template(
        f'loading_strategy.html',
        strategy_name=fn.strategy_name,
        strategy_url=f'/strategy/{strategy}',
    )

#@bp_{page}
#def {page}():
@bp_strategy.route(f'/strategy/<strategy>')
def strategy_page(strategy):
    db = database.Database()
    df = db.load_data()
    strategy_module = importlib.import_module(f'strategy_files.{strategy}')
    strategy_fn = getattr(strategy_module, strategy)
    picks = toolbox.find_todays_breakout(
        df,
        strategy_fn,
        days=strategy_module.days_to_backtest,
    )
    
    return render_template(
        f'strategy.html',
        db=db,
        picks=picks,
        strategy_name=strategy_module.strategy_name,
    )