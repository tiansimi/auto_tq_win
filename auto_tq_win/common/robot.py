# -*- coding:utf-8 -*-
# @Time   : 2022/3/24 16:49
# @Author : tq
# @File   : robot.py
import requests


def reports_robot(msg_info):
    # url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=52999afb-ee01-456c-9ba7-a0f1ae9cadf4'
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=52999afb-ee01-456c-9ba7-a0f1ae9cadf4'
    headers = {"Content-Type": "text/plain"}
    data = {
        "msgtype": "text",
        "text": {
            "content": msg_info,
        }
    }

    resp = requests.post(url=url, headers=headers, json=data)
    print(resp.text)


if __name__ == '__main__':
    reports_robot('rrrrrr')