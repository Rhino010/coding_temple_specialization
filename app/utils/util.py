import jose
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "my secret"

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(customer_id)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:

            token = request.headers['Authorization'].split()[1]

            if not token:
                return jsonify({"message": "missing token"}), 400
            
            try:

                data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                print(data)
                customer_id = data['sub']

            except ExpiredSignatureError:
                return jsonify({"message": "Token expired."}), 400
            except JWTError:
                return jsonify({"message": "Invalid token."})
            
            return f(customer_id, *args, **kwargs)
        
        else:
            return jsonify({"message": "you must be logged in to access this."})
        
    return decorated
