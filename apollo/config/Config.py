import os
import cerberus
import yaml
import json
from datetime import datetime


def validate_config(config):
    with open(os.path.join(os.path.dirname(__file__), "schema.json"), "r") as file:
        try:
            schema = json.load(file)
        except json.JSONDecodeError as exception:
            raise exception  # todo errorhandling
    v = cerberus.Validator(schema)
    v.validate(config, schema)
    print(f"Config errors: {v.errors}")


class Config:

    class LoggingColours:
        def __init__(self, colours: dict):
            self.message = colours["message"]
            self.private_message = colours["private_message"]
            self.command = colours["command"]

    class Commands:
        def __init__(self, commands: dict):
            self.help = set(commands["help"])
            self.latency = set(commands["latency"])
            self.time = set(commands["time"])
            self.download = set(commands["download"])

    class TimeTimes:
        def __init__(self, times: dict):
            self.format = times["format"]  # todo validation
            self.pastoral = times["pastoral"]  # todo validation
            self.session_1 = times["session_1"]
            self.session_2 = times["session_2"]
            self.session_3 = times["session_3"]
            self.session_4 = times["session_4"]
            self.session_5 = times["session_5"]
            self.session_6 = times["session_6"]

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "..", "..", "config.yml"), "r") as file:
            try:
                config = yaml.safe_load(file)
            except yaml.YAMLError as exception:
                raise exception  # todo errorhandling

        validate_config(config)

        try:
            self.nick = config["bot.nickname"]
            self.server_host = config["server.hostname"]
            self.port = config["server.port"]
            self.channel = "#" + config["channel"]

            self.logging_level = config["logging.level"]
            self.logging_colours = Config.LoggingColours(config["logging.colours"])
            self.command_prefix = config["commands.prefix"]
            self.commands = Config.Commands(config["commands"])

            self.dev_nick = config["dev_nick"]

            self.time_times = Config.TimeTimes(config["commands.time.times"])

        except KeyError as exception:
            raise exception  # todo errorhandling
