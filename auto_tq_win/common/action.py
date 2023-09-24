# -*- coding:utf-8 -*-
# @Time   : 2022/3/24 16:47
# @Author : tq
# @File   : action.py
import time

from conf.confpath import ConfSystemType


import pyautogui

import pyperclip


class Action:
    def to_click(self, x, y, move=True):
        """
        鼠标移动到位置，单击再移动走
        :param x: 横坐标
        :param y: 纵坐标
        :param move: 点击完成后是否移走
        :return:
        """
        pyautogui.moveTo(x, y, duration=0.2)
        # if 'with-Ubuntu' in sys_info.system_version:
        #     time.sleep(0.3)
        # else:
        #     time.sleep(0.5)
        time.sleep(0.1)
        pyautogui.click()
        if move:
            pyautogui.moveTo(1, 1)

    def to_click_double(self, x, y):
        """
        鼠标移动到位置，双击再移走
        :param x: 横坐标
        :param y: 纵坐标
        :return:
        """
        from pynput.mouse import Button, Controller
        pyautogui.moveTo(x, y, duration=0.2)
        time.sleep(0.01)
        mouse = Controller()
        mouse.click(Button.left, count=2)
        pyautogui.moveTo(10, 10)

    def to_click_right(self, x, y):
        """ 鼠标移动到位置，右键单击再移动走 （无法点击 是 回车代替）"""
        pyautogui.moveTo(x, y, duration=0.2)
        pyautogui.rightClick()
        pyautogui.moveTo(10, 10)

    def _send_text(self, text):
        """ 输入 text
        :param text: 输入的文字
        :return:
        """
        pyperclip.copy(text)
        self._delete_all()
        self.send_keys('ctrl', 'v')
        # pyautogui.typewrite(text)

    def _delete_all(self):
        self.send_keys('ctrl', 'a')
        self.press_keys(['delete'])

    def send_keys(self, *args):
        """ 发送热键 如：pyautogui.hotkey("win","d")"""
        import pyautogui
        pyautogui.hotkey(*args)

    def press_keys(self, key):
        """
        按一次 按键
         pyautogui.press(['c', 'h', 'e', 'n'])
         pyautogui.press('shift') # 切换输入法的中英文
        :param key:
        :return:
        """
        pyautogui.press(key)

    def drag_to(self, a, b, x, y):
        """
        拖动到指定位置
        :param x:
        :param y:
        :return:
        """
        pyautogui.moveTo(a, b, duration=0.2)
        pyautogui.mouseDown()
        pyautogui.dragTo(x, y, button='left')
        pyautogui.mouseUp()
        pyautogui.moveTo(10, 10)


if __name__ == '__main__':
    import time
    time.sleep(2)
    # Action().drag_to(1507, 405, 1507, 500)
    # pyautogui.moveTo(1507, 405, duration=1)
    # pyautogui.mouseDown()
    # pyautogui.dragTo(1507, 500, button='left')
    # pyautogui.mouseUp()

    # pyautogui.moveTo(1507, 405, duration=1)
    # pyautogui.click()
    # time.sleep(1)
    # pyautogui.doubleClick()
    from pynput.mouse import Button, Controller

    mouse = Controller()
    pyautogui.moveTo(1507, 405)
    mouse.click(Button.left, count=2)
