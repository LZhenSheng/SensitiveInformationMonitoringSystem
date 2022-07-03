from email.header import Header
import smtplib
from email.mime.text import MIMEText  # 创建邮件内容的文件内容
from email.mime.multipart import MIMEMultipart  # 创建带附件的实例
from email.mime.application import MIMEApplication


# 发送带附件邮箱
class Mail():
    def __init__(self) -> None:
        # 配置第三方smtp服务相关信息
        self.mail_host = "SMTP.qq.com"
        self.mail_pass = "todintrvetblebbd"  # 授权码
        self.sender = "2254263875@qq.com"
        self.receivers = "3489612495@qq.com"

    # 创建带附件实例
    def send(self):
        message = MIMEMultipart()
        # 创建参数
        message['From'] = Header("网络敏感信息监控系统", 'utf-8')
        message['To'] = Header("小付", 'utf-8')
        message['Subject'] = Header("敏感信息报告", 'utf-8')

        # 加入邮件正文内容
        message.attach(MIMEText('敏感信息报告', 'plain', 'utf-8'))

        # 构建邮件附件
        att = MIMEText(open("tools/mydata.xls", "rb").read(), 'base64', 'utf-8')  # 打开附件
        att["Content-Type"] = 'application/octet-stream'  # 设置类别信息
        att["Content-Disposition"] = 'attachment; filename="mydata.xls"'  # 添加描述信息
        message.attach(att)  # 加入到邮件中
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            print('邮件发送成功')
        except smtplib.SMTPException as e:
            print('邮件发送失败')


if __name__ == '__main__':
    mail = Mail()
    mail.send()