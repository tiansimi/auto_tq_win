# -*- coding:utf-8 -*-
# @Time   : 2022/3/24 19:00
# @Author : tq
# @File   : cmd_line.py
import os
import time

import allure
from common.log import log


class CmdLine:
    def __init__(self):
        pass

    def command(self, img_info, cmd):
        """ 命令行执行 shell 命令 """
        try:
            result = os.system(cmd)  # 加 start 不阻塞； linux 系统 后面加 &
            with allure.step(f'执行{img_info}命令：{cmd}'):
                if result == 0:
                    log.info(f'执行成功：{cmd}')
                    allure.attach('成功执行', f'{cmd}')
                else:
                    log.error(f'执行失败：{cmd}')
                    allure.attach('执行失败', f'{cmd}')
                assert not result
        except Exception as e:
            raise e

    def command_popen_list(self, cmd):
        """ 命令行执行 shell 命令，返回命令的输出内容 """
        try:
            result = os.popen(cmd)
            return result.readlines()
        except Exception as e:
            raise e

    def command_popen(self, cmd, timeout=18000):
        """ 命令行执行 shell 命令，返回命令的输出内容 """
        import subprocess
        try:
            sp = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            log.info("[PID] %s: %s" % (sp.pid, cmd))
            sp.wait(timeout=timeout)   # 等待子进程结束。设置并返回returncode属性

            if sp.returncode == 0:
                res = [(sp.stderr.read().decode("utf-8")), (sp.stdout.read().decode("utf-8"))]
                return res
            else:
                return False
        except Exception as e:
            raise e

    def command_popen_kill_process_bak(self, cmd):
        """ 命令行执行 shell 命令，返回命令的输出内容 """
        import subprocess
        try:
            sp = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            log.info("[PID] %s: %s" % (sp.pid, cmd))
            time.sleep(5)
            self.kill_process_running('hrconsole')
            res = [(sp.stderr.read().decode("utf-8")), (sp.stdout.read().decode("utf-8"))]
            return res
        except Exception as e:
            raise e

    def command_popen_kill_process(self, cmd):
        """ 命令行执行 shell 命令，返回命令的输出内容 """
        from subprocess import PIPE, Popen
        try:
            sp = Popen(
                cmd,
                stdout=PIPE,
                stderr=PIPE,
                encoding='utf8', errors='ignore'
            )
            log.info("[PID] %s: %s" % (sp.pid, cmd))
            time.sleep(5)
            self.kill_process_running('hrconsole')
            res1 = [(sp.stderr.read()), (sp.stdout.read())]
            # res = [(sp.stderr.read().decode("utf-8")), (sp.stdout.read().decode("utf-8"))]
            return res1
        except Exception as e:
            raise e

    def get_process_info(self, process):
        """ 获取正在运行的进程信息 """
        import subprocess
        pid = subprocess.Popen(["pgrep", "-f", process], stdout=subprocess.PIPE, shell=False)
        response = pid.communicate()[0]
        return response

    def kill_process_running(self, process):
        """
           结束正在运行的进程
           :param process: 进程名
        """
        import re
        res = self.get_process_info(process)
        if res:
            result = None
            for pid_num in re.findall(r"\d+", str(res)):
                result = os.system("sudo kill " + pid_num)
            return result
        else:
            return res


if __name__ == '__main__':
    CmdLine().command('dd', 'dir')