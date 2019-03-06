from flask import current_app as app, url_for
from CTFd.utils import get_config, get_app_config
from CTFd.utils.config import get_mail_provider, mailserver
from CTFd.utils.email import mailgun, smtp
from CTFd.utils.security.signing import serialize
import re


EMAIL_REGEX = r"(^[^@\s]+@[^@\s]+\.[^@\s]+$)"


def sendmail(addr, text):
    provider = get_mail_provider()
    if provider == 'smtp':
        return smtp.sendmail(addr, text)
    if provider == 'mailgun':
        return mailgun.sendmail(addr, text)
    return False, "No mail settings configured"


def forgot_password(email, team_name):
    token = serialize(team_name)
    text = """
    <!DOCTYPE html>
<html>

<body style="margin: 0; font-family: 'Cabin', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif';color: #6e7b8a; text-align: center;">

    <div style="background: #fff; margin: 0 auto; max-width: 550px;">
        <p style="font-size: 1.25rem; font-weight: 200; line-height: 1.5rem;">
            How to reset your password is as follows.
        </p>
        <p>Please click the following link to reset your password:</p>
        
        <a href="{0}/{1}
           style="background: #22b8eb;
           padding: 10px 20px 10px 30px;
           margin-bottom: 20px;
           color: #fff;
           font-size: .85rem;
           text-decoration: none;
           display: inline-block;
           text-align: center;
           cursor: pointer;
           border-radius: 5px;">Confirm Your Email</a>
        <br>
        <br><br><br><br>If you are not trying to reset your password, please ignore this email. It is possible that another user entered their login information incorrectly.<br>

    </div>
    
</body>

</html>



""".format(url_for('auth.reset_password', _external=True), token)

    return sendmail(email, text)


def verify_email_address(addr):
    token = serialize(addr)
    text = """
<!DOCTYPE html>
<html>

<body style="margin: 0; font-family: 'Cabin', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif';color: #6e7b8a; text-align: center;">

    <div style="background: #fff; margin: 0 auto; max-width: 550px;">
        <p style="font-size: 1.25rem; font-weight: 200; line-height: 1.5rem;">
            Welcome to {ctf_name}.
        </p>
        <p>Please click the following link to confirm your email address for {ctf_name}: </p>
        
        <a href="{url}/{token}"
           style="background: #22b8eb;
           padding: 10px 20px 10px 30px;
           margin-bottom: 20px;
           color: #fff;
           font-size: .85rem;
           text-decoration: none;
           display: inline-block;
           text-align: center;
           cursor: pointer;
           border-radius: 5px;">Confirm Your Email</a>
        <br>If you are not trying to confirm your email, please ignore this email. It is possible that another user entered their login information incorrectly.<br>
        <br><br><br><br>{info_add}
    </div>
    
</body>

</html>
    """.format(
        ctf_name=get_config('ctf_name'),
        url=url_for('auth.confirm', _external=True),
        token=token,
        info_add='Held by <a href="https://lancet.vip">Lancet</a>.'
    )
    return sendmail(addr, text)


def check_email_format(email):
    return bool(re.match(EMAIL_REGEX, email))


def check_email_is_whitelisted(email_address):
    local_id, _, domain = email_address.partition('@')
    domain_whitelist = get_config('domain_whitelist')
    if domain_whitelist:
        domain_whitelist = [d.strip() for d in domain_whitelist.split(',')]
        if domain not in domain_whitelist:
            return False
    return True
