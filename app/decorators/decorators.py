from functools import wraps
from flask import redirect, session, url_for

def logged_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "trainer_name" not in session:
            session["login_error"] = ["Introduce your trainer's name to access Pokémon Battle Web"]
            return redirect(url_for("trainer.login"))
        return func(*args, **kwargs)
    return wrapper