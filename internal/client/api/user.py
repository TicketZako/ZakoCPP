from internal.client.net import net_manager
from internal.data.request import CppCookies, CppHeaders
from internal.data.response import QueryLoginResponse, QueryLoginToken
from internal.util import log


class UserApi:
    """
    用户接口
    """

    @staticmethod
    def query_login(username: str, password: str) -> QueryLoginResponse:
        """
        登录

        :param username: 用户名
        :param password: 密码

        :return LoginResponse: 登录数据
        """
        url = ""
        data = {}
        resp = net_manager.request("post", url, data=data)

        if resp.code != -1:
            log.error(f"登陆失败: {resp.msg}")
            return QueryLoginResponse(
                code=resp.code,
                msg=resp.msg,
                data=None,
            )

        try:
            token = resp.data["token"]

            cpp_cookies = CppCookies(token='"' + token + '"')
            cpp_headers = CppHeaders()
            net_manager.refresh("cookie", cpp_cookies.model_dump())
            net_manager.refresh("header", cpp_headers.model_dump(by_alias=True))
            net_manager.token = token

            log.debug("Token 已刷新")
            resp.msg = "Token 已刷新"
            resp.code = 0

        except KeyError:
            log.error("账号或密码错误")
            token = ""
            resp.msg = "账号或密码错误"
            resp.code = 114514

        return QueryLoginResponse(
            code=resp.code,
            msg=resp.msg,
            data=QueryLoginToken(token=token),
        )
