# -*- coding: UTF-8 -*-
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from jinja2 import Environment, FileSystemLoader
 
# 第三方 SMTP 服务
mail_host = "smtp.163.com"      # SMTP服务器
mail_user = "nick_hxy@163.com"                  # 用户名
mail_pass = "qwe839507834"               # 授权密码，非登录密码
 
sender = 'nick_hxy@163.com'    # 发件人邮箱(最好写全, 不然会失败)
receivers = ['839507834@qq.com', 'huangxy17@fudan.edu.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

def render_template(template_name, **context):
    """Renders a template from the template folder with the given context.

    Parameters
    ----------
    template_name : string
        The name of the template to be rendered.
    context : dict
        The variables that should be available in the context of the template.

    Returns
    -------
    parsed_template : string
        The parsed template.
    """
    env = Environment(loader=FileSystemLoader('/root/quant/template'))
    template = env.get_template(template_name)
    parsed_template = template.render(**context)
    return parsed_template

class EmailWorker:
  def __init__(self, host=mail_host, send_mail=mail_user, send_pass=mail_pass, recv_mail=";".join(receivers)):
    self.host = host
    self.send_mail = send_mail
    self.send_pass = send_pass
    self.recv_mail = recv_mail
    
  def Send(self, subject='Default Subject', content="This is a test"):
    try:
      mail_client = smtplib.SMTP(self.host)
      mail_client.login(self.send_mail, self.send_pass)
      msg = MIMEText(content, 'plain', 'utf-8')
      msg['Subject'] = Header('[自动邮件]'+subject, 'utf-8')  # subject
      msg['From'] = self.send_mail
      msg['To'] = self.recv_mail
      mail_client.sendmail(self.send_mail, self.recv_mail, msg.as_string())
      mail_client.quit()
    except Exception as e:
      print('Send Failed! %s' %(str(e)))

  def SendHtml(self, subject='Default Subject', content="This is a test", png_list=[]):
    try:
      mail_client = smtplib.SMTP_SSL(self.host, port=465)
      #mail_client = smtplib.SMTP('smtpdm.aliyun.com')
      print('email connet host ok')
      mail_client.login(self.send_mail, self.send_pass)
      print('email login ok')
      # create msg
      msg = MIMEMultipart('mixed')
      msg.attach(MIMEText(content, 'html', 'utf-8'))
      msg['Subject'] = Header('[自动邮件]'+subject, 'utf-8')  # subject
      msg['From'] = self.send_mail
      msg['To'] = self.recv_mail
      for pl in png_list:
        att = MIMEImage(open(pl, 'rb').read())
        att.add_header('Content-ID','<image1>')
        msg.attach(att)
      mail_client.sendmail(self.send_mail, self.recv_mail, msg.as_string())
      mail_client.quit()
    except Exception as e:
      print('SendHtml Failed! %s' %(str(e)))

  def SendMulti(self):
    msg = MIMEMultipart('mixed') 
    msg['Subject'] = 'Python email test'
    msg['From'] = 'XXX@163.com <XXX@163.com>'
    msg['To'] = 'XXX@126.com'
    msg['Date']='2012-3-16'

if __name__=='__main__':
  EM = EmailWorker()
  #EM.Send()
  #with open('test', 'w') as f:
    #f.write(render_template('PT_report.html'))
  EM.SendHtml(content = render_template('PT_report.html'), png_list=['/root/pnl.png'])
