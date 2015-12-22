# coding: UTF-8
import smtplib
import email.utils
import getpass
from email.message import Message
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def get_massage(mail_from, mail_to, mail_cc, mail_bcc):
	message = MIMEMultipart('alternative')
	#message.set_unixfrom('author')

	# from, to, subject
	message['Subject'] = '涨薪通知'
	message['From'] = mail_from
	message['To'] = ";".join(mail_to)
	message['Cc'] = mail_cc
	message['Bcc'] = mail_bcc


	# html body
	html = 	"""Hi,\
		<html>
		   <head>
		      <meta charset="UTF-8">
		   </head>
		   <body>
		      <p>&nbsp;&nbsp;&nbsp;&nbsp;锡伟同学，很高兴通知你，你的工资提升到人民币50,000/月。感谢努力。</p>
		      <br>
		      &nbsp;&nbsp;&nbsp;&nbsp;此致
		      <br>
		      &nbsp;&nbsp;&nbsp;&nbsp;噢，对了，记得请杨小见吃个饭。
		      <p>_____________________________</p>
		      <p>This email (including any attachments) is confidential. It may be read, copied and used only by the intended recipient. If you have received it in error, please contact the sender immediately by return email. Please then delete this email (including its attachments) and do not disclose their contents to any third person.</p>
		   </body>
		</html>
		"""
	txt = MIMEText(html, 'html', 'UTF-8')
	# this may be coverd by inline image
	message.attach(txt)

	# inline image attachment
	body = 'Emoji-congratulations'
	con = MIMEText('<b>%s</b><img alt="ltr" src="cid:D:\\10535-102.jpg"/>'%body,'html')
	message.attach(con)
	img = MIMEImage(file('/home/yangxiaojian/Desktop/small.png','rb').read())
	img.add_header('Content-ID','D:\\10535-102.jpg')
	message.attach(img)
	 
	# file attachemnt
	att = MIMEText(open('/home/yangxiaojian/Desktop/small.png', 'rb').read(), 'base64', 'gb2312')
	att["Content-Type"] = 'application/octet-stream'
	att["Content-Disposition"] = 'attachment; filename="pic.png"'
	message.attach(att)

	# end
	return message


if __name__ == "__main__":
	# mail from and mail to
	# Prompt the user for connection info
	# your accout, must real account
	username = raw_input('Mail user name: ')
	password = getpass.getpass("%s's password: " % username)
	servername = raw_input('Mail server name: ')
	mail_to = raw_input('Recipient: ')
	mail_cc = raw_input('Cc to: ')
	who = raw_input('Faking who:')
	address = raw_input('Email address of %s:' % who)
	mail_from = email.utils.formataddr((who, address))
        
        
	# not work, just show in receiver, no send actually, bug..
        # mail_cc = 'hr@apple.com'
	# not work, just show in receiver, no send actually
	mail_bcc = 'forjobs@foxmail.com'

	# testing
        #username = "forjobs@foxmail.com"
        #password = "zhendejuedewohuixiezhema"
	#mail_to = ['forjobs@foxmail.com']
	#servername = "smtp.qq.com"
	#mail_from = email.utils.formataddr(('Steve Jobs', 'steve@apple.com'))

	server = smtplib.SMTP(servername, port = 587, timeout = 20)
	try:
	    server.set_debuglevel(True)

 	    # identify ourselves, prompting server for supported features
  	    server.ehlo()

  	    # If we can encrypt this session, do it
 	    if server.has_extn('STARTTLS'):
  	        server.starttls()
  	        server.ehlo() # re-identify ourselves over TLS connection

   	    # creat massage
   	    msg = get_massage(mail_from, mail_to, mail_cc, mail_bcc)
	
 	    server.login(username, password)
  	    # send
   	    server.sendmail(username, mail_to, msg.as_string())
	finally:
  	  server.quit()
	  print'Send success!'

