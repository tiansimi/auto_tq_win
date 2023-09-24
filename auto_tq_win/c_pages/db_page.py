# -*- coding:utf-8 -*-
# @Time   : 2022/3/30 10:17
# @Author : tq
# @File   : db_page.py
import os
import time
import json
import allure
import struct
from jsonpath import jsonpath
import json_tools

from c_datas.data_install import DataInstall
from c_datas.data_path import DataSecurityLog
from common.log import log
from utils.file import fo
from utils.sqlite import Sqlite
from conf.confpath import ConfPath


class DbPage:

    def __init__(self):
        self.log_file = 'log.db'
        self.quarantine_file = 'quarantine.db'
        self.config_file = 'config.db'
        self.trust_file = 'wlfile.db'

    def copy_db_file(self, db_name, system_type='desktop'):
        """
        拷贝日志文件到桌面
        :param db_name: 数据库文件。如：log.db
        :param system_type: 系统类型：desktop、server
        :return:
        """
        time.sleep(1)
        if '.' in db_name:
            db_name = db_name.split('.')[0]

        # suffixs = ('.db', '.db-shm', '.db-wal')
        # files_path = [os.path.join(DataInstall.SHARE_DIR, db_name + suffix) for suffix in suffixs]
        # dst_path = ConfPath.DB_DIR

        if system_type == 'desktop':
            suffixs = ('.db', '.db-shm', '.db-wal')
            files_path = [os.path.join(DataInstall.SHARE_DIR, db_name + suffix) for suffix in suffixs]
            dst_path = ConfPath.DB_DIR
        else:
            suffixs = ('.db', '.db-shm', '.db-wal')
            files_path = [os.path.join(DataInstallServer.SHARE_DIR, db_name + suffix) for suffix in suffixs]
            dst_path = ConfPath.DB_DIR

        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        for file_path in files_path:
            if os.path.exists(file_path):
                fo.copy_local(file_path, dst_path)

    def get_count_from_db(self, img_info, db_name, sql_select: str, expect: int, gt=False):
        """
        获取数据库 记录数量
        :param img_info: 信息
        :param db_name: 数据库文件。如：log.db
        :param sql_select: 查询数量的语句 select count(*) from 表
        :param expect: 期望数量
        :param gt: 大于期望数量
        :return:
        """
        if not sql_select.lower().strip().startswith('select count(*) from'):
            raise ValueError('获取数量的sql语句，必须以 select count(*) from 开头')
        i = 1
        while True:
            time.sleep(2)
            self.copy_db_file(db_name)
            sqlite = Sqlite(os.path.join(ConfPath.DB_DIR, db_name))
            result = sqlite.select(sql_select)
            log.info(f'查询结果数量：{result[0][0]}')
            length = result[0][0]

            with allure.step(f'断言 {img_info}下查杀数量'):
                allure.attach('断言', f'期望结果：{expect}, 实际结果-{img_info}:{length}')
                if not gt:
                    if length == expect:
                        log.info(f'断言成功 期望结果：{expect}, 实际结果-{img_info}:{length}')
                        break
                    else:
                        log.error(f'断言失败-第 {i} 次 期望结果：{expect}, 实际结果-{img_info}:{length}')
                        i += 1
                        if i > 2:
                            log.error(f'断言失败-第 {i} 次 期望结果：{expect}, 实际结果-{img_info}:{length}')
                            assert length == expect
                            break
                else:
                    if length >= expect:
                        log.info(f'断言成功 期望结果条数大于：{expect}, 实际结果-{img_info}:{length}')
                        break
                    else:
                        log.error(f'断言失败-第 {i} 次 期望结果条数大于：{expect}, 实际结果-{img_info}:{length}')
                        i += 1
                        if i > 2:
                            log.error(f'断言失败-第 {i} 次 期望结果条数大于：{expect}, 实际结果-{img_info}:{length}')
                            assert length > expect
                            break

    def get_data_from_db(self, db_name, sql_select, system_type='desktop'):
        """
        获取数据库 数据
        :param db_name: 数据库文件。如：log.db
        :param sql_select: 查询数据的语句 select detail from 表
        :param system_type: 系统类型：desktop、server
        :return:
        """
        self.copy_db_file(db_name, system_type)
        sqlite = Sqlite(os.path.join(ConfPath.DB_DIR, db_name))
        result = sqlite.select(sql_select)
        with allure.step(f'获取:{db_name}中的数据'):
            allure.attach('获取数据', f'获取:{db_name}实际结果:{result}')
            log.info(f'获取:{db_name}实际结果:{result}')
        return result

    def get_log_data(self, current_time=None):
        """ 获取日志库数据 """
        sql = f'select fid, detail from HrLogV3 where ts >= {current_time}'
        res = self.get_data_from_db('log.db', sql)
        log.info(str(res))
        return res

    def get_log_data_detail(self, fid=None, current_time=None):
        """ 获取日志库数据 """
        sql = f'select fid, detail from HrLogV3 where fid = {fid} and ts >= {current_time}'
        res = self.get_data_from_db('log.db', sql)
        log.info(str(res))
        return res

    def get_detailed_data(self, img_info, current_time=None):
        """ 用于文件实时监控，下载保护和web扫描 """
        db_list = []
        db_data = self.get_log_data(img_info, current_time=current_time)
        for data in db_data:
            db_dict = {}
            if isinstance(data, tuple):
                db_dict['fid'] = data[0]  # 提取 当前运行程序的ID
                db_dict['fname'] = data[1]  # 提取 当前运行的名称
                for tup in data:
                    if isinstance(tup, str) and "detail" in tup:
                        tup = json.loads(tup)
                        db_dict['treatment'] = jsonpath(tup, '$..treatment')[0]  # 提取 处理结果
                        db_dict['recname'] = jsonpath(tup, '$..recname')[0]  # 提取 病毒名称
                        db_dict['rid'] = jsonpath(tup, '$..rid')[0]  # 提取 病毒ID
                        db_dict['pathname'] = jsonpath(tup, '$..pathname')[0]  # 提取 病毒路径
            db_list.append(db_dict)
        return db_list

    def get_trust_files(self):
        """ 获取信任区信任项目 """
        db_name = 'wlfile.db'
        sql = "select fn from TrustFileV3"
        result = self.get_data_from_db(db_name, sql)
        return len(result)

    def get_quarantine_file_count(self, current_time=0):
        """ 获取隔离区文件数量 """
        db_name = self.quarantine_file
        sql = f"select sha1 from FilesV3 where ts > {current_time};"
        result = self.get_data_from_db(db_name, sql)
        return len(result)

    def get_quarantine_file_id(self, current_time=0, system_type='desktop'):
        """ 获取db文件中隔离区id """
        db_name = self.quarantine_file
        sql = f"select Id from FilesV3 where ts > {current_time};"
        result = self.get_data_from_db(db_name, sql, system_type=system_type)
        return result

    def get_task_data_detail(self, task_id, system_type='desktop'):
        """ 获取任务库数据 """
        sql = f'select data from CenterTask where task_id={task_id}'
        res = self.get_data_from_db('task.db', sql, system_type=system_type)
        log.info(str(res))
        return res

    def assert_detailed_general(self, img_info, current_time=None, fid=None, expect_data=None, expect_count=[],
                                ignore_data=None):
        """
        从数据详细信息中获取指定的参数
        @param img_info: 描述信息
        @param current_time: 查询时间
        @param fid: 当前运行程序id
        @param expect_data: 预期数据
        @param expect_count: 预期匹配数据条数
        @param ignore_data: 忽略信息，开始、结束时间等
        @return:
        """
        db_data = self.get_log_data_detail(fid=fid, current_time=current_time)
        # [('{"fid":2,"version":{"product":"2.0.0.1","dbtime":0},"detail":{"auto":1,"fetched":[{"err":0,"timestamp":1655202163,"url":"bases/libvxf.vdl.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vdl"},{"err":0,"timestamp":1655202163,"url":"bases/libvxf.vds.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vds"},{"err":0,"timestamp":1655202163,"url":"bases/libvxf.dat.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.dat"},{"err":0,"timestamp":1655202163,"url":"bases/libvxf.tdl.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.tdl"},{"err":0,"timestamp":1655202163,"url":"bases/hwl.db.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/hwl.db"},{"err":0,"timestamp":1655202163,"url":"bases/prop.db.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/prop.db"},{"err":0,"timestamp":1655202163,"url":"bases/pset.db.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/pset.db"},{"err":0,"timestamp":1655202164,"url":"bases/troj.db.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/troj.db"}],"merged":[{"err":0,"timestamp":1655202164,"dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vdl"},{"err":0,"timestamp":1655202164,"dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vds"},{"err":0,"timestamp":1655202164,"dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.dat"},{"err":0,"timestamp":1655202164,"dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.tdl"},{"err":0,"timestamp":1655202164,"dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/hwl.db"},{"err":0,"timestamp":1655202164,"dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/prop.db"},{"err":0,"timestamp":1655202164,"dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/pset.db"},{"err":0,"timestamp":1655202164,"dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/troj.db"}],"err":0,"timestamp":1655202164,"errmsg":[],"prevdbtime":0,"newver":"2.0.0.1","newdbtime":1655022284,"prever":"2.0.0.1"}}',),
        #  ('{"fid":2,"version":{"product":"2.0.0.1","dbtime":0},"detail":{"auto":1,"fetched":[{"err":0,"timestamp":1655202224,"url":"bases/libvxf.vdl.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vdl"},{"err":0,"timestamp":1655202224,"url":"bases/libvxf.vds.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vds"},{"err":0,"timestamp":1655202224,"url":"bases/libvxf.dat.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.dat"},{"err":0,"timestamp":1655202224,"url":"bases/libvxf.tdl.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.tdl"},{"err":0,"timestamp":1655202225,"url":"bases/hwl.db.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/hwl.db"},{"err":0,"timestamp":1655202225,"url":"bases/prop.db.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/prop.db"},{"err":0,"timestamp":1655202225,"url":"bases/pset.db.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/pset.db"},{"err":0,"timestamp":1655202225,"url":"bases/troj.db.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/troj.db"}],"merged":[{"err":0,"timestamp":1655202225,"dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vdl"},{"err":0,"timestamp":1655202225,"dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vds"},{"err":0,"timestamp":1655202225,"dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.dat"},{"err":0,"timestamp":1655202225,"dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.tdl"},{"err":0,"timestamp":1655202225,"dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/hwl.db"},{"err":0,"timestamp":1655202225,"dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/prop.db"},{"err":0,"timestamp":1655202225,"dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/pset.db"},{"err":0,"timestamp":1655202225,"dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/troj.db"}],"err":0,"timestamp":1655202225,"errmsg":[],"prevdbtime":0,"newver":"2.0.0.1","newdbtime":1655022284,"prever":"2.0.0.1"}}',)
        # ]
        # expect_dic ={"fid":2,"detail":{"auto":1,"fetched":[{"err":0,"url":"bases/libvxf.vdl.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vdl"},{"err":0,"url":"bases/libvxf.vds.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vds"},{"err":0,"url":"bases/libvxf.dat.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.dat"},{"err":0,"url":"bases/libvxf.tdl.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.tdl"},{"err":0,"url":"bases/hwl.db.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/hwl.db"},{"err":0,"url":"bases/prop.db.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/prop.db"},{"err":0,"url":"bases/pset.db.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/pset.db"},{"err":0,"url":"bases/troj.db.vfs","dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/troj.db"}],"merged":[{"err":0,"dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vdl"},{"err":0,"dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vds"},{"err":0,"dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.dat"},{"err":0,"dstfn":"/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.tdl"},{"err":0,"dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/hwl.db"},{"err":0,"dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/prop.db"},{"err":0,"dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/pset.db"},{"err":0,"dstfn":"/opt/apps/cn.huorong.esm/files/share/virdb/troj.db"}],"err":0,"errmsg":[]}}

        count = 0
        with allure.step(f'断言：{img_info}，日志存入数据与预期相符'):
            allure.attach('断言', f'{img_info}功能与期望相符')
            try:
                for data in db_data:
                    if isinstance(data, tuple):
                        state = True
                        if fid != data[0]:
                            log.info(f"位置：fid，实际结果：{data[0]}  期望结果：{fid}，比对结果不相符")
                            state = False

                        tup = json.loads(data[1])
                        result = json_tools.diff(expect_data, tup)
                        for ii in result:
                            if 'add' in ii:
                                ignore_str = ii['add'][ii['add'].rfind('/') + 1:]
                                if ignore_str in ignore_data:
                                    continue
                                else:
                                    log.info(f"位置：{ii['add']}，实际结果：{ii['value']}，比对结果不相符，分析原因：出现未知字段")
                                    state = False
                            elif 'replace' in ii:
                                log.info(f"位置：{ii['replace']}，实际结果：{ii['value']} 期望结果：{ii['prev']}，比对结果不相符")
                                state = False
                            elif 'remove' in ii:
                                log.info(f"位置：{ii['remove']}，实际结果：缺少该值  期望结果：{ii['prev']}，比对结果不相符")
                                state = False

                        if state:
                            count += 1
            except Exception as e:
                log.info(f'断言失败【{img_info}】，内部发生异常！')
                assert 0

            if count == expect_count:
                log.info(f'断言成功【{img_info}】，比对结果相符，期望匹配日志条数为：{expect_count}，实际匹配的条数为：{count}')
            else:
                log.info(f'断言失败【{img_info}】，比对结果不相符，期望匹配日志条数为：{expect_count}，实际匹配的条数为：{count}')
            assert count == expect_count

    def assert_config_data(self, img_info, subkey, name, expect, timeout=15):
        """
        断言config.db文件数据，用于修改设置项后验证
        :param img_info: 步骤信息
        :param subkey: 关键字
        :param name: 关键字名称
        :param expect: 预期结果
        :param timeout：超时时长
        """
        end_time = time.time() + timeout
        while True:
            sql = f"select data from userconfig where subkey='{subkey}' and name='{name}'"
            res = self.get_data_from_db(self.config_file, sql)
            if len(res) > 0:
                result = res[0][0]  # b'\x00\x00\x00\x00'
                unpack_str = struct.unpack('i', result)[0]
            else:
                unpack_str = 0
            # with allure.step('断言 设置项修改后db文件数据同步修改'):
            #     allure.attach(f'断言{img_info}, 期望结果：{expect}, 实际结果：{unpack_str}')
            if expect == unpack_str:
                with allure.step('断言 设置项修改后db文件数据同步修改'):
                    allure.attach(f'断言{img_info}, 期望结果：{expect}, 实际结果：{unpack_str}')
                    log.info(f'断言成功 {img_info} 期望结果：{expect}，实际结果：{unpack_str}')
                    assert expect == unpack_str
                    break
            if time.time() > end_time:
                with allure.step('断言 设置项修改后db文件数据同步修改'):
                    allure.attach(f'断言{img_info}, 期望结果：{expect}, 实际结果：{unpack_str}')
                    log.error(f'断言失败 {img_info} 期望结果：{expect}，实际结果：{unpack_str}')
                    assert expect == unpack_str  # 条件为假时，程序自动崩溃并抛出AssertionError的异常。
            time.sleep(2)

    def assert_log_type(self, img_info, current_time=None):
        """ 断言 日志类型 """
        pass

    def assert_detailed_data(self, img_info, current_time=None, pname=None, result=None, filepath=None):
        """
        用于 文件实时监控，下载保护和web扫描，验证日志信息与期望值是否相符
        :param img_info: 步骤信息
        :param current_time: 时间段
        :param pname: 当前测试功能的名称
        :param result: 处理结果
        :param filepath: 病毒路径
        :return:
        """
        detailed_list = self.get_detailed_data(img_info, current_time=current_time)
        for line in range(0, len(detailed_list)):
            with allure.step(f'断言验证{pname}功能，得到的数据，与日志存入是否相符'):
                allure.attach('断言', f'期望结果：运行程序名称为-{pname}, 实际运行程序名称{detailed_list[line]["fname"]}，断言 处理结果为{result}，'
                                    f'实际处理结果为：{detailed_list[line]["treatment"]}，断言病毒名称为{filepath[line]}，实际名称为：{detailed_list[line]["pathname"]}')

                filepath_name = \
                    [virus_name for virus_name in filepath if virus_name in detailed_list[line]['pathname']][0]
                if detailed_list[line]["fname"] == pname and detailed_list[line][
                    "treatment"] == result and filepath_name in detailed_list[line]['pathname']:
                    log.info(f'断言 成功 期望结果：运行程序名称为{pname}, 实际运行程序名称{detailed_list[line]["fname"]}，断言 处理结果为{result}，'
                             f'实际处理结果为：{detailed_list[line]["treatment"]}，断言病毒名称为{filepath_name}，实际名称为：{detailed_list[line]["pathname"]}')
                else:
                    log.error(f'断言 失败 期望结果：运行程序名称为{pname}, 实际运行程序名称{detailed_list[line]["fname"]}，断言 处理结果为{result}，'
                              f'实际处理结果为：{detailed_list[line]["treatment"]}，断言病毒名称为{filepath_name}，实际名称为：{detailed_list[line]["pathname"]}')
                assert detailed_list[line]["fname"] == pname
                assert detailed_list[line]["treatment"] == result
                assert filepath_name in detailed_list[line]["pathname"]

    def assert_log_db_scan_count(self, img_info, expect, expect2=None, current_time=0, system_type='desktop', fid=0):
        """
        扫描时，获取日志中 发现风险数量 和 已处理风险数量 与期望值相等
        :param img_info: 步骤信息
        :param expect: 期望发现病毒数
        :param expect2: 期望处理病毒数
        :param current_time: 当前时间戳
        :param system_type: 系统类型：desktop、server
        :param fid: fid=0 病毒查杀
        :return:
        """
        db_name = self.log_file
        sql = f"select detail from HrLogV3 where ts > {current_time} and fid = {fid};"
        res = self.get_data_from_db(db_name, sql, system_type)

        virus_count = None
        killed_count = None
        if len(res) > 0:
            result = res[0][0]
            js = json.loads(result)
            try:
                # 提取 json 数据
                virus_count = jsonpath(js, '$..threats')[0]  # 日志中提取 - 发现风险数量
                killed_count = jsonpath(js, '$..threat_killed')[0]  # 日志中提取 - 已处理风险数量
            except Exception as e:
                log.error(e)
        # result = res[0][0]
        # js = json.loads(result)
        #
        # # 提取 json 数据
        # virus_count = jsonpath(js, '$..threats')[0]  # 日志中提取 - 发现风险数量
        # killed_count = jsonpath(js, '$..threat_killed')[0]  # 日志中提取 - 已处理风险数量

        if expect2 is None:
            expect2 = expect

        with allure.step('断言 扫描时发现风险和已处理风险数量'):
            allure.attach(f'断言{img_info}', f'期望结果：{expect}-{expect2}, 实际结果：发现风险:{virus_count},处理风险数量:{killed_count}')
            if virus_count == expect and killed_count == expect2:
                log.info(f'断言成功 {img_info} 期望结果：{expect}-{expect2}, 实际结果：发现风险:{virus_count},处理风险数量:{killed_count}')
            else:
                log.error(f'断言失败 {img_info} 期望结果：{expect}-{expect2}, 实际结果：发现风险:{virus_count},处理风险数量:{killed_count}')
            assert virus_count == expect
            assert killed_count == expect2

    # def assert_log_db_scan_count_loop(self, img_info, expect, expect2=None, current_time=0, system_type='desktop', loop_timeout=15):
    #     """
    #     扫描时，获取日志中 发现风险数量 和 已处理风险数量 与期望值相等
    #     :param img_info: 步骤信息
    #     :param expect: 期望发现病毒数
    #     :param expect2: 期望处理病毒数
    #     :param current_time: 当前时间戳
    #     :param system_type: 系统类型：desktop、server
    #     :return:
    #     """
    #     if expect2 is None:
    #         expect2 = expect
    #
    #     virus_count = None
    #     killed_count = None
    #
    #     end_time = time.time() + loop_timeout
    #     while True:
    #         db_name = self.log_file
    #         sql = f"select detail from HrLogV3 where ts > {current_time};"
    #         res = self.get_data_from_db(db_name, sql, system_type)
    #
    #         if len(res) > 0:
    #             result = res[0][0]
    #             js = json.loads(result)
    #             try:
    #                 # 提取 json 数据
    #                 virus_count = jsonpath(js, '$..threats')[0]  # 日志中提取 - 发现风险数量
    #                 killed_count = jsonpath(js, '$..threat_killed')[0]  # 日志中提取 - 已处理风险数量
    #
    #                 with allure.step('断言 扫描时发现风险和已处理风险数量'):
    #                     allure.attach(f'断言{img_info}', f'期望结果：{expect}-{expect2}, 实际结果：发现风险:{virus_count},处理风险数量:{killed_count}')
    #                     log.info(f'断言成功 {img_info} 期望结果：{expect}-{expect2}, 实际结果：发现风险:{virus_count},处理风险数量:{killed_count}')
    #                     assert virus_count == expect
    #                     assert killed_count == expect2
    #                 break
    #             except Exception as e:
    #                 log.error(e)
    #         if time.time() > end_time:
    #             with allure.step('断言 扫描时发现风险和已处理风险数量'):
    #                 allure.attach(f'断言{img_info}', f'期望结果：{expect}-{expect2}, 实际结果：发现风险:{virus_count},处理风险数量:{killed_count}')
    #                 log.error(f'断言失败 {img_info} 期望结果：{expect}-{expect2}, 实际结果：发现风险:{virus_count},处理风险数量:{killed_count}')
    #                 assert virus_count == expect
    #                 assert killed_count == expect2  # 条件为假时，程序自动崩溃并抛出AssertionError的异常。
    #         time.sleep(3)

    def assert_log_db_scan_count_loop(self, img_info, expect, expect2=None, current_time=0, system_type='desktop',
                                      loop_timeout=15, sleep_time=3, fid =0):
        """
        扫描时，获取日志中 发现风险数量 和 已处理风险数量 与期望值相等
        :param img_info: 步骤信息
        :param expect: 期望发现病毒数
        :param expect2: 期望处理病毒数
        :param current_time: 当前时间戳
        :param system_type: 系统类型：desktop、server
        :param loop_timeout：超时时长
        :param sleep_time：休眠时间
        :return:
        """
        if expect2 is None:
            expect2 = expect

        virus_count = None
        killed_count = None

        end_time = time.time() + loop_timeout
        while True:
            db_name = self.log_file
            sql = f"select detail from HrLogV3 where ts > {current_time} and fid ={fid};"
            res = self.get_data_from_db(db_name, sql, system_type)

            if len(res) > 0:
                result = res[0][0]
                js = json.loads(result)
                try:
                    # 提取 json 数据
                    virus_count = jsonpath(js, '$..threats')[0]  # 日志中提取 - 发现风险数量
                    killed_count = jsonpath(js, '$..threat_killed')[0]  # 日志中提取 - 已处理风险数量

                    with allure.step('断言 扫描时发现风险和已处理风险数量'):
                        allure.attach(f'断言{img_info}',
                                      f'期望结果：{expect}-{expect2}, 实际结果：发现风险:{virus_count},处理风险数量:{killed_count}')
                        log.info(
                            f'断言成功 {img_info} 期望结果：{expect}-{expect2}, 实际结果：发现风险:{virus_count},处理风险数量:{killed_count}')
                        assert virus_count == expect
                        assert killed_count == expect2
                except Exception as e:
                    log.error(e)
                break
            if time.time() > end_time:
                with allure.step('断言 扫描时发现风险和已处理风险数量'):
                    allure.attach(f'断言{img_info}',
                                  f'期望结果：{expect}-{expect2}, 实际结果：发现风险:{virus_count},处理风险数量:{killed_count}')
                    log.error(f'断言失败 {img_info} 期望结果：{expect}-{expect2}, 实际结果：发现风险:{virus_count},处理风险数量:{killed_count}')
                    assert virus_count == expect
                    assert killed_count == expect2  # 条件为假时，程序自动崩溃并抛出AssertionError的异常。
            time.sleep(sleep_time)

    def assert_log_db_count(self, img_info, expect, current_time=None, gt=False):
        """
        获取日志中 发现风险数量  filemon(文件实时监控)、behavior(恶意行为监控)
        :param img_info: 步骤信息
        :param expect: 期望日志病毒数
        :param current_time: 当前时间戳
        :param gt: 大于 expect
        :return:
        """
        db_name = self.log_file
        if current_time:
            sql = f"select count(*) from HrLogV3 where ts > {current_time};"
        else:
            sql = f"select count(*) from HrLogV3 "
        self.get_count_from_db(img_info, db_name, sql, expect, gt=gt)

    def assert_msg_db_count(self, img_info, expect, current_time=0):
        """
        读取功能消息
        :param img_info: 步骤信息
        :param expect: 期望功能消息数
        :param current_time: 当前时间戳
        :return: 返回查询内容
        """
        db_name = self.log_file
        sql = f"select count(*) from HrTrayMsg where ts > {current_time};"
        self.get_count_from_db(img_info, db_name, sql, expect)

    def assert_quarantine_db_count(self, img_info, expect, current_time=0):
        """
        读取功能消息
        :param img_info: 步骤信息
        :param expect: 期望隔离区病毒数
        :param current_time: 当前时间戳
        :return: 返回查询内容
        """
        db_name = self.quarantine_file
        sql = f"select count(*) from FilesV3 where ts > {current_time};"
        self.get_count_from_db(img_info, db_name, sql, expect)

    def assert_quarantine_files_in_dirs(self, img_info, expect, current_time=0, system_type='desktop'):
        """
        断言本次查杀隔离区文件数量 及隔离文件存在于隔离区中
        :param img_info: 步骤信息
        :param expect: 期望隔离区文件数
        :param current_time: 当前时间戳
        :param system_type: 系统类型：desktop、server
        :return:
        """
        db_name = self.quarantine_file
        sql = f"select sha1 from FilesV3 where ts > {current_time};"
        result = self.get_data_from_db(db_name, sql, system_type=system_type)
        # result = [('FC52640121B665ADED5BBC55868EAF302795C28A',), ('2BA28E4B50942789155D21602A1FE852629E0C92',)]
        with allure.step(f'断言本次隔离文件数量-实际：{len(result)}，期望：{expect}'):
            if len(result) == expect:
                log.info(f'断言成功 {img_info} 期望结果：{expect}, 实际结果：{len(result)}')
            else:
                log.error(f'断言失败 {img_info} 期望结果：{expect}, 实际结果：{len(result)}')
            assert len(result) == expect
        if result:
            file_sha1 = [res[0] for res in result]
            if system_type == 'desktop':
                res = fo.files_in_dir(DataInstall.QUARANTINE_DIR, file_sha1)
            else:
                res = fo.files_in_dir(DataInstallServer.QUARANTINE_DIR, file_sha1)
            with allure.step(f'断言被隔离文件在硬盘中-实际{file_sha1}，期望：存在'):
                assert res

    def assert_trust_files_count(self, img_info, expect):
        """ 断言信任区信任项目数量 """
        res = self.get_trust_files()
        with allure.step(f'断言{img_info}'):
            allure.attach(f'断言{img_info}', f'期望结果：{expect}, 实际结果：{res}')
            if res == expect:
                log.info(f'断言成功 {img_info} 期望结果：{expect}, 实际结果：{res}')
            else:
                log.error(f'断言失败 {img_info} 期望结果：{expect}, 实际结果：{res}')
            assert res == expect

    def assert_delete_security_log(self, img_info, expect, current_time=0):
        """ 删除数据库安全日志数据 """
        db_name = self.log_file
        sql = f"delete from HrLogV3 where ts >= {current_time}"
        sqlite = Sqlite(os.path.join(data_install.hr_share_dir, db_name))
        result = sqlite.update_delete_insert(sql)

        with allure.step(f'断言{img_info}'):
            allure.attach(f'断言{img_info}', f'期望结果：{expect}, 实际结果：{result}')
            if result == expect:
                log.info(f'断言成功 {img_info} 期望结果：{expect}, 实际结果：{result}')
            else:
                log.error(f'断言失败 {img_info} 期望结果：{expect}, 实际结果：{result}')
            assert result == expect

    def assert_task_db(self, img_info, task_id, expect_data=None, system_type='desktop', timeout=15, sleep_time=3):
        """
        断言任务信息数据库存入数据
        @param img_info: 描述信息
        @param task_id: 中心任务Id
        @param expect_data: 预期数据
        @param system_type: 系统类型  desktop/server
        @param timeout：超时时长
        @param sleep_time：休眠时长
        @return:
        """
        end_time = time.time() + timeout
        while True:
            db_data = self.get_task_data_detail(task_id, system_type=system_type)
            if len(db_data) > 0:
                for data in db_data:
                    if isinstance(data, tuple):
                        db_dict = json.loads(data[0])
                        task_param = db_dict['param']
                        expect_param = expect_data['param']

                        with allure.step('断言数据库 与 预期结果 一致'):
                            allure.attach('断言', f'{img_info} - 期望结果：{expect_param}, 实际结果：{task_param}')
                            if isinstance(task_param, dict):
                                # 获取两个字典相同的key
                                diff = task_param.keys() & expect_param.keys()
                                # 获取相同key，不同value
                                diff_vals = [(k, task_param[k], expect_param[k]) for k in diff if
                                             task_param[k] != expect_param[k]]
                                if diff_vals:
                                    log.error(f'不一致字段：{diff_vals}')
                                log.info(f'数据库与期望结果字段对比：期望为[]空列表, 实际结果：{diff_vals}')
                                assert not diff_vals

                            diff_state = True
                            if db_dict['id'] != task_id:
                                log.error(f'数据库与期望结果对比：不一致字段task_id： - 预期结果：{task_id}, 实际结果：{db_dict["id"]}')
                                diff_state = False
                            if db_dict['name'] != expect_data['type']:
                                log.error(
                                    f'数据库与期望结果对比：不一致字段task_name： - 预期结果：{expect_data["type"]}, 实际结果：{db_dict["name"]}')
                                diff_state = False
                            log.info(
                                f'数据库与期望结果字段对比：字段task_id、task_name预期结果：{task_id}-{expect_data["type"]}， 实际结果：{db_dict["id"]}-{db_dict["name"]}')
                            assert diff_state
                break
            if time.time() > end_time:
                with allure.step('断言数据库 与 预期结果 一致'):
                    allure.attach('断言', f'{img_info} - 期望结果：{expect_data["param"]}, 实际结果：{[]}')
                    log.error(f'断言失败 {img_info} 期望结果：{expect_data["param"]}，实际结果：[]')
                    assert 0  # 条件为假时，程序自动崩溃并抛出AssertionError的异常。
            time.sleep(sleep_time)

    def assert_task_db_plan(self, img_info, plan_id, expect_data=None, system_type='desktop', timeout=15, sleep_time=3,
                            **kwargs):
        """
        断言任务信息数据库存入数据
        @param img_info: 描述信息
        @param plan_id: 计划任务Id
        @param expect_data: 预期数据
        @param system_type: 系统类型  desktop/server
        @param timeout：超时时长
        @param sleep_time：休眠时长
        @param kwargs：对比排除字段
        @return:
        """
        end_time = time.time() + timeout
        while True:
            db_data = self.get_task_data_detail(plan_id, system_type=system_type)
            # db_data = [('{"id":66,"config":{"id":66,"create_time":1658553169,"update_time":1658553169,"sched_name":"计划任务_717","action":{"type":"quick_scan","param":{"scan_end_halt":false,"cannot_cancel":true,"clean_automate":true,"scan_maxspeed":false,"clean_quarantine":true,"whitelist_ignore":false}},"memo":"自动化计划任务备注信息_666","enabled":true,"trigger":{"type":"ByOnce","param":{"start_datetime":"2022-07-23 13:13","interval":0,"start_time":"2022-07-23 13:13"}},"exceptions":{"run_limit":0,"retry":{"interval":180,"times":0},"exec_expire":false,"retry_on":false,"run_limit_on":false}},"result":{"preform_ts":0,"next_ts":1658553180}}',)]
            # expect_data= {'name': '计划任务_717', 'memo': '自动化计划任务备注信息_666', 'trigger': {'type': 'ByOnce', 'param': {'start_time': '2022-07-23 13:13', 'start_datetime': '2022-07-23 13:13', 'interval': 0}}, 'exceptions': {'retry_on': False, 'retry': {'times': 0, 'interval': 180}, 'run_limit_on': False, 'run_limit': 0, 'exec_expire': False}, 'target_type': 'clients', 'action': {'type': 'quick_scan', 'param': {'whitelist_ignore': False, 'scan_maxspeed': False, 'clean_automate': True, 'clean_quarantine': True, 'scan_end_halt': False, 'cannot_cancel': True}}, 'clients': [1]}

            if len(db_data) > 0:
                log.info(f'任务db文件数据：{db_data}')
                log.info(f'预期数据：{expect_data}')
                for data in db_data:
                    if isinstance(data, tuple):
                        db_dict = json.loads(data[0])
                        task_param = db_dict['config']
                        if kwargs:
                            for kw in kwargs:
                                if kwargs.get(kw) == 'exclude':
                                    expect_data.pop(kw)
                        expect_param = expect_data

                        with allure.step('断言数据库 与 预期结果 一致'):
                            allure.attach('断言', f'{img_info} - 期望结果：{expect_param}, 实际结果：{task_param}')
                            if isinstance(task_param, dict):
                                # 获取两个字典相同的key
                                diff = task_param.keys() & expect_param.keys()
                                # 获取相同key，不同value
                                diff_vals = [(k, task_param[k], expect_param[k]) for k in diff if
                                             task_param[k] != expect_param[k]]
                                if diff_vals:
                                    log.error(f'不一致字段：{diff_vals}')
                                log.info(f'数据库与期望结果不一致字段对比：期望为[]空列表, 实际结果：{diff_vals}')
                                assert not diff_vals

                            diff_state = True
                            if db_dict['id'] != plan_id:
                                log.error(f'数据库与期望结果对比：不一致字段id： - 预期结果：{plan_id}, 实际结果：{db_dict["id"]}')
                                diff_state = False
                            if task_param['sched_name'] != expect_data['name']:
                                log.error(
                                    f'数据库与期望结果对比：不一致字段sched_name： - 预期结果：{expect_data["name"]}, 实际结果：{task_param["sched_name"]}')
                                diff_state = False
                            log.info(
                                f'数据库与期望结果不一致字段对比：字段id、sched_name预期结果：{plan_id}--{expect_data["name"]}， 实际结果：{db_dict["id"]}--{task_param["sched_name"]}')
                            if not task_param['enabled']:
                                log.error(f'数据库与期望结果对比：不一致字段enabled： - 预期结果：True, 实际结果：{task_param["enabled"]}')
                                diff_state = False
                            assert diff_state
                break
            if time.time() > end_time:
                with allure.step('断言数据库 与 预期结果 一致'):
                    allure.attach('断言', f'{img_info} - 期望结果：{expect_data}, 实际结果：[]')
                    log.error(f'断言失败 {img_info} 期望结果：{expect_data}，实际结果：[]')
                    assert 0  # 条件为假时，程序自动崩溃并抛出AssertionError的异常。
            time.sleep(sleep_time)


if __name__ == '__main__':
    import time
    import json

    db = DbPage()
    db.assert_config_data('断言 升级方式db文件设置状态', subkey='update', name='auto_update', expect=-1)
    # # res = db.get_count_from_db('日志数量', 'log.db', f"select count(*) from HrLogV3 ;", 8)
    # res = db.assert_quarantine_files_in_dirs('获取详细的日志信息', 1, current_time=1649311817)
    # log.info(f'-------得到的信息内容{res}-----------')
