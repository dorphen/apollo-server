from datetime import datetime
from apollo import Client, Response
from apollo.config import Config


def latency_command(client: Client.Client, config: Config.Config, command: str, args: list, msg: Response.Response):
    if command not in config.commands.latency:
        return

    start_time = datetime.now()
    client.send_recv(f"PING {config.nick}")
    end_time = datetime.now()
    ping = round((end_time - start_time).total_seconds() * 1000, 3)
    client.send(f"Pong! Latency: {ping} ms.", msg.reply_channel)
    print(f"Called [{config.command_prefix}ping]")  # fixme log this
