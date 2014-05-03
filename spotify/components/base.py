from requests_futures.sessions import FuturesSession

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'


class Component(object):
    def __init__(self, sp=None):
        self.sp = sp

        self.session = None

        # Inherit session from global
        if self.sp:
            self.session = self.sp.session

    def create_session(self, user_agent):
        self.session = FuturesSession()

        # Update headers
        self.session.headers.update({
            'User-Agent': user_agent or USER_AGENT
        })

    def send(self, name, *args):
        return self.sp.send(name, *args)

    def build(self, name, *args):
        return self.sp.build(name, *args)

    def send_request(self, request):
        return self.sp.send_request(request)

    def send_message(self, message):
        self.sp.send(message)

    @staticmethod
    def request_wrapper(request, callback=None, async=True, timeout=None):
        if not async:
            return request.wait(
                timeout,
                on_bound=lambda: request.send()
            )

        return request.on(
            'success', callback,
            on_bound=lambda: request.send()
        )
