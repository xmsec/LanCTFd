from CTFd.utils.security.csrf import generate_nonce
from flask import session


def login_user(user):
    session['id'] = user.id
    session['name'] = user.name
    session['type'] = user.type
    session['email'] = user.email
    session['nonce'] = generate_nonce()
    session['elimit'] = 0

def logout_user():
    session.clear()

def send_mail_limit():
    if session['elimit']<2:
        session['elimit']=session['elimit']+1
        return  True
    return False
