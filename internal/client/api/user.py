from internal.client.api import net_client
from internal.data.request import CppCookies, CppHeaders
from internal.data.response import LoginResponse, LoginToken
from internal.util import log


class UserApi:
    """
    用户接口
    """

    @staticmethod
    def query_login(username: str, password: str) -> LoginResponse:
        """
        登录

        :param username: 用户名
        :param password: 密码

        :return LoginResponse: 登入数据
        """
        url = ""
        data = {}
        resp = net_client.request("post", url, data=data)

        try:
            token = resp.data["token"]

            cpp_cookies = CppCookies(token='"' + token + '"')
            cpp_headers = CppHeaders()
            net_client.refresh("cookie", cpp_cookies.model_dump())
            net_client.refresh("header", cpp_headers.model_dump(by_alias=True))
            net_client.token = token

            log.debug("Token 已刷新")
            resp.msg = "Token 已刷新"
            resp.code = 0

        except KeyError:
            log.error("账号或密码错误")
            token = ""
            resp.msg = "账号或密码错误"
            resp.code = 114514

        return LoginResponse(
            code=resp.code,
            msg=resp.msg,
            data=LoginToken(token=token),
        )
