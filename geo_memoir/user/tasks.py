from django.core import mail
from django.template.loader import render_to_string

from geo_memoir.celery import app


@app.task
def email_password_reset_link(lang_code, email, recipient, reset_url):
    subject = 'Geo Memoir Password Reset'
    html_message = get_password_reset_email(lang_code, recipient, reset_url)
    mail.send_mail(
        subject=subject,
        message='',  # 由於沒有默認值, 需要給一個空
        from_email='travelwithgeomemo@gmail.com',
        recipient_list=[email],
        html_message=html_message
    )


@app.task
def send_change_email_code(lang_code, email, recipient, code):
    subject = 'Geo Memoir Verification Code'
    get_code_email(lang_code, recipient, code)
    html_message = '''
            <strong>Dear %s,</strong><br>
            <br>
            A request has been received to change the email for your <b>Geo Memoir</b> account.<br>
            Please use the verification code below to change your email: 
            <br>
            <h1>%d</h1>
            <br>
            <h4 style="color:darkred;"><strong>This code is only valid for 5 minutes.</strong></h4>  
            <br>
            Thanks,<br>
            Geo Memoir      
            ''' % (recipient, code)
    mail.send_mail(
        subject=subject,
        message='',  # 由於沒有默認值, 需要給一個空
        from_email='travelwithgeomemo@gmail.com',
        recipient_list=[email],
        html_message=html_message
    )


def get_password_reset_email(lang_code, recipient, reset_url):
    html_message_en = '''
                <strong>Dear %s,</strong><br>
                <br>
                A request has been received to change the password for your <b>Geo Memoir</b> account.<br>
                Click the link below to create a new password: 
                <div style="margin: 30px;">
                <a href="%s" target="_blank" style="text-decoration:none; color: blue; background-color: rgb(253, 255, 165); padding: 10px;">
                <strong>Click this link to reset your password</strong>
                </a>
                </div>
                <h4 style="color:darkred;"><strong>This link is only valid for 5 minutes.</strong></h4>
                Thanks,<br>
                Geo Memoir Team
                ''' % (recipient, reset_url)
    html_message_tw = '''
                <strong>Dear %s,</strong><br>
                <br>
                我們已經收到更改您的 <b>Geo Memoir</b> 帳戶密碼的請求。<br>
                請點擊下面的鏈接以創建新密碼： 
                <div style="margin: 30px;">
                <a href="%s" target="_blank" style="text-decoration:none; color: blue; background-color: rgb(253, 255, 165); padding: 10px;">
                <strong>點擊此鏈接重置您的密碼</strong>
                </a>
                </div>
                <h4 style="color:darkred;"><strong>此鏈接僅在 5 分鐘內有效</strong></h4>
                Thanks,<br>
                Geo Memoir Team
                ''' % (recipient, reset_url)
    html_message_cn = '''
                <strong>Dear %s,</strong><br>
                <br>
                我们已收到更改您的 <b>Geo Memoir</b> 帐户密码的请求。
                请点击下面的链接以创建新密码： 
                <div style="margin: 30px;">
                <a href="%s" target="_blank" style="text-decoration:none; color: blue; background-color: rgb(253, 255, 165); padding: 10px;">
                <strong>点击此链接重置您的密码</strong>
                </a>
                </div>
                <h4 style="color:darkred;"><strong>此链接仅在 5 分钟内有效</strong></h4>
                Thanks,<br>
                Geo Memoir Team
                ''' % (recipient, reset_url)

    if lang_code == 'en':
        html_message = html_message_en
    elif lang_code == 'zh_Hant_TW':
        html_message = html_message_tw
    else:
        html_message = html_message_cn

    return html_message


def get_code_email(lang_code, recipient, code):
    html_message_en = '''
                <strong>Dear %s,</strong><br>
                <br>
                A request has been received to change the email for your <b>Geo Memoir</b> account.<br>
                Please use the verification code below to change your email: 
                <br>
                <h1>%d</h1>
                <br>
                <h4 style="color:darkred;"><strong>This code is only valid for 5 minutes.</strong></h4>  
                <br>
                Thanks,<br>
                Geo Memoir Team   
                ''' % (recipient, code)
    html_message_tw = '''
                <strong>Dear %s,</strong><br>
                <br>
                我們已收到更改您的 <b>Geo Memoir</b> 帳戶電子郵件的請求。<br>
                請使用以下驗證碼更改您的電子郵件： 
                <br>
                <h1>%d</h1>
                <br>
                <h4 style="color:darkred;"><strong>此代碼僅在 5 分鐘內有效</strong></h4>  
                <br>
                Thanks,<br>
                Geo Memoir Team 
                ''' % (recipient, code)
    html_message_cn = '''
                <strong>Dear %s,</strong><br>
                <br>
                我们已收到更改您的 <b>Geo Memoir</b> 帐户邮箱的请求。<br>
                请使用以下验证码更改您的邮箱： 
                <br>
                <h1>%d</h1>
                <br>
                <h4 style="color:darkred;"><strong>此代码仅在 5 分钟内有效</strong></h4>  
                <br>
                Thanks,<br>
                Geo Memoir Team 
                ''' % (recipient, code)

    if lang_code == 'en':
        html_message = html_message_en
    elif lang_code == 'zh_Hant_TW':
        html_message = html_message_tw
    else:
        html_message = html_message_cn

    return html_message

