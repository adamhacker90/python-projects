import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email = "redboxdaemon@gmail.com" # the email where you sent the email
password = "R3c0rder"
send_to_email = "ahacker@redboxvoice.com" # for whom
subject = "TEST"
message = "This is a test email sent by Python. Isn't that cool?!"

msg = MIMEMultipart()
msg["From"] = email
msg["To"] = send_to_email
msg["Subject"] = subject

msg.attach(MIMEText(message, 'plain'))

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email, password)
text = msg.as_string()
server.sendmail(email, send_to_email, text)
server.quit()