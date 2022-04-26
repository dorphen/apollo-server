import socket
import logging

from apollo.config import Config
from apollo import Response


class Client:
    irc_socket: socket.socket = None

    def __init__(self, config: Config.Config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.is_connected = False

        self.command_handlers = []  # list of functions registered for on_command event

    def connect(self):
        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc_socket.connect((self.config.server_host, self.config.port))

        self.send_raw(f"USER {self.config.nick} {self.config.nick} {self.config.nick} {self.config.nick}")
        self.send_raw(f"NICK {self.config.nick}")

        self.is_connected = True
        self.on_connect()

    def run(self):
        if not self.is_connected:
            self.connect()

        self.send_raw(f"JOIN {self.config.channel}")
        self.logger.info("Joining channel")
        response = ""
        while "366" not in response:
            response = self.recv_raw()
            for line in response.split("\n"):
                if self.logger.getEffectiveLevel() == logging.DEBUG:
                    self.logger.debug(line)
                else:
                    self.logger.info(line.split(" ", 1)[1])  # todo prettify
        self.logger.info("Done!")
        self.on_join()

        # main loop
        while True:
            response = Response.Response(self.config, self.recv_raw())

            if response.is_ping:
                self.send_raw("PONG :pingis")
                self.on_ping()
            if response.is_command:
                for handler in self.command_handlers:
                    handler(self, self.config, response.brick_command, response.params[1].split()[1:], response)
            if response.is_privmsg:
                self.on_privmsg(response)

    def send_raw(self, content: str):
        if not content.endswith("\n"):
            content += "\n"  # todo test
        self.irc_socket.send(bytes(content, "UTF-8"))

    def send(self, message: str, channel: str, colour: int = None):
        colour_str = ""
        if colour is not None:
            try:
                if 0 >= colour >= 15 and colour != 99:
                    raise ValueError  # todo errorhandling
                if len(str(colour)) == 0:
                    colour_str = f"\u00030{colour}"
                else:
                    colour_str = f"\u0003{colour}"
            except ValueError:
                pass
        self.send_raw(f"PRIVMSG {channel} :{colour_str}{message}")

    def send_multiline(self, message: list[str], channel: str):
        for line in message:  # type: str
            # line = self.format_msg(line)  # fixme
            self.send(line, channel)

    def send_recv(self, message):
        self.send_raw(message)
        return self.recv_raw()

    def recv_raw(self):
        response = self.irc_socket.recv(2048).decode("UTF-8")
        response = response.strip("\n\r")
        return response

    def add_command_handler(self, func):
        self.command_handlers.append(func)  # todo validate handler

    def event(self, func):
        """
        event names:
         - on_connect
         - on_join
         - on_ping
         - on_privmsg(msg)
         - on_command(client, config, command: str, args: list, msg)
        :param func:
        :return:
        """
        if func.__name__ == "on_command":
            self.add_command_handler(func)
        else:
            setattr(self, func.__name__, func)

    def on_connect(self):
        pass

    def on_join(self):
        pass

    def on_ping(self):
        pass

    def on_privmsg(self, msg: Response.Response):
        pass
