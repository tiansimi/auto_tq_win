# -*- coding:utf-8 -*-
# @Time   : 2022/3/30 15:07
# @Author : tq
# @File   : path_install.py
import os
from conf.confpath import ConfPath


class PathInstall:
    # 火绒桌面图标
    path_desktop_hr = os.path.join(ConfPath.PATH_DIR, r'install/path_install/desktop_hr.png')
    # 火绒安装图标
    path_inst = os.path.join(ConfPath.PATH_DIR, r'install/path_install/inst.png')
    # 安装按钮
    path_install = os.path.join(ConfPath.PATH_DIR, r'install/path_install/install.png')
    # 密码（输入框定位）
    path_password = os.path.join(ConfPath.PATH_DIR, r'install/path_install/password.png')
    # 安装帮助程序按钮
    path_inst_app = os.path.join(ConfPath.PATH_DIR, r'install/path_install/inst_app.png')
    # 继续按钮
    path_continue = os.path.join(ConfPath.PATH_DIR, r'install/path_install/continue.png')
    # 完成按钮
    path_complete = os.path.join(ConfPath.PATH_DIR, r'install/path_install/complete.png')
    # 前往安全与隐私按钮
    path_to_safe = os.path.join(ConfPath.PATH_DIR, r'install/path_install/to_safe.png')
    # 点击点按锁按钮以进行更改
    path_to_unlock = os.path.join(ConfPath.PATH_DIR, r'install/path_install/to_unlock.png')
    # 点击解锁
    path_unlock = os.path.join(ConfPath.PATH_DIR, r'install/path_install/unlock.png')
    # 点击勾选火绒
    path_uncheck_hr = os.path.join(ConfPath.PATH_DIR, r'install/path_install/uncheck_hr.png')
    # 点击退出并重新打开
    path_exit_reopen = os.path.join(ConfPath.PATH_DIR, r'install/path_install/exit_reopen.png')

    # 火绒正在保护您的电脑
    path_hr_text = os.path.join(ConfPath.PATH_DIR, r'install/path_install/hr_text.png')



