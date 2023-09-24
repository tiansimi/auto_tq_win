# -*- coding:utf-8 -*-
# @Time   : 2022/3/24 14:24
# @Author : tq
# @File   : data_path.py
import os

from conf.confpath import ConfPath


class DataVirusScan:
    data_desktop = ConfPath.DESKTOP_DIR
    data_virus = 'c:/AutoTestData/ui_ess20_linux/系统关键位置/eggGG666'
    data_virus_file = 'c:/AutoTestData/ui_ess20_linux/系统关键位置/ed13ce6c259ade4ab1a8ef134b735546e47761bb'
    data_virus_rar = 'c:/AutoTestData/ui_ess20_linux/系统关键位置/压缩包查杀.rar'
    data_virus_7z = 'c:/AutoTestData/ui_ess20_linux/系统关键位置/压缩包查杀1.7z'
    data_big_virus_rar = 'c:/AutoTestData/ui_ess20_linux/系统关键位置/压缩包查杀大于20M2.rar'
    data_virus_desktop = os.path.join(data_desktop, 'eggGG666')

    data_etc = '/etc'
    data_proc = '/proc'
    data_etc_xdg = '/etc/xdg'
    data_opt = '/opt/apps'  # 常用软件
    data_home_path = '/home'
    data_home_test = '/home/test'
    data_home_softs = '/home/test/softs'
    data_home_softs_trustedzone = '/home/test/softs/trustedzone'
    data_etc_init = '/etc/init.d'
    data_virus_etc = os.path.join(data_etc, 'eggGG666')
    data_virus_etc_file = os.path.join(data_etc, 'ed13ce6c259ade4ab1a8ef134b735546e47761bb')
    data_virus_etc_rar = os.path.join(data_etc, '压缩包查杀.rar')
    data_virus_etc_7z = os.path.join(data_etc, '压缩包查杀1.7z')
    data_big_virus_etc_rar = os.path.join(data_etc, '压缩包查杀大于20M2.rar')
    data_virus_proc = os.path.join(data_proc, 'eggGG666')
    data_virus_opt = os.path.join(data_opt, 'eggGG666')
    data_virus_file_opt = os.path.join(data_opt, 'ed13ce6c259ade4ab1a8ef134b735546e47761bb')
    data_virus_file_home = os.path.join(data_home_path, 'ed13ce6c259ade4ab1a8ef134b735546e47761bb')
    data_big_virus_home = os.path.join(data_home_test, '压缩包查杀大于20M2.rar')
    data_virus_test_path = os.path.join(data_home_test, 'eggGG666')
    data_virus_test_path_rar = os.path.join(data_home_test, '压缩包查杀.rar')
    data_virus_test_path_file = os.path.join(data_home_test, 'ed13ce6c259ade4ab1a8ef134b735546e47761bb')
    data_virus_test_softs_trustedzone_path = os.path.join(data_home_softs_trustedzone, 'eggGG666')
    data_virus_softs_path = os.path.join(data_home_softs, 'eggGG666')
    data_virus_softs_path_rar = os.path.join(data_home_softs, '压缩包查杀.rar')

    data_virus_home_path = os.path.join(data_home_path, 'eggGG666')
    data_virus_home_path_rar = os.path.join(data_home_path, '压缩包查杀.rar')


