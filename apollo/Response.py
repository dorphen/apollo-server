import re
from datetime import datetime
from apollo.config import Config


class Response:
    raw: str = None
    sent_time: datetime = None

    tags: str = None
    nick: str = None
    user: str = None
    host: str = None
    command: str = None
    params: list[str] = None

    is_privmsg: bool = None
    channel: str = None
    content: str = None
    reply_channel: str = None

    is_command: bool = False
    brick_command: str = None

    is_ping: bool = False
    is_dm: bool = False

    def __init__(self, config: Config.Config, raw: str):
        self.raw = raw
        self.sent_time = datetime.now()

        if raw.startswith("@"):
            self.tags = raw.split(" ", 1)[0]
            raw = raw.split(" ", 1)[1]

        if raw.startswith(":"):
            address = raw.removeprefix(":").split(" ", 1)[0]
            self.nick = re.split("[!@]", address, 1)[0]

            address = address.split(self.nick[-1], 1)[1]
            if address.startswith("!"):
                self.user = address.removeprefix("!").split("@", 1)[0]

            if len(address.split("@", 1)) == 2:
                self.host = address.split("@", 1)[1]

            raw = raw.split(" ", 1)[1]

        self.command = raw.split(" ", 1)[0]

        self.params = []
        if len(raw.split(" ")) <= 1:
            self.params.append(raw)
        else:
            raw = raw.split(" ", 1)[1]
            while True:
                param = raw.split(" ", 1)[0]
                if param.startswith(":"):
                    self.params.append(raw.removeprefix(":"))
                    break
                else:
                    self.params.append(param)
                    if len(raw.split(" ", 1)) <= 1:
                        self.params.append(raw)
                        break
                    else:
                        raw = raw.split(" ", 1)[1]

        if self.command == "PING":
            self.is_ping = True
        elif self.command == "PRIVMSG":
            self.is_privmsg = True
            self.channel = self.params[0]
            if self.channel.startswith("#"):
                self.reply_channel = self.channel
            else:
                self.is_dm = True
                self.reply_channel = self.nick

            self.content = self.params[1]
            if self.content.startswith(config.command_prefix):
                self.is_command = True
                self.brick_command = self.content.removeprefix(config.command_prefix).split(" ", 1)[0].lower()

