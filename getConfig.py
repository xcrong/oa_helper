import configparser
import os

config = configparser.ConfigParser()
config.read("config.ini")


# sender
account = config["sender"]["account"]
if account.startswith("$"):
    account = os.getenv(account.lstrip("$"))
password = config["sender"]["password"]
if password.startswith("$"):
    password = os.getenv(password.lstrip("$"))
smtp_server = config["sender"]["smtp_server"]
smtp_port = eval(config["sender"]["smtp_port"])

# receiver_list
receiver_list = eval(config["receiver"]["account"])

# schedule
startTime = eval(config["schedule"]["startTime"])
endTime = eval(config["schedule"]["endTime"])
interval = int(eval(config["schedule"]["interval"]))

if (startTime >= endTime):
    startTime = 8
    endTime = 18
if (interval <= 0) or (interval >= 11*60):
    interval = 60




