import pytest
from utils.cmd_line import CmdLine
from conf.config import conf
from conf.confpath import ConfParams
from c_datas.data_install import DataInstall
from utils.base_api import BaseApi

re_api = BaseApi()


@pytest.fixture(scope='class', autouse=True)
def open_huorong(request):
    """ """
    CmdLine().command('打开火绒', DataInstall.data_open_sh)

#
# @pytest.fixture(scope='session', autouse=True)
# def get_header():
#     """ 获取 headers cookies """
#     login_data = {
#         'method': 'post',
#         'url': '/auth/_login',
#         'json': {"username": "admin", "password": "585004c128942a72dae745732429b88d776d88f5", "remember": False}
#     }
#
#     resp = re_api.http_center('获取COOKIES', login_data, body=False)
#     ConfParams.HEADERS = {
#         'HTTP-CSRF-TOKEN': resp.cookies.get('HRESSCSRF'),
#         'Origin': conf.center_url
#     }
#     ConfParams.COOKIES = dict(resp.cookies)