class DataSecurityLog:
    data_update_expect_dic = {"fid": 2, "detail": {"auto": 1, "fetched": [
        {"err": 0, "url": "bases/libvxf.vdl.vfs", "dstfn": "/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vdl"},
        {"err": 0, "url": "bases/libvxf.vds.vfs", "dstfn": "/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vds"},
        {"err": 0, "url": "bases/libvxf.dat.vfs", "dstfn": "/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.dat"},
        {"err": 0, "url": "bases/libvxf.tdl.vfs", "dstfn": "/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.tdl"},
        {"err": 0, "url": "bases/hwl.db.vfs", "dstfn": "/opt/apps/cn.huorong.esm/files/share/virdb/hwl.db"},
        {"err": 0, "url": "bases/prop.db.vfs", "dstfn": "/opt/apps/cn.huorong.esm/files/share/virdb/prop.db"},
        {"err": 0, "url": "bases/pset.db.vfs", "dstfn": "/opt/apps/cn.huorong.esm/files/share/virdb/pset.db"},
        {"err": 0, "url": "bases/troj.db.vfs", "dstfn": "/opt/apps/cn.huorong.esm/files/share/virdb/troj.db"}],
                                                   "merged": [
                                                       {"err": 0,
                                                        "dstfn": "/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vdl"},
                                                       {"err": 0,
                                                        "dstfn": "/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.vds"},
                                                       {"err": 0,
                                                        "dstfn": "/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.dat"},
                                                       {"err": 0,
                                                        "dstfn": "/opt/apps/cn.huorong.esm/files/share/xsse/libvxf.tdl"},
                                                       {"err": 0,
                                                        "dstfn": "/opt/apps/cn.huorong.esm/files/share/virdb/hwl.db"},
                                                       {"err": 0,
                                                        "dstfn": "/opt/apps/cn.huorong.esm/files/share/virdb/prop.db"},
                                                       {"err": 0,
                                                        "dstfn": "/opt/apps/cn.huorong.esm/files/share/virdb/pset.db"},
                                                       {"err": 0,
                                                        "dstfn": "/opt/apps/cn.huorong.esm/files/share/virdb/troj.db"}],
                                                   "err": 0, "errmsg": []}}

    data_update_ignore_data = ['timestamp', 'prevdbtime', 'newver', 'newdbtime', 'prever', 'version']

    # # 查杀两个病毒文件所产生的日志在不同虚拟机顺序不一致
    # data_anti_virus_expect_dic = {"fid": 0, "detail": {"threat_killed": 2, "taskname": "SCANTYPE_full", "threats": 2,
    #                                                    "sysrepair": 0, "threat_list": [
    #         {"id": 1, "fn": "/etc/eggGG666", "sm": 0, "clean": 0, "pid": 0, "mcs": 100, "fid": 0, "cat": 0,
    #          "rid": "9300BC2F36BE71BE", "fnhash": 7974144539504859469, "det": "Adware/JS.MultiPlug.b",
    #          "objn": "/etc/eggGG666", "objnhash": -4143723550219231088, "solid": 1},
    #         {"id": 2, "fn": "/etc/压缩包查杀.rar", "sm": 0, "clean": 0, "pid": 0, "mcs": 100, "fid": 0, "cat": 0,
    #          "rid": "F0FDC288B0144E74", "fnhash": -5180477457208402249, "det": "Backdoor/Hupigon.r",
    #          "objn": "/etc/压缩包查杀.rar >> 新建文件夹/压缩包查杀1.7z >> 僵尸网路/僵尸.7z >> 僵尸/DAT/SERVER.DAT",
    #          "objnhash": 4560609213939144820, "solid": 1}], "sysrepair_fixed": 0, "sysrepair_list": []}}

    data_anti_virus_expect_dic = {"fid": 0, "detail": {"threat_killed": 1, "taskname": "SCANTYPE_full", "threats": 1,
                                                       "sysrepair": 0, "threat_list": [
            {"id": 1, "fn": "/etc/eggGG666", "sm": 0, "clean": 0, "pid": 0, "mcs": 100, "fid": 0, "cat": 0,
             "rid": "9300BC2F36BE71BE", "fnhash": 7974144539504859469, "det": "Adware/JS.MultiPlug.b",
             "objn": "/etc/eggGG666", "objnhash": -4143723550219231088, "solid": 1}], "sysrepair_fixed": 0,
                                                       "sysrepair_list": []}}

    data_anti_virus_ignore_data = ['objects', 'db_version', 'tm_start', 'files', 'duration', 'version']
