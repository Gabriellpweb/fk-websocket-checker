import websocket
import re


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

    def on_fail(self):
        print "Test failed!"
        # TODO: Develop the callers for fail event

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
