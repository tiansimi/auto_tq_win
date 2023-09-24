# -*- coding:utf-8 -*-
# @Time   : 2022/3/24 17:23
# @Author : tq
# @File   : file.py
import os
import json
import shutil
import stat
import time

from common.log import log
from conf.confpath import ConfPath
from utils.sys_info import sys_info


class File:
    def __init__(self):
        pass

    def is_exist_path(self, path):
        """ 检测 文件或路径是否存在 """
        if os.path.exists(path):
            return True
        return False

    def remove(self, file_path, su=None):
        """ 删除文件或文件夹
        :param file_path: 文件或文件夹路径完整路径。
        :param su: 是否使用sudo执行命令
        :return:
        """
        if os.path.exists(file_path):
            # 删除文件
            if su:
                os.system(f'sudo rm -rf {file_path}')
            else:
                os.system(f'rm -rf {file_path}')
            if not os.path.exists(file_path):
                log.info(f'成功删除 - 成功删除 - 路径：{file_path}')
                return True
            else:
                log.error(f'失败删除 - 失败删除 - 路径：{file_path}')
                return False
        else:
            log.info(f'文件不存在：{file_path}')
            return False

    def copy_from(self, src, dst):
        """ 拷贝文件或文件夹 从 window 拷贝到 linux 本地
        :param src: 源文件路径
        :param dst: 目的文件路径
        :param su: 是否使用sudo执行命令
        :return:
        """
        try:
            log.info('使用sshpass形式拷贝文件')
            os.system(f'sshpass -p Q1w2e3r4 scp -r test01@192.168.3.194:{src} {dst}')
            assert os.path.exists(dst)
        except Exception as e:
            log.error(f'拷贝失败：{e}')
            return False
        else:
            if os.path.exists(os.path.join(dst, os.path.split(src)[-1])):
                log.info(f'成功拷贝 - 文件源路径：192.168.3.194:{src}--目的路径：{dst}')
                return True
            else:
                log.error(f'失败拷贝 - 文件源路径：{src}--目的路径：{dst}')
                return False

    def copy_local(self, src, dst):
        """ 拷贝文件或文件夹 linux 本地拷贝 """
        try:
            os.system(f'cp -fr {src} {dst}')
            if os.path.exists(os.path.join(dst, os.path.split(src)[-1])):
                log.info(f'成功拷贝 - 文件源路径：192.168.3.194:{src}--目的路径：{dst}')
            else:
                log.error(f'失败拷贝 - 文件源路径：{src}--目的路径：{dst}')
        except Exception as e:
            log.error(f'拷贝失败：{e}')
            return False

    def get_filecount(self, dir_path):
        """
        获取某个目录下，文件数量
        :param dir_path: 目录全路径
        :return:
        """
        if not os.path.isdir(dir_path):
            raise ValueError('不是一个合法的目录路径')

        count = len(os.listdir(dir_path))  # 计算目录下文件数量
        return count

    def get_filesize(self, file_path):
        """
        获取文件或文件夹大小
        :param dir_path: 目录全路径
        :return:
        """
        size = 0
        if not os.path.exists(file_path):
            raise ValueError('不是一个合法的文件或文件夹路径')

        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
        else:
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    size += os.path.getsize(os.path.join(root, file))
        return size

    def files_in_dir(self, dir_path, file_list: list):
        """
        判断文件在文件夹内
        :param dir_path: # dir_path = r'C:\ProgramData\Huorong\Sysdiag\Quarantine'
        :param file_list: # file_list = ['93B1CDD6764DE9B9CE09805AE6FE300647BAC8F0']
        :return:
        """
        files_dirs = []
        if not os.path.isdir(dir_path):
            raise ValueError('不是一个合法的目录路径')

        for root, dirs, files in os.walk(dir_path):
            for file in files:
                files_dirs.append(file)
        length = len(file_list)

        if set(files_dirs) >= set(file_list):
            log.info(f'断言 隔离区包含刚隔离的文件 成功 - 完全包含：{length}个，文件名为：{file_list}')
            return True
        else:
            log.error(f'断言 隔离区包含刚隔离的文件 失败 - 总：{length}个，文件名为：{file_list}，未包含文件名为：{set(file_list) - set(files_dirs)}')
            return False

    def create_file(self, filename):
        """ 创建文件 """
        with open(filename, mode='w', encoding='utf-8'):
            pass

    def create_dir(self, dir):
        """ 创建文件夹 """
        os.makedirs(dir)

    def json_read(self, key, file_path):
        """
        读取 key 值
        :param key:
        :return: list
        """
        with open(file_path, 'r') as fp:
            js = json.load(fp)
        return js.get(key)

    def json_write(self, key, value, file_path):
        with open(file_path, 'r') as fp:
            js = json.load(fp)
        js[key] = value
        with open(file_path, 'w', encoding='utf-8') as fp:
            json.dump(js, fp, indent=4, separators=(',', ': '))

    def get_dir(self, dir_path, string):
        """
        获取目录下，特定文件夹
        :param dir_path: 文件夹路径
        :param contain_string: 以字符串开头
        :return: 文件夹名称
        """
        if not os.path.isabs(dir_path):
            dir_path = os.path.join(ConfPath.DESKTOP_DIR, dir_path)
        files_list = []
        if not os.path.isdir(dir_path):
            print(f'路径为：{dir_path}')
            log.debug(f'路径为：{dir_path}')
            raise ValueError('不是一个合法的目录路径')
        if not isinstance(string, str):
            raise ValueError('extend 必须是字符串！')
        for root, dirs, files in os.walk(dir_path):
            for dir in dirs:
                if dir.startswith(string):
                    return dir
        return 0

    def get_files(self, dir_path, extend=(), contain=None):
        """
        获取目录下，特定扩展名的文件
        :param dir_path: 文件夹路径
        :param extend: 扩展名列表 如 ['.exe','.bat']
        :param contain: 包含
        :return: 文件列表
        """
        if not os.path.isabs(dir_path):
            dir_path = os.path.join(ConfPath.DESKTOP_DIR, dir_path)
        files_list = []
        if not os.path.isdir(dir_path):
            print(f'路径为：{dir_path}')
            log.debug(f'路径为：{dir_path}')
            raise ValueError('不是一个合法的目录路径')
        if not isinstance(extend, (tuple, list,)):
            raise ValueError('extend 必须是元组或列表类型！')
        if contain:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    if contain in file:
                        return file, os.path.join(root, file)
            return 0, 0
        else:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    if os.path.splitext(file)[-1] in extend:
                        files_list.append(os.path.join(root, file))
            return files_list

    def get_id_version(self, path):
        """ 获取 path路径的 id 及 版本号 """
        id2 = self.get_dir(path, 'id')
        filename, file_path = self.get_files(path, contain='installer')
        # version = filename.split('-')[1]
        return id2, filename

    def get_txt_text(self, file_path):
        """ 获取path路径下txt文件内容 """
        f = open(file_path, encoding="utf-8")
        text = f.readlines()
        f.close()
        return text

    def get_file_size_convert(self, value):
        """ 字节自适应转换单位
        :param value: 字节数
        :return: 识别后单位
        """
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        size = 1024.0
        for i in range(len(units)):
            if (value / size) < 1:
                return "%.2f%s" % (value, units[i])
            value = value / size

fo = File()

