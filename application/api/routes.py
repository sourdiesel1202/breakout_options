print(__name__)
#from flask import current_app as app
from flask import Blueprint
from flask import request
#from application.app import framework
from application.app import database
from application.app import strategies
from application.app import toolbox

import json

page = 'api'
# bp_{page}
bp_api = Blueprint(
    f'bp_{page}',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path=f'/{page}/static',
)

#@bp_{page}
#def {page}():
@bp_api.route(f'/{page}/update')
def api_update():
    db = database.Database()
    db.update_historic_data()
    inventory = [getattr(strategies, x) for x in strategies.inventory]
    return json.dumps({'success': True})

#@bp_{page}
#def {page}():
@bp_api.route(f'/{page}/price/get')
def api_price_get():
    args = request.args
    symbol = args.get('symbol')
    contract_type = args.get('contract_type')
    gain = args.get('gain')
    
    row_data = {
        'symbol': symbol,
        'contract_type': contract_type,
        'gain': gain,
    }
    output = toolbox.get_pricing(symbol, contract_type, gain)
    return json.dumps(output)



#@bp_{page}
#def {page}():
@bp_api.route(f'/{page}')
def api():
    return json.dumps({'success': True})