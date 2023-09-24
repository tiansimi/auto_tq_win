# -*- coding:utf-8 -*-
# @Time   : 2022/3/30 15:08
# @Author : tq
# @File   : hr_install.py
import time
import allure

from c_datas.data_install import DataInstall
from common.report import report_show
from c_pages.install.page_install import PageInstall
from utils.sys_info import sys_info


@allure.epic('终端安装')
@allure.feature('终端安装')
class HrInstall:
    def setup_class(self):
        self.install = PageInstall()

    @allure.severity(allure.severity_level.CRITICAL)
    def hr_install_normal(self):
        report_show('软件安装', '正常安装')
        self.install.down_install_file('下载安装文件')
        self.install.execute_install_file('执行安装')
        time.sleep(3)
