import os
import time
import allure
import operator
from utils.cmd_line import CmdLine
from common.log import log


class ShellPage:

    def __int__(self):
        self.cmd = CmdLine()

    def shell(self, img_info, shell):
        """ """
        self.cmd.command(img_info, shell)

    def shell_popen_list(self, img_info, shell):
        """ 命令行执行 shell 命令，返回命令的输出内容 """
        with allure.step(f'执行{img_info} 命令：{shell}'):
            result = self.cmd.command_popen_list(shell)
            assert result
            return result

    def shell_popen(self, img_info, shell):
        """ 命令行执行 shell 命令，返回命令的输出内容 """
        with allure.step(f'执行{img_info} 命令：{shell}'):
            result = self.cmd.command_popen(shell)
            assert result
            return result

    def shell_popen_kill_process(self, img_info, shell, ele, timeout=15, sleep_time=3):
        """ 命令行执行 shell 命令，返回命令的输出内容 """
        end_time = time.time() + timeout
        while True:
            with allure.step(f'执行{img_info} 命令：{shell}'):
                result = self.cmd.command_popen_kill_process(shell)
                log.info(f'获取hrconsole 返回日志：{str(result)}')
                if ele in result[1]:
                    return result

                if time.time() > end_time:
                    with allure.step('断言TUI界面返回内容'):
                        allure.attach('断言', f'{img_info} - 期望结果：包含{ele}, 实际结果：{result}')
                        log.error(f'断言失败 {img_info} 期望结果：包含{ele}，实际结果：{result}')
                        assert 0  # 条件为假时，程序自动崩溃并抛出AssertionError的异常。

    def assert_shell_data(self, img_info, shell, expect_data, expect_count):
        """
        从数据详细信息中获取指定的参数
        @param img_info: 描述信息
        @param expect_data: 预期数据
        @param expect_count: 预期匹配数据条数
        @param ignore_data: 忽略信息，开始、结束时间等
        @return:
        """
        with allure.step(f'断言：{img_info}，脚本输出内容与预期相符'):
            allure.attach('断言', f'{img_info}内容与期望相符')
            try:
                result = self.cmd.command_popen(img_info, shell)
                count = len(result)
                state = operator.eq(result, expect_data)

                if state:
                    log.info(f'断言成功【{img_info}】，比对结果相符，期望匹配日志条数为：{expect_count}，实际匹配的条数为：{count}')
                else:
                    log.info(f'断言失败【{img_info}】，比对结果不相符，期望匹配日志条数为：{expect_count}，实际匹配的条数为：{count}')

                # for data in result:
                #     pass

                assert count == expect_count
            except Exception as e:
                log.info(f'断言失败【{img_info}】，内部发生异常！')
                assert 0

    def open_url(self, url):
        """ 打开一个网址 https://www.baidu.com """
        import webbrowser
        webbrowser.open(url)
