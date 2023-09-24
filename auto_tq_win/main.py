# -*- coding:utf-8 -*-
# @Time   : 2022/3/25 18:25
# @Author : tq
# @File   : main.py
import os

from conf.config import conf
from conf.confpath import ConfPath
from common.report import Report
from common.log import log
from utils.request import send_info
from utils.file import fo


def run():
    if conf.is_ide == 0:
        # args = ['./c_cases', '--alluredir', ConfPath.RESULT_LOC_DIR, '--clean-alluredir']
        args = ['-k', 'hr_install_normal', '--alluredir', ConfPath.RESULT_LOC_DIR, '--clean-alluredir']
        Report().run(args, send=False)  # 发送测试报告
    else:
        branch = fo.json_read('branch', ConfPath.REMOTE_CONFIG_FILE).strip()
        case = fo.json_read('case', ConfPath.REMOTE_CONFIG_FILE).strip()
        if case and branch == 'dev':
            args = ['-k', f'hr_install_normal or {case}', '--alluredir', ConfPath.RESULT_LOC_DIR, '--clean-alluredir']
            Report().run(args, send=True)  # 发送测试报告.CLIENT_ID
        else:
            level_list = []
            level_critical = fo.json_read('level_critical', ConfPath.REMOTE_CONFIG_FILE).strip()
            level_normal = fo.json_read('level_normal', ConfPath.REMOTE_CONFIG_FILE).strip()
            level_minor = fo.json_read('level_minor', ConfPath.REMOTE_CONFIG_FILE).strip()
            if level_critical == '1': level_list.append('critical')
            if level_normal == '1': level_list.append('normal')
            if level_minor == '1': level_list.append('minor')
            level = '--allure-severities=' + ','.join(level_list)
            log.info(f'{level}')
            if level:
                args = ['./c_cases', '--alluredir', ConfPath.RESULT_LOC_DIR, level, '--clean-alluredir']
                Report().run(args, send=True)  # 发送测试报告
            else:
                raise ValueError('用例级别最少要选择一个！')

        send_info(r'finish')
        # os.system("sudo shutdown -h now")


if __name__ == '__main__':
    run()
    # r = input('\n')
