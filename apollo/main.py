import logging

from apollo import Client, Response, commands
from apollo.config import Config
from apollo.commands import help, latency, time, download


def main():
    config = Config.Config()
    print(f"Logging with level {config.logging_level}")

    logging.basicConfig(level=config.logging_level,
                        format="%(asctime)s %(name)s %(levelname)s\t%(message)s",
                        datefmt="[%y.%m.%d %H:%M:%S]")
    logging.info("Starting Apollo IRC")

    client = Client.Client(config)

    @client.event
    def on_ping():
        client.logger.debug("Ping!")

    @client.event
    def on_privmsg(msg: Response.Response):
        client.logger.info(f"{msg.channel} {msg.nick}: {msg.content}")

    client.add_command_handler(commands.help.help_command)
    client.add_command_handler(commands.latency.latency_command)
    client.add_command_handler(commands.time.time_command)
    client.add_command_handler(commands.download.download_command)

    client.run()


if __name__ == "__main__":
    main()
