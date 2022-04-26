import logging

from apollo.config import Config
from apollo import Response, Client


def help_command(client: Client.Client, config: Config.Config, command: str, args: list, msg: Response.Response):
    if command not in config.commands.help:
        return

    # \u2514 is an L shaped symbol which indicates a line is continuing from the previous one
    # \u251E is a |- character for a line continuing from the previous one and followed by another connected one
    prefix = config.command_prefix
    help_text = [
        "",
        "<ORANGE><U><B>IRC Brick Help",
        f"<B>{prefix}help<0> See this message",
        f"  \u2514 Aliases: <I>{prefix}brick<0>, <I>{prefix}commands<0>",
        f"<B>{prefix}ping<0> Make sure the bot is online and get an approximate ping/latency",
        f"  \u2514 Aliases: <I>{prefix}pong<0>, <I>{prefix}latency<0>, <I>{prefix}connection<0>, <I>{prefix}delay<0>, <I>{prefix}lag<0>",
        f"<B>{prefix}time<0> Get the current time and the next school session",
        f"  \u2514 Aliases: <I>{prefix}session<0>, <I>{prefix}class<0>, <I>{prefix}timetable<0>, <I>{prefix}next<0>",
        f"<B>{prefix}download <url><0> Download a file (useful when blocked at school)",
        f"  \u251E <B><url><0> A valid url. Make sure it ends in .zip or whatever file type it is!",
        f"  \u2514 Aliases: <I>{prefix}get<0>",
        ""
    ]

    if not msg.is_dm:
        client.send("Sent help in DMs to avoid spamming chat.", msg.reply_channel)
    client.send_multiline(help_text, channel=msg.nick)
    logging.debug(f"\x1b[38;5;{str(config.logging_colours.command)}mCalled [{prefix}help]\x1b[0m")  # fixme colours
