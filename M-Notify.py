import requests
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
import time
import os

def read_file_lines(file_path):
    with open(file_path, 'r') as file:
        one = file.readline().strip()
        two = file.readline().strip()
        three = file.readline().strip()
        return one, two, three

print('歡迎使用天堂M小工具')

config_path = r".\line-notify-config.txt"
token, log_numbers, refresh_cadence_in_seconds = read_file_lines(config_path)

log_modification_times = {}

while True:
    for log_number in log_numbers.split(','):
        log_path =r'.\{}.log'.format(log_number)
        current_modification_time = int(os.stat(log_path).st_mtime)
        if log_number in log_modification_times:
            last_modification_time = log_modification_times[log_number]
            if current_modification_time > last_modification_time:
                log_modification_times[log_number] = current_modification_time
                with open(log_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    last_line = '[Log {}] '.format(log_number) + lines[-2][1:].strip()
                    try:
                        message = last_line
                        headers = { "Authorization": "Bearer " + token }
                        data = { 'message':message }
                        requests.post(("https://notify-api.line.me/api/notify", headers = headers, data = data
                        print(last_line)
                    except LineBotApiError as e:
                        # error handle
                        print('line的設置可能有問題')
                        print(e)
        else:
            log_modification_times[log_number] = current_modification_time
    time.sleep(int(refresh_cadence_in_seconds))
