# -*- coding:utf-8 -*-
# @Time   : 2021/12/22 9:29
# @Author : tq
# @File   : conftest.py
import os
import time
import json

import allure
import pytest

from conf.config import conf
from conf.confpath import ConfPath, ConfSystemType
from common.log import log
from utils.request import send_info, create_snapshot
from utils.file import fo


def pytest_runtest_protocol(item, nextitem):
    """ 每个测试用例执行前，执行一次 """
    log.info(f'---执行开始---：{item.nodeid}')
    send_info(f'-执行开始-{item.nodeid.split("/")[-1]}')

    if 'hr_install.py::' in item.nodeid:
        conf.run_flag_write('1')
        log.info('修改标志为1')
    else:
        conf.run_flag_write('2')
        log.info('修改标志为2')


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """ 获取用例执行结果的钩子函数（每个测试用例执行完成后，执行一次）  # 用例失败后自动截图 """
    outcome = yield
    report = outcome.get_result()

    filepath = os.path.join(ConfPath.PATH_DIR, 'failures.png')
    if report.when == 'call' and report.failed:
        branch = fo.json_read('branch', ConfPath.REMOTE_CONFIG_FILE).strip()
        if branch == 'main':
            create_snapshot(item.nodeid.split('::')[-1])
            time.sleep(1)
        if ConfSystemType.system_type == 'desktop':
            mode = 'a' if os.path.exists(ConfPath.REPORT_LOC_DIR + '/failures') else 'w'
            with open(ConfPath.REPORT_LOC_DIR + '/failures', mode) as f:
                if 'tmpir' in item.fixturenames:
                    extra = ' (%s) ' % item.funcargs['tmpdir']
                else:
                    extra = ''
                    f.write(report.nodeid + extra + '\n')
                with allure.step('用例运行失败截图...'):
                    if not os.path.exists(filepath):
                        return
                    with open(filepath, 'rb') as f:
                        file = f.read()
                        allure.attach(file, '失败截图', allure.attachment_type.PNG)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """ 收集测试结果（全部测试用例执行完成后，执行一次）, 并写入文件 """
    mydict = {}
    mydict['total'] = terminalreporter._numcollected
    mydict['deselected'] = len(terminalreporter.stats.get("deselected", []))
    mydict['selected'] = terminalreporter._numcollected - len(terminalreporter.stats.get("deselected", []))
    mydict['passed'] = len(terminalreporter.stats.get("passed", []))
    mydict['failed'] = len(terminalreporter.stats.get("failed", []))
    mydict['error'] = len(terminalreporter.stats.get("error", []))
    mydict['skipped'] = len(terminalreporter.stats.get("skipped", []))
    mydict['total times'] = f'{time.time() - terminalreporter._sessionstarttime} seconds'
    try:
        with open(ConfPath.REPORT_LOC_DIR + f'/result.txt', 'w', encoding='utf-8') as fp:
            json.dump(mydict, fp, ensure_ascii=False, indent=2)
    except:
        with open(ConfPath.REPORT_LOC_DIR + '/API_result.txt', 'w', encoding='utf-8') as fp:
            json.dump(mydict, fp, ensure_ascii=False, indent=2)
