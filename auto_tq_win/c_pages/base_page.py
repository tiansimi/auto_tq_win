# -*- coding:utf-8 -*-
# @Time   : 2022/3/30 10:17
# @Author : tq
# @File   : base_page.py
import time

import allure
from common.opencv import OpenCV
from common.log import log
from common.action import Action

from utils.file import fo
from c_pages.db_page import DbPage
from c_pages.assert_page import AssertPage
from c_pages.shell_page import ShellPage
from utils.sys_info import sys_info
from datetime import datetime


class BasePage(OpenCV, DbPage, AssertPage, ShellPage):
    def __init__(self):
        # super(BasePage, self).__init__()
        OpenCV.__init__(self)
        DbPage.__init__(self)
        AssertPage.__init__(self)
        ShellPage.__init__(self)

        self.act = Action()

    def click_center(self, img_info, img_path, double=False, right=False):
        """ 单击图片中间位置
        :param img_info: 步骤信息
        :param img_path: 图片路径
        :param click_2: True 两次单击代替双击
        :return:
        """
        self.click_position(img_info, img_path, double=double, right=right)

    def click_position(self, img_info, img_path, x_percent=None, y_percent=None,
                       double=False, right=False, move=True):
        """ 单击 图片*percent 的位置，x_percent为横向系数
        :param img_info: 步骤信息
        :param img_path: 图片路径
        :param x_percent: 百分比系数
        :param y_percent: 百分比系数
        :param double: 双击
        :param click_2: True 两次单击 double=True 时生效
        :param right: 右键点击
        :param move: False 表示点击完后，鼠标不移动
        :return:
        """
        with allure.step(f'点击【{img_info}】'):
            loc = self.get_loc_position(img_info, img_path, x_percent=x_percent, y_percent=y_percent)
            try:
                log.debug(f'点击的坐标位置是：{loc}')
                time.sleep(0.5)
                if right:
                    self.act.to_click_right(*loc)
                    return
                if not double:
                    self.act.to_click(*loc, move=move)
                else:
                    self.act.to_click_double(*loc)
                log.info(f'正常点击【{img_info}】--图片路径：{img_path}')
            except Exception as e:
                log.error(f'失败点击【{img_info}】--图片路径：{img_path}')
                log.error(e)

    def click_position_index(self, img_info, img_path, index=1, x_percent=None, y_percent=None):
        """ 单击 图片*percent 的位置，x_percent为横向系数
        :param img_info: 图片名称
        :param img_path: 图片路径
        :param index: 索引，第几个位置 0:第一个； 1：第一个；  2：第二个；  -1：倒数第一个
        :param x_percent: 百分比系数
        :param y_percent: 百分比系数
        :return:
        """
        with allure.step(f'点击，第{index}个【{img_info}】'):
            try:
                length, loc = self.get_locs_position(img_info, img_path, x_percent=x_percent, y_percent=y_percent)
                if index > 0:
                    loc_index = loc[index - 1]
                else:
                    loc_index = loc[index]
                self.act.to_click(*loc_index)
                log.info(f'正常点击第{index}个【{img_info}】--图片路径：{img_path}')
            except Exception as e:
                log.error(f'失败点击第{index}个【{img_info}】--图片路径：{img_path}')
                log.error(e)
                self.savescreen('failures.png')

    def scroll_down(self, img_path, count):
        """
        点击图片中间位置，然后按键的次数
        :param img_path:
        :param count: 次数
        :return:
        """
        self.click_center('点击图片一下获取焦点', img_path)
        for i in range(count):
            self.act.press_keys('down')

    def scroll_up(self, img_path, count):
        """
        点击图片中间位置，然后按键的次数
        :param img_path:
        :param count: 次数
        :return:
        """
        self.click_center('点击图片一下获取焦点', img_path)
        for i in range(count):
            self.act.press_keys('up')

    def press_keys_enter(self):
        """ 点击回车按键 """
        with allure.step(f'点击回车'):
            try:
                self.act.press_keys('enter')
                log.info(f'正常点击回车')
            except Exception as e:
                log.error(f'回车点击失败')
                log.error(e)

    def press_keys_tab(self):
        """ 点击Tab按键 """
        with allure.step(f'点击Tab'):
            try:
                self.act.press_keys('tab')
                log.info(f'正常点击Tab')
            except Exception as e:
                log.error(f'Tab点击失败')
                log.error(e)

    def copy(self, img_info, src, dst):
        with allure.step(f'拷贝{img_info}'):
            res = fo.copy_from(src, dst)
            assert res

    def remove(self, img_info, file_path, su=None):
        with allure.step(f'删除{img_info}'):
            fo.remove(file_path, su)
            # assert res

    def send_text(self, info, text):
        """ 输入文字 """
        with allure.step(f'输入{info}：{text}'):
            try:
                # txt = [i for i in text]
                for txt in text:
                    time.sleep(0.2)
                    self.act.press_keys(txt)
                log.info(f'输入【{info}】成功，输入内容：{text}')
            except Exception as e:
                log.error(f'输入【{info}】异常，输入内容：{text}')
                log.error(e)

    def delete_text(self, img_info):
        """ 全选后删除文本 """
        with allure.step(f'删除全部【{img_info}】'):
            try:
                self.act._delete_all()
                log.info(f'正常删除全部【{img_info}】')
            except Exception as e:
                log.error(f'异常删除全部【{img_info}】')
                log.error(e)

    def send_text_paste(self, img_info, text):
        with allure.step(f'输入【{img_info}】:{text}'):
            try:
                self.act._send_text(text=text)
                log.info(f'正常输入【{img_info}】:{text}')
            except Exception as e:
                log.error(f'异常输入【{img_info}】:{text}')
                log.error(e)

    def kill_process(self, process):
        """ 结束进程 """
        with allure.step(f'结束进程{process}'):
            try:
                res = sys_info.kill_process_running(process)
                if res == 0:
                    log.info(f'结束进程【{process}】成功')
                else:
                    log.error(f'结束进程【{process}】失败')
            except Exception as e:
                log.error(f'结束进程【{process}】异常')
                log.error(e)
            assert res == 0

    def get_current_time(self):
        """ 获取当前时间 """
        tm = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        week = datetime.now().isoweekday()
        hour = datetime.now().hour
        return week, hour, tm


if __name__ == '__main__':
    time.sleep(3)
    BasePage().send_text('dd', '/home/test/softs/trustedzone')
