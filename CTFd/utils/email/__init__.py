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
            您好，您正在重置账号
        </p>
        <p>请点击下面链接以重置账号: </p>
        
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
        <br><br><br><br>若您误收到此电子邮件，可能是其他用户在申请帐号时误操作，您可忽略此邮件。
    </div>
    
</body>

</html>



""".format(url_for('auth.reset_password', _external=True), token)

    sendmail(email, text)


def verify_email_address(addr):
    token = serialize(addr)
    text = """
<!DOCTYPE html>
<html>

<body style="margin: 0; font-family: 'Cabin', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif';color: #6e7b8a; text-align: center;">

    <div style="background: #fff; margin: 0 auto; max-width: 550px;">
        <p style="font-size: 1.25rem; font-weight: 200; line-height: 1.5rem;">
            您好，欢迎加入 {ctf_name}，您正在激活账号
        </p>
        <p>请点击下面链接以激活 {ctf_name} 中的账号: </p>
        
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
        <br>{info_add}
        <br><br><br><br>若您误收到此电子邮件，可能是其他用户在申请帐号时误操作，您可忽略此邮件。
    </div>
    
</body>

</html>
    """.format(
        ctf_name=get_config('ctf_name'),
        url=url_for('auth.confirm', _external=True),
        token=token,
        info_add="LanCTF 由 Lancet 举办，由一群热爱网络安全的北航学生组成。Lancet 名为柳叶刀，寓意着 Lancet 战队既能做披襟斩棘的战刃，也能做祛病消灾的手术刀，以保护信息时代的安全感。"
    )
    sendmail(addr, text)


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
