from functools import wraps
from flask import session, redirect, url_for

def login_obrigatorio(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('index'))  # redireciona pro login
        return f(*args, **kwargs)
    return decorated_function

def acesso_minimo(nivel_requerido):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'nivel' not in session or session['nivel'] > nivel_requerido:
                return redirect(url_for('index'))  # acesso negado
            return f(*args, **kwargs)
        return decorated_function
    return decorator
