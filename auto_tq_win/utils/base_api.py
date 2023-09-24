# -*- coding:utf-8 -*-
# @Time   : 2022/2/10 14:57
# @Author : tq
# @File   : base_api.py
import json
import requests
import allure

from conf.config import conf
from conf.confpath import ConfParams, ConfPath
from common.log import log


class BaseApi:
    def __init__(self):
        self.center_url = conf.center_url

    def http_center(self, step_info, data, body=True):
        if isinstance(data, str):
            data = json.loads(self.replace_str(data))
        if not isinstance(data, dict):
            raise ValueError(f'data数据不是正确的字典格式，请检查传入参数！\n当前data 为: {data}')
        if not 'url' in data:
            raise ValueError('请求参数中没有 url')
        if not data['url'].startswith('http'):
            data['url'] = self.center_url + data['url']
        # 请求加入 headers 和 cookies
        data['headers'], data['cookies'] = {}, {}
        data['headers'] = ConfParams.HEADERS
        data['cookies'] = ConfParams.COOKIES

        log.info(f'{step_info}-center请求数据：{json.dumps(data, ensure_ascii=False, sort_keys=True)}')
        with allure.step(f'{step_info}'):
            allure.attach(f'{step_info}-center请求数据', json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))
            try:
                resp = requests.request(**data)
                # 更新 cookies
                if resp.cookies.get('HRESSCSRF'):
                    ConfParams.HEADERS['HTTP-CSRF-TOKEN'] = resp.cookies.get('HRESSCSRF')
                    ConfParams.COOKIES['HRESSCSRF'] = resp.cookies.get('HRESSCSRF')
                    # data['headers']['HTTP-CSRF-TOKEN'] = resp.cookies.get('HRESSCSRF')
                    # data['cookies']['HRESSCSRF'] = resp.cookies.get('HRESSCSRF')
                if body:
                    try:
                        log.debug(resp.text)
                        js = resp.json()
                        allure.attach(f'{step_info}-center返回结果', json.dumps(js, ensure_ascii=False, sort_keys=True, indent=4))
                        log.info(f'{step_info}-center返回结果:{json.dumps(js, ensure_ascii=False, sort_keys=True)}')
                        assert js.get('errno') == 0
                        return js
                    except:
                        txt = resp.text
                        log.error(txt)
                        allure.attach(f'{step_info}-center返回结果', txt)
                        assert 0
                        # return txt
                else:
                    return resp
            except Exception as e:
                log.error(f'center请求响应出错！出错信息为：{e}')
                allure.attach('center请求响应出错', f'请求响应出错！出错信息为：{e}')
                assert 0

    @staticmethod
    def replace_str(data):
        """
        字符替换
        :param data:
        :return:
        """
        if isinstance(data, str):
            new_data = data \
                .replace('｛', '{').replace('｝', '}') \
                .replace('‘', '"').replace('”', '"') \
                .replace("\'", '"')

            return new_data
        return data


if __name__ == '__main__':
    import time
    re_api = BaseApi()
    login_data = {
        'method': 'post',
        'url': '/auth/_login',
        'json': {"username": "admin", "password": "585004c128942a72dae745732429b88d776d88f5", "remember": False}
    }
    resp = re_api.http_center('', login_data, body=True)
    print(resp)

