# coding=utf-8

import re
import websocket
import smtplib
import fklayouts

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class FkChecker(object):
    endpoint = ''
    frames = []
    options = None
    ws = None
    total_validated = 0
    total_validation_run = 0

    def __init__(self, endpoint, options):
        self.endpoint = endpoint
        self.options = options
        websocket.enableTrace(True)

    def execute(self):
        if 'timeout' in self.options:
            websocket.setdefaulttimeout(self.options['timeout'])

        self.ws = websocket.WebSocketApp(self.endpoint,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

        self.ws.on_open = self.on_open

        print "### Starting... ###"
        self.ws.run_forever()

    def add_frame(self, message):
        self.frames.append(message)

    def validate(self):
        for validation in self.options['validations']:
            if validation['type'] == 'regex':
                regex = re.compile(validation['value'])
                for frame in self.frames:
                    regex_test = regex.match(frame)
                    if regex_test is not None:
                        self.total_validated += 1

    def on_message(self, ws, message):
        print message
        if len(self.frames) >= self.options['total_frames']:
            self.ws.close()
        else:
            self.add_frame(message)

    def on_error(self, ws, error):
        self.ws.close()
        print error

    def on_close(self, ws):
        print "### closed ###"
        self.validate()

        if self.get_assert_rate >= self.options['assert_rate']:
            self.on_success()
        else:
            self.on_fail()

    def on_open(self, ws):
        if 'send' in self.options:
            ws.send(self.options['send'])
            print "sending: " + self.options['send']

    def on_success(self):
        print "Test passed!"
        # TODO: Develop the callers for success event
        if 'on_success' in self.options and len(self.options['on_success']) > 0:
            for action in self.options['on_success']:
                if action['type'] == 'mail' and 'smtp' in self.options:
                    self.fire_email('success')

    def on_fail(self):
        print "Test failed!"
        # i'm a cow boy on my steel horse i ride! xD
        # TODO: Develop the callers for fail event
        if 'on_fail' in self.options and len(self.options['on_fail']) > 0:
            for action in self.options['on_fail']:
                if action['type'] == 'mail' and 'smtp' in self.options:
                    self.fire_email('fail')

                elif action['type'] == 'shell':
                    #TODO: implement shell code action for FAIL
                    pass

    def get_tags(self):
        return {
            '{ENDPOINT}': self.endpoint,
            '{TOTAL_FRAMES}': str(self.get_recv_frames),
            '{TOTAL_ASSERTS}': str(self.get_asserts),
            '{TOTAL_VALIDATIONS}': str(self.get_validations_runned),
            '{ASSERT_RATE}': str(self.get_assert_rate),
        }

    def fire_email(self, event):
        if 'fail' == event:
            self.options['smtp']['subject'] = '[WS/FAIL] Websocket (' + self.endpoint + ') fail'
            message = fklayouts.get_layout('FAIL', self.get_tags())

        elif 'success' == event:
            self.options['smtp']['subject'] = '[WS/SUCCESS] Websocket (' + self.endpoint + ') succeded'
            message = fklayouts.get_layout('SUCCESS', self.get_tags())

        smtp_mail = SmtpMail(self.options['smtp'])
        smtp_mail.send(message)

    @property
    def get_asserts(self):
        return self.total_validated

    @property
    def get_assert_rate(self):
        return ((100 * self.total_validated) / (len(self.options['validations']) * len(self.frames)))

    @property
    def get_recv_frames(self):
        return len(self.frames)

    @property
    def get_validations_runned(self):
        return len(self.options['validations']) * len(self.frames)


class SmtpMail(object):

    host = ''
    port = ''
    username = ''
    password = ''
    instance = None
    tls = False

    options = []
    subject = ''
    email_from = ''
    email_to = ''
    message = ''

    def __init__(self, options):

        self.host = options['host']
        self.port = options['port']

        self.email_from = options['from']
        #self.email_to = ", ".join(options['to'])
        self.email_to = options['to']

        self.username = options['username']

        self.password = options['password']

        self.subject = options['subject']

        if 'tls' in options:
            self.tls = options['tls']

    def send(self, message):

        try:

            self.instance = smtplib.SMTP(self.host, str(self.port))
            self.instance.ehlo()
            self.instance.login(self.username, self.password)
            if self.tls:
                self.instance.starttls()

            msg = MIMEMultipart('alternative')
            msg['Subject'] = self.subject
            msg['From'] = self.email_from
            msg['To'] = ", ".join(self.email_to)
            msg.attach(MIMEText(message, 'html'))

            self.instance.sendmail(self.email_from, self.email_to, msg.as_string())
            self.instance.quit()

        except Exception, e:
            print '### ERROR :: ' + e.message + ' ### '
        finally:
            print '### MAIL SENT... ###'

