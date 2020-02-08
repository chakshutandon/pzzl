from flask import Blueprint, jsonify
from random import randint

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)
