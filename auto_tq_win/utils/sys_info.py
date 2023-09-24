# -*- coding:utf-8 -*-
# @Time   : 2022/3/24 16:57
# @Author : tq
# @File   : sys_info.py
import os
import sys
import locale
import re
import socket
import platform
import subprocess
import psutil

class SysInfo:
    def __init__(self):
        if platform.system() == 'Windows':
            import wmi
            self.c = wmi.WMI()

    @property
    def host_ip(self):
        """ 查询本机ip地址 """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    @property
    def system_name(self):
        """ 查询本机name """
        return socket.gethostname()

    @property
    def system_version(self) -> str:
        """ 返回 系统版本 如：
        Windows-10-10.0.19041-SP0
        Linux-4.15.0-29-generic-x86_64-with-Ubuntu-18.04-bionic
        Linux-4.19.0-desktop-amd64-x86_64-with-uos-20-eagle
        """
        return platform.platform()  # Linux-4.15.0-29-generic-x86_64-with-Ubuntu-18.04-bionic'

    @property
    def system_type(self) -> str:
        """ 返回 系统版本 如：Windows/Linux"""
        # return sys.platform  # windows: win32  linux： linux
        return platform.system()

    @property
    def system_lang(self) -> tuple:
        """ 返回 系统语言
        如：Linux中文 返回 ('zh_CN', 'UTF-8')
           Windows 返回 ('zh_CN', 'cp936')
        """
        lang = locale.getdefaultlocale()
        return lang

    @property
    def system_bit(self) -> str:
        """ 返回 系统位数 如：64bit 或 32bit """
        return platform.architecture()[0]

    def get_process_running(self, process):
        """
        获取正在运行的进程
        :param process: 进程名 或 进程列表
        :return: (长度, 进程名或进程列表)
        """
        if platform.system() == 'Windows':
            process_list = []
            if isinstance(process, str):
                for pro in self.c.Win32_Process(name=process):
                    process_list.append(pro.Name)
                    return list(set(process_list))
            if isinstance(process, (list, tuple)):
                for pro in process:
                    for p in self.c.Win32_Process(name=pro):
                        process_list.append(p.Name)
                return list(set(process_list))
            return []

    def get_process_info(self, process):
        """ 获取正在运行的进程信息 """
        pid = subprocess.Popen(["pgrep", "-f", process], stdout=subprocess.PIPE, shell=False)
        response = pid.communicate()[0]
        return response

    def get_process_running_linux(self, process):
        """
        获取正在运行的进程
        :param process: 进程名
        :return: 进程名称
        """
        process_list = []
        if platform.system() == 'Linux':
            try:
                res = self.get_process_info(process)
                if res:
                    pid_num = re.findall(r"\d+", str(res))[0]
                    pid_name = psutil.Process(int(pid_num)).name()
                    process_list.append(pid_name)
                    return list(set(process_list))
                else:
                    return []
            except Exception as e:
                return []

    def kill_process_running(self, process):
        """
           结束正在运行的进程
           :param process: 进程名
        """
        if platform.system() == 'Linux':
            res = self.get_process_info(process)
            if res:
                pid_num = re.findall(r"\d+", str(res))[0]
                result = os.system("sudo kill " + pid_num)
                return result
            else:
                return res

    def get_process_startup(self, process):
        """
        获取自启动中进程
        :param process:
        :return:
        """
        if platform.system() == 'Windows':
            process_list = []
            if isinstance(process, str):
                for pro in self.c.Win32_StartupCommand():
                    if process in pro.Command:
                        process_list.append(process)
                        return process_list
            if isinstance(process, (list, tuple)):
                for p in process:
                    for pro in self.c.Win32_StartupCommand():
                        if p in pro.Command:
                            process_list.append(p)
                            return process_list
            return []

    def get_driver_running(self, drivers):
        """
        获取正在运行的驱动
        :param drivers: 驱动名 或 驱动列表
        :return: (长度, 进程名或进程列表)
        """
        if platform.system() == 'Windows':
            driver_list = []
            if isinstance(drivers, str):
                for driver in self.c.Win32_SystemDriver(State='Running', Name=re.split('[_.]', drivers)[0]):
                    if drivers in driver.PathName:
                        driver_list.append(drivers)
                    return driver_list
            if isinstance(drivers, (list, tuple)):
                for d in drivers:
                    for driver in self.c.Win32_SystemDriver(State='Running', Name=re.split('[_.]', d)[0]):
                        if d in driver.PathName:
                            driver_list.append(d)
                return driver_list
            return []


sys_info = SysInfo()
