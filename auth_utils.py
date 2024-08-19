from functools import wraps
from flask import request, jsonify

def check_password(password):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            provided_password = data.get('password') if data else None
            
            if provided_password and provided_password == password:
                return f(*args, **kwargs)
            else:
                return jsonify({'error': 'Unauthorized access'}), 401
        return decorated_function
    return decorator
