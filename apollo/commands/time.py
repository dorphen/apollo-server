from datetime import datetime, timedelta
from apollo import Client, Response
from apollo.config import Config


def time_to(time_str: str, time_format: str):
    now = datetime.now()
    time = datetime.strptime(time_str, time_format)
    next_occurrence = now.replace(hour=time.hour, minute=time.minute)
    while next_occurrence <= now:
        next_occurrence += timedelta(days=1)
    return next_occurrence - now


def time_command(client: Client.Client, config: Config.Config, command: str, args: list, msg: Response.Response):
    if command not in config.commands.time:
        return

    times = config.time_times

    times_to_sessions: dict[str, timedelta] = {
        "pastoral": time_to(times.pastoral, times.format),
        "session_1": time_to(times.session_1, times.format),
        "session_2": time_to(times.session_2, times.format),
        "session_3": time_to(times.session_3, times.format),
        "session_4": time_to(times.session_4, times.format),
        "session_5": time_to(times.session_5, times.format),
        "session_6": time_to(times.session_6, times.format)
    }

    next_session = min(times_to_sessions, key=times_to_sessions.get)

    client.send(f"It's {datetime.now().strftime('%I:%M %p').lstrip('0')}. {next_session.replace('_', ' ').capitalize()}"
                f" starts at {datetime.strptime(getattr(times, next_session), times.format).strftime('%I:%M %p').lstrip('0')} "
                f"({times_to_sessions[next_session].seconds//3600} hours and "
                f"{(times_to_sessions[next_session].seconds//60)%60} minutes).", msg.reply_channel)  # todo colours
    print(f"Called [{config.command_prefix}time]")  # fixme log this
