# -*- coding:utf-8 -*-
# @Time   : 2022/3/24 13:51
# @Author : tq
# @File   : confpath.py
import os
from utils.sys_info import sys_info

desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
# if sys_info.system_type == 'Linux' and 'zh_CN' in sys_info.system_lang:
#     desktop = os.path.join(os.path.expanduser('~'), '桌面')
# desktop = '/Users/test/Desktop'


class ConfPath:
    # 桌面路径
    DESKTOP_DIR = desktop

    # 工程根目录 D:\HR\HR_ui_cs
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 测试用例目录
    CASE_DIR = os.path.join(BASE_DIR, 'c_cases')
    # page 对象目录
    PAGE_DIR = os.path.join(BASE_DIR, 'c_pages')
    # 路径目录
    PATH_DIR = os.path.join(BASE_DIR, 'c_paths')

    # 配置文件目录
    CONF_DIR = os.path.join(BASE_DIR, 'conf')
    # 配置文件
    CONF_FILE = os.path.join(BASE_DIR, 'conf/config.ini')

    # log 文件目录
    LOG_DIR = os.path.join(BASE_DIR, 'logs')

    # libs 目录
    LIB_DIR = os.path.join(BASE_DIR, 'libs')

    # 测试报告 本地目录
    REPORT_LOC_DIR = os.path.join(BASE_DIR, 'reports')
    # 测试结果 本地保存路径
    RESULT_LOC_DIR = os.path.join(REPORT_LOC_DIR, 'result')

    # DB库拷贝出的路径
    DB_DIR = os.path.join(desktop, 'db')
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    # 本地配置文件
    PATH_CONF = r'/Users/test/softs/conf_local.json'
    # 测试报告 远程目录
    REPORT_REMOTE_DIR = '/Users/test/ui_ess20_mac'
    REPORT_REMOTE_URL = 'http://192.168.3.194:8088/ui_ess20_mac'
    if os.path.exists('/Users/test/ui_ess20_mac/share/git_dev.py'):
        REPORT_REMOTE_DIR = '/Users/test/ui_ess20_mac_dev'
        REPORT_REMOTE_URL = r'http://192.168.3.194:8088/ui_ess20_mac_dev'
    REMOTE_CONFIG_FILE = r'/Users/test/ui_ess20_mac/share/conf.json'

    # 中心文件路径
    PATH_SRC = r'/Users/test/ui_ess20_linux/share/安装文件'


class ConfParams:
    # cookies 变量
    COOKIES = {}
    # headers 变量
    HEADERS = {}
    # 终端服务器ID 变量
    CLIENT_ID = ''


class ConfSystemType:
    desktop_list = ['Linux-4.19.0-desktop-amd64-x86_64-with-uos-20-eagle',
                    'Linux-4.15.0-29-generic-x86_64-with-Ubuntu-18.04-bionic',
                    'Linux-5.4.18-35-generic-x86_64-with-glibc2.29',
                    'Linux-4.15.0-188-generic-x86_64-with-Ubuntu-18.04-bionic',
                    'Linux-4.15.0-189-generic-x86_64-with-Ubuntu-18.04-bionic']  # 添加临时机器：Linux-4.15.0-189-generic-x86_64-with-Ubuntu-18.04-bionic

    server_list = ['Linux-4.19.0-server-amd64-x86_64-with-uos-20-fou',
                   'Linux-3.10.0-1160.el7.x86_64-x86_64-with-centos-7.9.2009-Core']

    if sys_info.system_version in desktop_list:
        system_type = 'desktop'  # 不跳过
    else:
        system_type = 'server'
