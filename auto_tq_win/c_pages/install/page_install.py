# -*- coding:utf-8 -*-
# @Time   : 2022/3/30 10:33
# @Author : tq
# @File   : page_install.py
import os
import re
import requests
import allure

from common.log import log
from c_pages.base_page import BasePage
from c_datas.data_install import DataInstall
from c_datas.data_shell import DataShell
from c_paths.install.path_install import PathInstall
from utils.cmd_line import CmdLine


class PageInstall(BasePage):
    def __init__(self):
        super(BasePage, self).__init__()
        self.cmd = CmdLine()

    def down_install_file(self, img_info):
        """
        下载安装文件
        :param img_info: 步骤信息
        :param url: 下载 安装文件的接口 url 地址
        :param down_path: 下载路径
        :return:
        """
        r = requests.get(DataInstall.data_down_url, stream=True)
        if r.status_code == 200:
            file_name = re.search('macOS_inst.*dmg', r.headers.get('Content-Disposition')).group()
            install_path = os.path.join(DataInstall.data_install_desktop, file_name)
            with open(install_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: f.write(chunk)
            with allure.step(f'{img_info}'):
                if os.path.exists(install_path):
                    log.info(f'成功下载：{install_path}')
                    allure.attach('下载文件成功', f'{install_path}')
                else:
                    log.error(f'下载失败：{install_path}')
                    allure.attach('下载文件失败', f'{install_path}')
                assert os.path.exists(install_path)
        else:
            raise ValueError(f'相应异常-状态码：{r.status_code}')

    def execute_install_file(self, img_info):
        """ 执行安装程序 """
        self.shell('挂载dmg', f'{DataInstall.data_dmg_mount}')
        self.click_position('双击桌面火绒图标', PathInstall.path_desktop_hr, double=True)
        self.click_position('双击火绒安装', PathInstall.path_inst, double=True)

        self.click_center('点击安装按钮', PathInstall.path_install)

        self.click_position('点击密码框', PathInstall.path_password)
        self.send_text('发送密码', '123456')
        self.click_center('点击安装帮助程序', PathInstall.path_inst_app)
        self.click_center('点击继续', PathInstall.path_continue)
        self.assert_match('等待完成按钮', PathInstall.path_complete, timeout=1)
        self.click_center('点击完成', PathInstall.path_complete)
        self.click_center('点击点按锁按钮以进行更改', PathInstall.path_to_safe)
        self.click_center('点击按锁图标', PathInstall.path_to_unlock)
        self.click_position('点击密码框', PathInstall.path_password)
        self.send_text('发送密码', '123456')
        self.click_center('点击解锁', PathInstall.path_unlock)
        self.click_position('勾选火绒', PathInstall.path_uncheck_hr, x_percent=0.15)
        self.click_center('点击退出并重新打开', PathInstall.path_exit_reopen)
        self.shell('卸载磁盘镜像', f'{DataInstall.data_dmg_unmount}')
        # self.click_center('点击点按锁按钮以进行更改', PathInstall.path_to_safe)

        # self.click_position('点击火绒图标打开火绒', PathInstall.path_desktop_hr)
        self.assert_match('火绒正在保护你的电脑', PathInstall.path_hr_text)
        self.copy('拷贝windows共享测试文件', DataInstall.data_test_file_src, DataInstall.desktop)
        self.assert_files_exist('断言文件存在', DataInstall.data_test_file_dst)
        self.remove('删除测试文件', DataInstall.data_test_file_dst)
        # self.shell('退出火绒', DataInstall.data_quit_hr)
        # self.shell('打开火绒', DataInstall.data_open_hr)
        self.shell('打开Safari浏览器', DataShell.data_open_safari)
        self.shell('关闭Safari浏览器', DataShell.data_kill_safari)
        # self.open_url('https://www.baidu.com')

    def assert_hr_text(self, img_info):
        """ 断言 火绒正在保护您的电脑存在 """
        self.assert_match(img_info, PathInstall.path_hr_text)

    def is_hr_text(self, img_info):
        """ 判断 火绒正在保护您的电脑存在 """
        self.is_match(img_info, PathInstall.path_hr_text, timeout=5)

    def install_after_check(self):
        """ 安装后基础文件验证 """
        try:
            # 本地文件夹
            # self.share.assert_files_exist('断言 文件目录-病毒库目录存在', DataInstall.data_files_virdb_files)   # 2.0.1.0安装后无此文件
            self.assert_files_exist('断言 应用程序目录-启动项文件存在', DataInstall.data_applications_desktop_files)
            self.assert_files_exist('断言 火绒安全终端托盘程序开机自启动文件存在', DataInstall.data_applications_desktop_files_etc)
            self.assert_files_exist('断言 火绒安全终端快捷方式文件存在', DataInstall.data_applications_desktop_files_usr)
            self.assert_files_exist('断言 应用程序目录-图标文件存在', DataInstall.data_hr_icons_files)
            self.assert_files_exist('断言 程序目录-bin程序文件存在', DataInstall.data_bin_files)
            self.assert_files_exist('断言 程序目录-图片样式相关插件库目录存在', DataInstall.data_bin_imageformats_files)
            self.assert_files_exist('断言 程序目录-输入法相关插件库目录存在', DataInstall.data_bin_forminput_files)
            self.assert_files_exist('断言 程序目录-平台相关插件库存在', DataInstall.data_bin_platforms_files)
            self.assert_files_exist('断言 配置文件目录-配置文件存在', DataInstall.data_files_etc_files)
            self.assert_files_exist('断言 依赖库目录-lib文件存在', DataInstall.data_files_lib_files)
            self.assert_files_exist('断言 脚本文件目录-脚本文件存在', DataInstall.data_files_script_files)
            self.assert_files_exist('断言 公共目录-DB及隔离区等文件存在', DataInstall.data_share_files)
            self.assert_files_exist('断言 公共目录-字体文件存在', DataInstall.data_share_fonts_files)
            self.assert_files_exist('断言 公共目录-安装文件存在', DataInstall.data_share_inst_files)
            self.assert_files_exist('断言 公共目录-隔离区文件夹存在', DataInstall.data_share_quarantine_files)
            # self.assert_files_exist('断言 公共目录-查杀日志目录存在', DataInstall.data_share_scanlog_files)   # 查杀过程中会变化
            self.assert_files_exist('断言 公共目录-病毒库目录存在', DataInstall.data_share_virdb_files)
            self.assert_files_exist('断言 公共目录-xsse引擎目录存在', DataInstall.data_share_xsse_files)
            # self.assert_files_exist('断言 文件目录-xsse引擎虚拟机目录存在', DataInstall.data_files_xsse_files)  # 2.0.1.0安装后无此文件
            self.assert_files_exist('断言 文件目录-火绒版本文件存在', DataInstall.data_hr_version_file)
            self.assert_files_exist('断言 火绒基本信息文件存在', DataInstall.data_hr_info_file)
            # self.assert_files_exist('断言 服务文件hipsdaemon.service存在', DataInstall.system_hipsdaemon_service) # 2.0.1.0安装后无此文件
            self.assert_files_exist('断言 服务文件hressclnt.service存在', DataInstall.data_system_hressclnt_service)
            # self.assert_files_exist('断言 服务文件hipsdaemon.service软链接文件存在', DataInstall.multi_user_hipsdaemon_service) # 2.0.1.0安装后无此文件
            self.assert_files_exist('断言 服务文件hressclnt.service软链接文件存在', DataInstall.data_multi_user_hressclnt_service)
            # 启动项
            self.assert_files_exist('断言 启动项文件存在', DataInstall.data_auto_start_files)
            # 进程验证
            self.assert_files_exist('断言 进程文件存在', DataInstall.data_hr_client_files)
            self.assert_process_running_linux('断言 正在运行的进程存在', 'hrclient')
            self.assert_process_running_linux('断言 正在运行的进程存在', 'hipsmain')
            self.assert_process_running_linux('断言 正在运行的进程存在', 'hipsdaemon')
        finally:
            self.open_huorong('打开火绒')


if __name__ == '__main__':
    PageInstall().down_install_file('下载')