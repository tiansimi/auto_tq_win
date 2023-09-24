import os

import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from conf.config import conf
from common.log import log


class Mail:
    """封装发送邮件类"""

    def __init__(self):
        # 第一步：连接到smtp服务器
        # self.smtp_s = smtplib.SMTP_SSL(host='smtp.exmail.qq.com', port=465)
        try:
            self.smtp_s = smtplib.SMTP(host=conf.host, port=conf.port)
            # self.smtp_s = smtplib.SMTP()
            # self.smtp_s.connect(host=conf.host, port=conf.port)
            log.info('连接邮件服务器成功！')
        except Exception as e:
            log.error(f'初始化 smtp 协议失败：{e}')
        else:
            # 第二步：登陆smtp服务器
            self.smtp_s.login(user=conf.user, password=conf.pwd)

    def conn_server(self):
        self.smtp_s = smtplib.SMTP(host=conf.host, port=conf.port)
        self.smtp_s.login(user=conf.user, password=conf.pwd)

    def send_text(self, subject, content):
        """
        发送文本邮件
        :param subject: 邮件主题
        :param content: 邮件正文
        :return:
        """
        # 第三步：准备邮件
        # 使用email构造邮件
        msg = MIMEText(content, _subtype='plain', _charset="utf8")
        # 添加发件人
        msg["From"] = conf.sender
        # 添加收件人
        msg["To"] = conf.receivers
        # 添加邮件主题
        msg["subject"] = subject
        # 第四步：发送邮件
        try:
            self.smtp_s.send_message(msg, from_addr=conf.sender, to_addrs=conf.receivers)
            print('发送成功')
        except Exception as e:
            print('发送失败')
        else:
            self.smtp_s.quit()

    def send_file(self, subject, file_name):
        """
        发送测试报告邮件
        :param subject: 主题
        :param file_name: 发送文件的路徑名称
        """

        # 读取报告文件中的内容
        file_content = open(file_name, "rb").read()
        # 2.使用email构造邮件
        # （1）构造一封多组件的邮件
        msg = MIMEMultipart()
        # (2)往多组件邮件中加入文本内容
        text_msg = MIMEText('text...', _subtype='plain', _charset="GB2312")
        msg.attach(text_msg)
        # (3)往多组件邮件中加入文件附件
        file_msg = MIMEApplication(file_content)
        # file_msg.add_header('content-disposition', 'attachment', filename=file_name)
        # fn = os.path.split(file_name)[-1]
        # file_msg.add_header('content-disposition', 'attachment', filename=('gbk', '', fn))
        file_msg.add_header('content-disposition', 'attachment', filename=os.path.split(file_name)[-1])
        msg.attach(file_msg)

        # 添加发件人
        msg["From"] = conf.sender
        # 添加收件人
        msg["To"] = conf.receivers
        # 添加邮件主题
        msg["subject"] = subject
        try:
            # 第四步：发送邮件
            self.smtp_s.send_message(msg, from_addr=conf.sender, to_addrs=conf.receivers)

        except Exception as e:
            log.error(f'邮件发送失败{e}')
        else:
            log.info(f'邮件发送成功, 文件地址：{file_name}')
        finally:
            self.smtp_s.quit()


if __name__ == '__main__':
    # Mail().send_text('test', 'fdafdsqfdsafsd')
    Mail().send_file('测试邮件', r'C:\Users\HR\Desktop\config.db')