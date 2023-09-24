# -*- coding:utf-8 -*-
# @Time   : 2022/3/24 13:50
# @Author : tq
# @File   : config.py
import os, sys
import json

from configparser import ConfigParser

from conf.confpath import ConfPath


def json_read(key, file_path):
    """
    读取 key 值
    :param key:
    :return: list
    """
    with open(file_path, 'r') as fp:
        js = json.load(fp)
    return js.get(key)


class Config:
    """ 配置文件的封装 """
    __instance = None

    def __init__(self):
        self.config = ConfigParser()
        if not os.path.exists(ConfPath.CONF_FILE):
            raise FileNotFoundError(f"请确保配置文件存在！！{ConfPath.CONF_FILE}")
        self.load_file()
        self.host_ip = json_read('host_ip', ConfPath.REMOTE_CONFIG_FILE)

        self.vm_name = json_read('vm_name', ConfPath.PATH_CONF)

        # [log]
        self.level = self.get_conf('log', 'LEVEL')

        # [image]
        self.threshold = self.get_conf('image', 'THRESHOLD')

        # [run]
        self.run_flag = self.get_conf('run', 'RUN_FLAG')

        # 邮箱配置
        self.host = self.get_conf('email', 'HOST')
        self.port = self.get_conf('email', 'PORT')
        self.user = self.get_conf('email', 'USER')
        self.pwd = self.get_conf('email', 'PWD')
        self.sender = self.get_conf('email', 'SENDER')
        self.receivers = self.get_conf('email', 'RECEIVERS')
        # [URL]
        self.center_ip = self.get_conf('url', 'center_ip')

        self.center_url = f'http://{self.center_ip}:8080'

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
            return cls.__instance
        return cls.__instance

    @property
    def is_ide(self):
        """
         判断是否 ide 执行
        :return: 0：ide执行； 1：其他执行
        """
        try:
            s = sys.argv[1]
            return 1
        except:
            return 0

    def load_file(self):
        """
        打开配置文件
        :return:
        """
        try:
            self.config.read(ConfPath.CONF_FILE, encoding='UTF-8')
        except Exception as e:
            print("打开配置文件失败！！！")
            raise e

    def get_conf(self, section, option):
        """
        配置文件读取
        :param section:
        :param option:
        :return:
        """
        try:
            param = self.config.get(section, option)
            return param
        except Exception as e:
            print('获取配置文件参数值失败')
            raise e

    def set_conf(self, section, option, value):
        """
        配置文件修改
        :param section: [param]
        :param option: msc_no
        :param value: 1
        :return:
        """
        if not isinstance(value, str):
            value = str(value)
        self.config.set(section, option, value)
        try:
            with open(ConfPath.CONF_FILE, "w+", encoding='utf-8') as fp:
                self.config.write(fp)
        except ImportError as e:
            print("写入配置文件错误！！！")
            raise e

    def run_flag_write(self, text):
        self.set_conf('run', 'RUN_FLAG', text)
        self.run_flag = self.get_conf('run', 'RUN_FLAG')


conf = Config()