# -*- coding:utf-8 -*-
# @Time   : 2022/3/24 14:25
# @Author : tq
# @File   : data_install.py
import os
from utils.sys_info import sys_info

desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
# 主文件目录
hr_files_dir = '/opt/apps/cn.huorong.esm/files'
# DB及隔离区目录
hr_share_dir = os.path.join(hr_files_dir, 'share')
# 应用程序目录
hr_applications_dir = '/opt/apps/cn.huorong.esm/entries/applications'
# 执行目录
hr_program_bin_dir = os.path.join(hr_files_dir, 'bin')


class DataInstall:
    desktop = desktop

    # 下载火绒
    data_down_url = 'http://192.168.3.122/deploy/mac-inst.dmg?type=macos'
    # 下载火绒文件路径
    data_install_desktop = desktop
    # 挂载dmg文件(挂载磁盘镜像)
    data_dmg_mount = 'hdiutil attach /Users/test/Desktop/macOS_inst\(https_192.168.3.122_80\).dmg'
    # 卸载磁盘镜像
    data_dmg_unmount = 'hdiutil detach /Volumes/火绒安全终端/'

    # 拷贝windows共享文件测试
    data_test_file_src = 'd:/AutoTestData/do_not_delete.txt'
    data_test_file_dst = os.path.join(desktop, 'do_not_delete.txt')
    # 打开火绒
    data_open_hr = 'open /Applications/HipsMain.app &'
    # 退出火绒
    data_quit_hr = 'pkill HipsMain &'


