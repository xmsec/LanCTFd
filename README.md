![](https://github.com/CTFd/CTFd/blob/master/CTFd/themes/core/static/img/logo.png?raw=true)
====

## CTFd
https://github.com/CTFd/CTFd


请使用官方CTFd，已发现的 bug 已提交修复，且本身版本比官方版本低，存在其他 bug。
## LanCTFd -- Modified CTFd
1. 添加谷歌验证码，支持大陆环境（via [ctfd-recaptcha-plugin](https://github.com/tamuctf/ctfd-recaptcha-plugin)）
2. 前端移除第三方授权验证，仅保留账号验证登录
3. 修改 SMTP 服务器发信内容，减少被服务器拒绝概率；修复发信返回值未判断的 bug（官方已 fix）
4. 控制未验证账号重发次数，在 CTFd/utils/security/auth.py 中硬编码实现
5. 动态积分插件，计分公式适应性修改，适配20人解出时达到最低值，使用自定义公式
6. 修复动态积分插件中，隐藏用户提交 flag 后造成分数变化的 bug [PR](https://github.com/CTFd/CTFd/pull/919)
7. 修复普通用户在 profile 中排名与 scoreboard 排名不一致的 bug [PR](https://github.com/CTFd/CTFd/pull/918)
8. 小幅修改
### Code
#### 控制重发
`CTFd/utils/security/auth.py`
```
def send_mail_limit():
    if session['elimit']<2:
        session['elimit']=session['elimit']+1
        return  True
    return False
```

```
def confirm(data=None):
  ……
     if data is None:
        if request.method == "POST":
            # User wants to resend their confirmation email
            if send_mail_limit():
            ……
            
```
#### 动态积分
```
            value = chal.initial * 0.03 + (
                (chal.initial * 0.97) / (1 +
                    (max(0, solve_count) / 4.92201) ** 3.206069
                )
            )
            
            value = math.ceil(value)

            if value < chal.minimum:
                value = chal.minimum

            if chal.decay != 0 and solve_count >= chal.decay:
                value = chal.minimum
        
```
#### SMTP
`smtp.py`
```
def sendmail(addr, text):
    ……
        try:
        smtp = get_smtp(**data)
        msg = MIMEText(text, 'html', 'utf-8')
        msg['Subject'] = Header("{0} Account Status Message".format(ctf_name), 'utf-8')
        msg['From'] = ctf_name+'<'+mailfrom_addr+'>'
        msg['To'] = addr

        smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
        smtp.quit()
        return True, "Email sent"
```
`__init__.py`
```
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
```

### Deploy
```
docker-compose up
``` 
### Backup
使用 docker-compose 方式部署时，redis、misql、CTFd 挂载于 .data 目录以备份。
### Maintance
docker-compsoe.yml services restart automaticly

## What is CTFd?
CTFd is a Capture The Flag framework focusing on ease of use and customizability. It comes with everything you need to run a CTF and it's easy to customize with plugins and themes.


## Features
 * Create your own challenges, categories, hints, and flags from the Admin Interface
    * Dynamic Scoring Challenges
    * Unlockable challenge support
    * Challenge plugin architecture to create your own custom challenges
    * Static & Regex based flags
        * Custom flag plugins
    * Unlockable hints
    * File uploads to the server or an Amazon S3-compatible backend
    * Limit challenge attempts & hide challenges
    * Automatic bruteforce protection
* Individual and Team based competitions
    * Have users play on their own or form teams to play together
 * Scoreboard with automatic tie resolution
    * Hide Scores from the public
    * Freeze Scores at a specific time
 * Scoregraphs comparing the top 10 teams and team progress graphs
 * Markdown content management system
 * SMTP + Mailgun email support
    * Email confirmation support
    * Forgot password support
 * Automatic competition starting and ending
 * Team management, hiding, and banning
 * Customize everything using the [plugin](https://github.com/CTFd/CTFd/wiki/Plugins) and [theme](https://github.com/CTFd/CTFd/tree/master/CTFd/themes) interfaces
 * Importing and Exporting of CTF data for archival
 * And a lot more...

## Install
  1. Install dependencies: `pip install -r requirements.txt`
       1. You can also use the `prepare.sh` script to install system dependencies using apt.
  2. Modify [CTFd/config.py](https://github.com/CTFd/CTFd/blob/master/CTFd/config.py) to your liking.
  3. Use `flask run` in a terminal to drop into debug mode.

You can use the auto-generated Docker images with the following command:

`docker run -p 8000:8000 -it ctfd/ctfd`

Or you can use Docker Compose with the following command from the source repository:

`docker-compose up`

Check out the [wiki](https://github.com/CTFd/CTFd/wiki) for [deployment options](https://github.com/CTFd/CTFd/wiki/Basic-Deployment) and the [Getting Started](https://github.com/CTFd/CTFd/wiki/Getting-Started) guide

## Live Demo
https://demo.ctfd.io/

## Support
To get basic support, you can join the [CTFd Slack Community](https://slack.ctfd.io/): [![CTFd Slack](https://slack.ctfd.io/badge.svg)](https://slack.ctfd.io/)

If you prefer commercial support or have a special project, feel free to [contact us](https://ctfd.io/contact/).

## Managed Hosting
Looking to use CTFd but don't want to deal with managing infrastructure? Check out [the CTFd website](https://ctfd.io/) for managed CTFd deployments.

## MajorLeagueCyber
CTFd is heavily integrated with [MajorLeagueCyber](https://majorleaguecyber.org/). MajorLeagueCyber (MLC) is a CTF stats tracker that provides event scheduling, team tracking, and single sign on for events. 

By registering your CTF event with MajorLeagueCyber users can automatically login, track their individual and team scores, submit writeups, and get notifications of important events. 

To integrate with MajorLeagueCyber, simply register an account, create an event, and install the client ID and client secret in the relevant portion in `CTFd/config.py` or in the admin panel:

```python
OAUTH_CLIENT_ID = None
OAUTH_CLIENT_SECRET = None
```

## Credits
 * Logo by [Laura Barbera](http://www.laurabb.com/)
 * Theme by [Christopher Thompson](https://github.com/breadchris)
