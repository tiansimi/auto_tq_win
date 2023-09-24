# -*- coding:utf-8 -*-
# @Time   : 2022/3/24 17:11
# @Author : tq
# @File   : request.py
import requests

from conf.config import conf
from common.log import log


def send_info(info):
    """ 发送日志信息 """
    if conf.is_ide != 0:
        host = conf.host_ip
        vm_name = conf.vm_name
        all_url = host+'/send_info/'+vm_name+':'+info.replace("/", "-")
        try:
            resp = requests.get(all_url)
            if resp.json().get("code") == 0:
                log.info(f'成功发送请求get请求：{all_url}')
            else:
                log.error(f'成功发送请求，返回结果：{resp.json()}')
            return resp.json()
        except Exception as e:
            log.error(f'发送get请求失败.{e}{all_url}')
            return {}


def create_snapshot(snapshot):
    """ 创建快照 """
    if conf.is_ide != 0:
        host = conf.host_ip
        vm_name = conf.vm_name
        url = host + '/create_snapshot'
        data = {'windows': vm_name, 'snapshot': snapshot}
        try:
            resp = requests.post(url, json=data)
            log.info(f'{resp.text}')
            send_info(f'{resp.text}')
            return resp.json()
        except Exception as e:
            log.error(f'create_snapshot接口请求出错:{e},url:{url},data:{data}')
            return {}

