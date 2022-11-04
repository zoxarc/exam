from objects.template import GeneralServer


class TestServer(GeneralServer):
    def __init__(self):
        super(TestServer, self).__init__()

        self.client_message += self.on_client_message
        self.starting += self.on_server_start

    @staticmethod
    def on_client_message(data, **kwargs):
        print(data)

    @staticmethod
    def on_server_start(**kwargs):
        print("server started")


if __name__ == '__main__':
    s = TestServer()
    s.main_loop()
