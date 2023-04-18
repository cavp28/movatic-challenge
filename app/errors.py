from flask import jsonify
from werkzeug.exceptions import HTTPException

def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify({'error': str(e)}), code