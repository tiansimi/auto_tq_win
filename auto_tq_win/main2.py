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


def run2():
    # args = ['./c_cases', '--alluredir', ConfPath.RESULT_LOC_DIR, '--clean-alluredir']
    args = ['-k', 'hr_full_multiple_files_part_clean', '--alluredir', ConfPath.RESULT_LOC_DIR, '--clean-alluredir']
    Report().run(args, send=False)  # 发送测试报告


if __name__ == '__main__':
    run2()
    # r = input('\n')
