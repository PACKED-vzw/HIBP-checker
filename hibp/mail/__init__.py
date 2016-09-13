import smtplib
from os.path import join
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from hibp.config import Config


class Mail:

    def __init__(self):
        self.config = Config()
        self.server = smtplib.SMTP(self.config.config['mail']['server'], self.config.config['mail']['port'])

    def start(self):
        self.server.starttls()
        self.server.login(self.config.config['mail']['username'], self.config.config['mail']['password'])

    def stop(self):
        self.server.quit()

    def send(self, recipient, msg_text, subject=None):
        if not subject:
            subject = 'Your email address {0} has been found inside a data leak'.format(recipient)
        msg = MIMEMultipart()
        msg['From'] = self.config.config['mail']['username']
        msg['To'] = ', '.join([recipient, self.config.config['main']['it_email']])
        msg['Subject'] = subject
        msg.attach(MIMEText(msg_text, 'plain'))
        self.start()
        self.server.sendmail(self.config.config['mail']['username'], recipient, msg.as_string())
        self.stop()

    def breach_msg(self, email, breaches):
        msg = ''
        with open(join('config', self.config.config['mail']['msg']), 'r') as f:
            msg = f.read()
        return msg.format(
            USERNAME=email,
            LEAKS=', '.join(['{0} ({1}, ca. {2})'.format(b['Title'], b['Domain'], b['BreachDate']) for b in breaches])
        )
