import threading, websocket, json

class MessageHandler(object):
    Message_available = threading.Event()
    NellyResponse = None
    def __init__(self, model, access_token, server):
        websocket.enableTrace(True)
        port = 34596
        print("Connecting to http://{}:{}".format(server, port))

        self.ws  = websocket.WebSocketApp(
            "ws://{}:{}/websocket".format(server, port),
            on_open = self.on_open,
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close,
            on_ping = None,
            on_pong = None,
            keep_running = True,
            header= {"Authorization": "bearer " + access_token}
        )

        print("Connection initialized" + self.ws.__str__())
        wst = threading.Thread(target=self.ws.run_forever, kwargs={'ping_interval': 500, 'ping_timeout': 200})
        wst.daemon = True
        wst.start()


    def sendMessage(self, userMessage):
        json_data = json.dumps(userMessage)
        self.ws.send(json_data)

    def close(self):
        self.ws.close()

    def on_message(self, message):
        self.NellyResponse = json.loads(message)
        self.Message_available.set()

    def on_error(self, error):
        print ("Error occured : " + error + " sessionId is " + self.ws.header['Authorization'].split()[1])

    def on_close(self):
        print("### closed ###" + " sessionId is " + self.ws.header['Authorization'].split()[1])

    def on_open(self):
         print("Connection opened " + self.ws.__str__())
