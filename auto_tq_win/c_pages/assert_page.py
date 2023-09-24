# -*- coding:utf-8 -*-
# @Time   : 2022/4/22 10:21
# @Author : tq
# @File   : assert_page.py
import os
import re
import time

import allure

from conf.confpath import ConfPath
from common.log import log
from utils.file import fo

from utils.sys_info import sys_info


class AssertPage:

    def __init__(self):
        self.desktop = ConfPath.DESKTOP_DIR

    def assert_file_count(self, dir_path, expect: int):
        """
        获取某个目录下，文件数量
        :param dir_path: 目录路径。也可以写目录全路径
        :param expect: 期望结果，文件的数量
        :return:
        """
        if not os.path.isabs(dir_path):
            dir_path = os.path.join(self.desktop, dir_path)

        if not os.path.isdir(dir_path):
            raise ValueError('不是一个合法的目录路径')

        count = len(os.listdir(dir_path))  # 计算目录下文件数量

        with allure.step('断言文件数量'):
            if count == expect:
                log.info(f'断言文件数量成功 - 期望文件数量：{expect}实际文件数量：{count}-目录路径：{dir_path}')
                allure.attach('成功', f'断言文件数量成功 - 期望文件数量：{expect}实际文件数量：{count}-目录路径：{dir_path}')
            else:
                log.error(f'断言文件数量失败 - 期望文件数量：{expect}实际文件数量：{count}-目录路径：{dir_path}')
                allure.attach('失败', f'断言文件数量失败 - 期望文件数量：{expect}实际文件数量：{count}-目录路径：{dir_path}')
            assert count == expect

    def assert_file_size(self, file_path, expect):
        """
        获取文件或文件夹大小
        :param file_path: 直接写文件名，默认指桌面的文件。也可以写文件全路径
        :param expect: 期望结果，文件的大小字节数
        :return:
        """
        size = 0
        if ':' not in file_path:
            file_path = os.path.join(self.desktop, file_path)
        if not os.path.exists(file_path):
            raise ValueError('不是一个合法的文件或文件夹路径')

        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
        if os.path.isdir(file_path):
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    size += os.path.getsize(os.path.join(root, file))

        with allure.step(f'断言文件大小'):
            if size >= expect:
                log.info(f'断言文件或文件夹大小成功 - 期望文件大小：{expect}，实际文件大小：{size}-文件路径：{file_path}')
                allure.attach('成功', f'断言文件大小成功 - 期望文件大小：{expect}，实际文件大小：{size}-文件路径：{file_path}')
            else:
                log.error(f'断言文件或文件夹大小失败 - 期望文件大小：{expect}，实际文件大小：{size}-文件路径：{file_path}')
                allure.attach('失败', f'断言文件大小失败 - 期望文件大小：{expect}，实际文件大小：{size}-文件路径：{file_path}')
            assert size >= expect

    # def assert_files_exist(self, img_info, files, exist=True, extend=()):
    #     """
    #     断言 一个或多个 文件或目录是否存在
    #     :param img_info:
    #     :param files: (r'virdb\hwl.db', r'virdb\prop.db', r'virdb\pset.db', r'virdb\troj.db',)
    #     :param exist: False 断言文件或目录不存在
    #     :param extend: 排除判断的文件或文件夹
    #     """
    #     if isinstance(files, (tuple, list)):
    #         with allure.step(f'断言 {img_info}: {len(files)} 个文件是否存在'):
    #             for file in files:
    #                 if file not in extend:
    #                     result = fo.is_exist_path(file)
    #                     if exist:
    #                         if result:
    #                             log.debug(f'断言成功 文件存在，文件为：{file}')
    #                         else:
    #                             log.error(f'断言失败 文件不存在，文件为：{file}')
    #                         assert result
    #                     else:
    #                         if not result:
    #                             log.debug(f'断言成功 文件不存在，文件为：{file}')
    #                         else:
    #                             log.error(f'断言失败 文件存在，文件为：{file}')
    #                         assert not result
    #         if exist:
    #             log.info(f'断言成功 {img_info}: {len(files)} 个文件或文件夹存在')
    #         else:
    #             log.info(f'断言成功 {img_info}: {len(files)} 个文件或文件夹不存在')
    #     if isinstance(files, str):
    #         with allure.step(f'断言 {img_info}: 1 个文件是否存在'):
    #             if files not in extend:
    #                 result = fo.is_exist_path(files)
    #                 if exist:
    #                     if result:
    #                         log.debug(f'断言成功 文件存在，文件为：{files}')
    #                     else:
    #                         log.error(f'断言失败 文件不存在，文件为：{files}')
    #                     assert result
    #                 else:
    #                     if not result:
    #                         log.debug(f'断言成功 文件不存在，文件为：{files}')
    #                     else:
    #                         log.error(f'断言失败 文件存在，文件为：{files}')
    #                     assert not result
    #         if exist:
    #             log.info(f'断言成功 {img_info}: 1 个文件或文件夹存在')
    #         else:
    #             log.info(f'断言成功 {img_info}: 1 个文件或文件夹不存在')

    def assert_files_exist_bak1(self, img_info, files, exist=True, timeout=15, sleep_time=1, extend=()):
        """
            断言 一个或多个 文件或目录是否存在
            :param img_info:
            :param files: (r'virdb\\hwl.db', r'virdb\\prop.db', r'virdb\\pset.db', r'virdb\\troj.db',)
            :param exist: False 断言文件或目录不存在
            :param extend: 排除判断的文件或文件夹
            :param timeout: 超时时间
            :param sleep_time：休眠时间
            :return:
        """
        end_time = time.time() + timeout
        while True:
            state = False
            if isinstance(files, (tuple, list)):
                with allure.step(f'断言 {img_info}: {len(files)} 个文件是否存在'):
                    for file in files:
                        if file not in extend:
                            result = fo.is_exist_path(file)
                            if exist:
                                if result:

                                    log.debug(f'断言成功 文件存在，文件为：{file}')
                                    assert result
                                    state = True
                                else:
                                    if time.time() > end_time:
                                        log.error(f'断言失败 文件不存在，文件为：{file}')
                                        state = False
                                        assert result
                            else:
                                if not result:
                                    log.debug(f'断言成功 文件不存在，文件为：{file}')
                                    assert not result
                                    state = True
                                else:
                                    if time.time() > end_time:
                                        log.error(f'断言失败 文件存在，文件为：{file}')
                                        state = False
                                        assert not result
                if exist and state:
                    log.info(f'断言成功 {img_info}: {len(files)} 个文件或文件夹存在')
                    break
                elif state:
                    log.info(f'断言成功 {img_info}: {len(files)} 个文件或文件夹不存在')
            if isinstance(files, str):
                with allure.step(f'断言 {img_info}: 1 个文件是否存在'):
                    if files not in extend:
                        result = fo.is_exist_path(files)
                        if exist:
                            if result:
                                log.debug(f'断言成功 文件存在，文件为：{files}')
                                assert result
                                state = True
                            else:
                                if time.time() > end_time:
                                    log.error(f'断言失败 文件不存在，文件为：{files}')
                                    assert result
                        else:
                            if not result:
                                log.debug(f'断言成功 文件不存在，文件为：{files}')
                                assert not result
                                state = True
                            else:
                                if time.time() > end_time:
                                    log.error(f'断言失败 文件存在，文件为：{files}')
                                    assert not result
                if exist and state:
                    log.info(f'断言成功 {img_info}: 1 个文件或文件夹存在')
                    break
                elif state:
                    log.info(f'断言成功 {img_info}: 1 个文件或文件夹不存在')
                    break
            if time.time() > end_time:
                assert 0
            time.sleep(sleep_time)

    def assert_files_exist(self, img_info, files, exist=True, timeout=15, sleep_time=1, extend=()):
        """
            断言 一个或多个 文件或目录是否存在
            :param img_info:
            :param files: (r'virdb\\hwl.db', r'virdb\\prop.db', r'virdb\\pset.db', r'virdb\\troj.db',)
            :param exist: False 断言文件或目录不存在
            :param extend: 排除判断的文件或文件夹
            :param timeout: 超时时间
            :param sleep_time：休眠时间
            :return:
        """
        end_time = time.time() + timeout
        while True:
            state = False
            if isinstance(files, (tuple, list)):
                # with allure.step(f'断言 {img_info}: {len(files)} 个文件是否存在'):
                for file in files:
                    if file not in extend:
                        result = fo.is_exist_path(file)
                        if exist:
                            if result:
                                with allure.step(f'断言 {img_info}: 文件为：{file}'):
                                    log.info(f'断言成功 文件存在，文件为：{file}')
                                    state = True
                                    assert result
                            else:
                                if time.time() > end_time:
                                    with allure.step(f'断言 {img_info}: 文件为：{file}'):
                                        log.error(f'断言失败 文件不存在，文件为：{file}')
                                        state = False
                                        assert result
                        else:
                            if not result:
                                with allure.step(f'断言 {img_info}: 文件为：{file}'):
                                    log.info(f'断言成功 文件不存在，文件为：{file}')
                                    state = True
                                    assert not result
                            else:
                                if time.time() > end_time:
                                    with allure.step(f'断言 {img_info}: 文件为：{file}'):
                                        log.error(f'断言失败 文件存在，文件为：{file}')
                                        state = False
                                        assert not result
                if state: break
            if isinstance(files, str):
                # with allure.step(f'断言 {img_info}: 1 个文件是否存在'):
                if files not in extend:
                    result = fo.is_exist_path(files)
                    if exist:
                        if result:
                            with allure.step(f'断言 {img_info}: 文件为：{files}'):
                                log.info(f'断言成功 文件存在，文件为：{files}')
                                state = True
                                assert result
                        else:
                            if time.time() > end_time:
                                with allure.step(f'断言 {img_info}: 文件为：{files}'):
                                    log.error(f'断言失败 文件不存在，文件为：{files}')
                                    state = False
                                    assert result
                    else:
                        if not result:
                            with allure.step(f'断言 {img_info}: 文件为：{files}'):
                                log.info(f'断言成功 文件不存在，文件为：{files}')
                                state = True
                                assert not result
                        else:
                            if time.time() > end_time:
                                with allure.step(f'断言 {img_info}: 文件为：{files}'):
                                    log.error(f'断言失败 文件存在，文件为：{files}')
                                    state = False
                                    assert not result
                    if state: break
            if time.time() > end_time: assert 0
            time.sleep(sleep_time)

    def assert_process_running(self, img_info, process, not_run=False):
        """ 断言 正在运行的进程
        data_process = ['HipsDaemon.exe', 'wsctrlsvc.exe', 'HipsTray.exe']
        not_run=False 参数默认进程运行
        """
        if isinstance(process, str):
            process = [process]
        pro = sys_info.get_process_running(process)
        with allure.step(f'{img_info} - 期望：{process}。实际：{pro}'):
            if not_run:
                if pro == []:
                    log.info(f'断言成功 进程未运行{process}')
                else:
                    log.error(f'断言失败 正在运行的程序：{pro}')
                assert pro == []
            else:
                if pro.sort() == process.sort():
                    log.info(f'断言成功 {len(pro)}个进程正在运行:{pro}')
                else:
                    if isinstance(process, str):
                        log.error(f'断言失败 {len(pro)}个进程正在运行:没有运行的进程为：{process}')
                    else:
                        log.error(f'断言失败 {len(pro)}个进程正在运行:没有运行的进程为：{list(set(process) - set(pro))}')
                assert pro == process

    def assert_process_running_linux(self, img_info, process, not_run=False):
        """ 断言 正在运行的进程
        process = hrclient、hipsmain、hipsdaemon
        not_run=False 参数默认进程运行
        """
        pro = sys_info.get_process_running_linux(process)
        with allure.step(f'{img_info} - 期望：{process}。实际：{pro}'):
            if not_run:
                if not pro:
                    log.info(f'断言成功 进程未运行：{process}')
                else:
                    log.info(f'断言失败 进程{process}正在运行，进程：{pro}')
                assert not pro
            else:
                if pro:
                    log.info(f'断言成功 进程{process}正在运行，进程：{pro}')
                else:
                    log.error(f'断言失败 进程未运行：{process}')
                assert pro

    def assert_process_startup(self, img_info, process):
        """ 断言 自启动中存在进程
        data_auto_process = ['HipsTray.exe']
        """
        if isinstance(process, str):
            process = [process]
        pro = sys_info.get_process_startup(process)
        with allure.step(f'{img_info} - 期望：{process}。实际：{pro}'):
            if pro.sort() == process.sort():
                log.info(f'{len(pro)}个进程在自启动中:{pro}')
            else:
                if isinstance(process, str):
                    log.error(f'{len(pro)}个进程在自启动中：{process}')
                else:
                    log.error(f'{len(pro)}个进程在自启动中：{list(set(process) - set(pro))}')
            assert pro == process

    def assert_driver_running(self, img_info, drivers):
        """ 断言 正在运行的驱动
        data_drivers = ['sysdiag.sys', 'hrfwdrv.sys', 'hrdevmon.sys']
        """
        if isinstance(drivers, str):
            drivers = [drivers]
        drv = sys_info.get_driver_running(drivers)
        with allure.step(f'{img_info} - 期望：{drivers}。实际：{drv}'):
            if drv.sort() == drivers.sort():
                log.info(f'{len(drv)}个驱动正在运行:{drv}')
            else:
                log.error(f'{len(drv)}个驱动正在运行:没有运行的驱动为：{list(set(drivers) - set(drv))}')
            assert drv == drivers

    def assert_in(self, info, data, ele, other_ele=None):
        """
        断言 data 包含 ele
        :param info: 描述信息
        :param data: 数据
        :param ele: 元素
        :param other_ele：其他元素
        :return:
        """
        with allure.step(f'{info}-包含："{ele}"'):
            # if ele in data:
            if re.findall(ele, data):
                allure.attach('断言包含成功', f'期望-包含：{ele}； 实际-包含：{ele}； 校验值：{data}; ')
                log.info(f'断言包含成功-包含元素：{ele}； 校验值：{data}')
            else:
                if other_ele:
                    if re.findall(other_ele, data):
                        allure.attach('断言包含成功', f'期望-包含：{other_ele}； 实际-包含：{other_ele}； 校验值：{data}; ')
                        log.info(f'断言包含成功-包含元素：{other_ele}； 校验值：{data}')
                        re.findall(other_ele, data)
                else:
                    allure.attach('断言包含失败', f'期望-包含：{ele}； 实际-未包含：{ele}； 校验值：{data}; ')
                    log.error(f'断言包含失败-包含元素：{ele}； 校验值：{data}')
                    # assert ele in data
                    assert re.findall(ele, data)

    def assert_equal(self, info, a, b):
        """
        断言 a == b
        :param info: 描述信息
        :param a:
        :param b:
        :return:
        """
        with allure.step(f'{info}-{a} == {b}'):
            if a == b:
                allure.attach('断言相等成功', f'期望：{a} == {b}；实际：{a} == {b}')
                log.info(f'断言相等成功，期望：{a} == {b}；实际：{a} == {b}')
            else:
                allure.attach('断言相等失败', f'期望：{a} == {b}；实际：{a} != {b}')
                log.error(f'断言相等失败，期望：{a} == {b}；实际：{a} != {b}')
            assert a == b


if __name__ == '__main__':
    pass
