from apollo import Client, Response
from apollo.config import Config
import threading
from urllib import request, error


def download_command(client: Client.Client, config: Config.Config, command: str, args: list, msg: Response.Response):
    print(f"Called [!download]")  # todo logging
    if len(args) < 1:
        client.send("Missing argument!", msg.reply_channel)
        return

    url = "%20".join(args)
    if not url.startswith("http://") or url.startswith("https://"):
        client.send(f"Didn't detect valid URL schema (HTTP or HTTPS). Changed to http://{url}", msg.reply_channel)
        url = "http://" + url
    else:
        client.send(f"Attempting to download {url}", msg.reply_channel)

    thread = threading.Thread(target=get, args=(client, url, msg))
    thread.start()


def get(client: Client.Client, url: str, msg: Response.Response):
    try:
        client.send("Starting download...", msg.reply_channel)
        filepath, response = request.urlretrieve(url)
    except error.URLError:
        client.send("Invalid Download URL!", msg.reply_channel)
        return

    with open(filepath, "r") as file:
        content = file.readlines()
        client.send_multiline(content, msg.reply_channel)

    return
